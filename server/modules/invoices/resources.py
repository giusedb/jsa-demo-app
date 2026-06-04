import os
from itertools import groupby
from operator import itemgetter
from typing import List, Dict

import yaml
from sqlalchemy import delete, select, func
from sqlalchemy.orm import DeclarativeBase, selectinload
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
        return await super().delete(pks)


class InvoiceResource(DBResource):
    def __init__(self, resource_manager: ResourceManager):
        super().__init__(name='Invoice', model=Invoice, resource_manager=resource_manager)

    @verb(detached_instance=True)
    async def delete(self, pks: List[str]):
        return await super().delete(pks)

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
                db_invoice = Invoice(**{k: v for k, v in invoice.items() if type(v) is not list},
                                     provider=db_provider)
                db.add(db_invoice)
                for line in invoice.get('lines', ()):
                    db.add(Line(**line, invoice=db_invoice))
                db_invoice.total_amount = sum(
                    line['quantity'] * line['price'] for line in invoice.get('lines', ()))
        await db.flush()
        await db.execute(delete(Line).where(Line.id <= max_line_id))
        await db.execute(delete(Invoice).where(Invoice.id <= max_invoice_id))
        await db.execute(delete(Provider).where(Provider.id <= max_provider_id))


class LineResource(DBResource):

    def __init__(self, resource_manager: ResourceManager):
        super().__init__(name='Line', model=Line, resource_manager=resource_manager)

    async def _recalculate_invoice_total(self, invoice_id):
        """Update the invoice's total_amount to reflect its current lines."""
        if invoice_id:
            invoice = (await db.execute(
                select(Invoice)
                .where(Invoice.id == int(invoice_id))
                .options(selectinload(Invoice.lines))
            )).scalar_one_or_none()
            if invoice:
                invoice.total_amount = sum(
                    l.quantity * l.price for l in invoice.lines
                )

    async def post(self, **record: dict) -> None:
        await super().post(**record)
        await self._recalculate_invoice_total(record.get('invoice_id'))

    @verb(detached_instance=True)
    async def put(self, **record: dict) -> None:
        # Resolve the invoice_id before the update in case it includes a new invoice_id
        inv_id = record.get('invoice_id')
        await super().put(**record)
        await db.flush()
        await self._recalculate_invoice_total(inv_id)
        await db.flush()

    async def bulk(self, records: List[Dict]):
        """Bulk insert records and recalculate invoice totals."""
        await super().bulk(records)
        inv_ids = {rec['invoice_id'] for rec in records if 'invoice_id' in rec}
        for iid in inv_ids:
            await self._recalculate_invoice_total(iid)