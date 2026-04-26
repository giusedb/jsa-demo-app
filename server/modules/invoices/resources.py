import os
from itertools import groupby
from operator import itemgetter
from typing import List, Dict

import yaml
from sqlalchemy import delete, select, func
from sqlalchemy.orm import DeclarativeBase
from yaml import SafeLoader

from jsalchemy_api import DBResource, ResourceManager
from jsalchemy_api.resources.base import verb
from jsalchemy_web_context import db
from .models import Provider, Invoice, Line


class ProviderResouce(DBResource):

    def __init__(self, resource_manager: ResourceManager):
        super().__init__(
            name='Provider',
            model=Provider,
            resource_manager=resource_manager,
        )

    @verb(detached_instance=True)
    async def delete(self, pks: List[str]):
        invoice_ids = (await db.execute(select(Invoice.id).where(Invoice.provider_id.in_(pks)))).scalars().all()
        await db.execute(delete(Line).where(Line.invoice_id.in_(invoice_ids)))
        await db.execute(delete(Invoice).where(Invoice.provider_id.in_(pks)))
        return await super().delete(pks)

class InvoiceResource(DBResource):
    def __init__(self, resource_manager: ResourceManager):
        super().__init__(name='Invoice',model=Invoice, resource_manager=resource_manager)

    @verb(detached_instance=True)
    async def delete(self, pks: List[str]):
        await db.execute(delete(Line).where(Line.invoice_id.in_(pks)))
        return await super().delete(*pks)

    @verb(detached_instance=True)
    async def fixture(self):
        with open(os.sep.join(os.path.dirname(__file__).split(os.sep)[:-2] + ['fixtures', 'invoices.yaml'])) as f:
            fixture = yaml.load(f, SafeLoader)

        max_provider_id = (await db.execute(select(func.max(Provider.id)))).scalar()
        max_invoice_id = (await db.execute(select(func.max(Invoice.id)))).scalar()
        max_line_id = (await db.execute(select(func.max(Line.id)))).scalar()

        for provider in fixture['providers']:
            db_provider = Provider(**{k: v for k, v in provider.items() if type(v) is not list})
            db.add(db_provider)
            for invoice in provider.get('invoices', ()):
                db_invoice = Invoice(**{k: v for k, v in invoice.items() if type(v) is not list}, provider = db_provider)
                db.add(db_invoice)
                for line in invoice.get('lines', ()):
                    db.add(Line(**line, invoice=db_invoice))
                db_invoice.total_amount = sum(line['quantity'] * line['price'] for line in invoice.get('lines', ()))
        await db.flush()
        await db.execute(delete(Line).where(Line.id <= max_line_id))
        await db.execute(delete(Invoice).where(Invoice.id <= max_invoice_id))
        await db.execute(delete(Provider).where(Provider.id <= max_provider_id))


class LineResource(DBResource):
    async def bulk(self, records: List[Dict]):
        """Bulk insert records"""
        await super().bulk(records)
        i_ids = {rec['invoice_id'] for rec in records}
        self.update_invoice(i_ids)

    async def update_invoice(self, *invoice_ids):
        i_ids = tuple(filter(bool, invoice_ids))
        if i_ids:
            await db.flush()
            for invoice in (await db.execute(select(Invoice).where(Invoice.id.in_(i_ids)))).scalars().all():
                invoice.total_amount = await invoice.get_total()

    async def post(self, **record: dict) -> None:
        super().post(**record)
        await self.update_invoice(record.get('invoice_id'))

    @verb(detached_instance=True)
    async def put(self, **record: dict) -> None:
        await super().put(**record)
        await db.flush()
        await self.update_invoice(record.get('invoice_id') or (await db.get(self.model, record['id'])).invoice_id)
        await db.flush()


    def __init__(self, resource_manager: ResourceManager):
        super().__init__(name='Line',model=Line, resource_manager=resource_manager)
