"""
Tests for Provider, Invoice, and Line resources.

Covers CRUD for each, the Provider→Invoice→Line cascade chain, the persistence-layer
total recalculation event listener, and the positivity validator on Line.price/quantity.
"""

import pytest


def make_prov(rm, token, name, address="Addr"):
    """Helper to create a provider and return its id."""
    return rm.action(token, "provider", "post", name=name, address=address)


class TestProvider:
    """CRUD for Provider resources."""

    @pytest.mark.asyncio
    async def test_create(self, rm, test_user):
        result = await make_prov(rm, test_user["token"], "ACME", "123 Main St")
        providers = result.get("new", {}).get("Provider", [])
        assert len(providers) == 1
        assert providers[0]["name"] == "ACME"

    @pytest.mark.asyncio
    async def test_delete_cascades_to_invoices_and_lines(self, rm, test_user):
        """Deleting a Provider must cascade-delete its invoices and lines."""
        prov = await make_prov(rm, test_user["token"], "Cascade Test")
        pid = str(prov["new"]["Provider"][0]["id"])
        inv = await rm.action(test_user["token"], "invoice", "post", provider_id=pid, number="INV-001")
        iid = str(inv["new"]["Invoice"][0]["id"])
        await rm.action(test_user["token"], "line", "post", invoice_id=iid, product="Widget", price=10.0, quantity=2)

        # Delete provider
        await rm.action(test_user["token"], "provider", "delete", pks=[pid])

        # Verify invoice and line are gone
        inv_query = await rm.action(test_user["token"], "invoice", "query", filter={"id": iid})
        assert inv_query["payload"]["totalCount"] == 0
        line_query = await rm.action(test_user["token"], "line", "query", filter={"invoice_id": iid})
        assert line_query["payload"]["totalCount"] == 0


class TestInvoice:
    """CRUD and business logic for Invoice resources."""

    @pytest.mark.asyncio
    async def test_create_with_provider(self, rm, test_user):
        prov = await make_prov(rm, test_user["token"], "Widget Co")
        pid = str(prov["new"]["Provider"][0]["id"])
        result = await rm.action(test_user["token"], "invoice", "post", provider_id=pid, number="INV-042")
        invoices = result.get("new", {}).get("Invoice", [])
        assert len(invoices) == 1
        assert invoices[0]["number"] == "INV-042"

    @pytest.mark.asyncio
    async def test_cascade_delete_to_lines(self, rm, test_user):
        """Deleting an Invoice must cascade-delete its lines."""
        prov = await make_prov(rm, test_user["token"], "Co")
        pid = str(prov["new"]["Provider"][0]["id"])
        inv = await rm.action(test_user["token"], "invoice", "post", provider_id=pid, number="INV-DEL")
        iid = str(inv["new"]["Invoice"][0]["id"])
        await rm.action(test_user["token"], "line", "post", invoice_id=iid, product="A", price=5.0, quantity=1)

        # Delete invoice
        await rm.action(test_user["token"], "invoice", "delete", pks=[iid])
        line_q = await rm.action(test_user["token"], "line", "query", filter={"invoice_id": iid})
        assert line_q["payload"]["totalCount"] == 0


class TestLine:
    """CRUD and business logic for Line resources."""

    @pytest.mark.asyncio
    async def test_create_line_updates_invoice_total(self, rm, test_user):
        """GIVEN an invoice, WHEN a line is created, THEN the invoice total_amount is recalculated."""
        prov = await make_prov(rm, test_user["token"], "Shop")
        pid = str(prov["new"]["Provider"][0]["id"])
        inv = await rm.action(test_user["token"], "invoice", "post", provider_id=pid, number="INV-TOT")
        iid = str(inv["new"]["Invoice"][0]["id"])

        # Add line: 3 × 10 = 30
        await rm.action(test_user["token"], "line", "post", invoice_id=iid, product="Gadget", price=10.0, quantity=3)

        # Read back invoice — total_amount should be 30
        r = await rm.action(test_user["token"], "invoice", "get", pks=[iid])
        inv_data = r.get("read", {}).get("Invoice", [])
        assert len(inv_data) == 1
        assert inv_data[0]["total_amount"] == 30.0, f"Expected 30.0, got {inv_data[0]['total_amount']}"

    @pytest.mark.asyncio
    async def test_update_line_price_recalculates_total(self, rm, test_user):
        """GIVEN an invoice with a line, WHEN the line price changes, THEN total_amount updates."""
        prov = await make_prov(rm, test_user["token"], "Fix Price")
        pid = str(prov["new"]["Provider"][0]["id"])
        inv = await rm.action(test_user["token"], "invoice", "post", provider_id=pid, number="INV-UPD")
        iid = str(inv["new"]["Invoice"][0]["id"])

        line = await rm.action(test_user["token"], "line", "post", invoice_id=iid, product="Item", price=5.0, quantity=4)
        lid = str(line["new"]["Line"][0]["id"])

        # Update price: 5 → 10, so total should become 10 × 4 = 40
        await rm.action(test_user["token"], "line", "put", id=lid, price=10.0, quantity=4, invoice_id=iid, product="Item")

        r = await rm.action(test_user["token"], "invoice", "get", pks=[iid])
        inv_data = r.get("read", {}).get("Invoice", [])
        assert inv_data[0]["total_amount"] == 40.0, f"Expected 40.0, got {inv_data[0]['total_amount']}"

    @pytest.mark.asyncio
    @pytest.mark.xfail(reason="The validate_positive validator raises ValueError, but it's not yet surfaced as a HandledValidation or 422. Requires wiring the validation error into the request handling path.")
    async def test_reject_negative_price(self, rm, test_user):
        """Line.price must be non-negative (persistence-layer invariant)."""
        prov = await make_prov(rm, test_user["token"], "Bad Price")
        pid = str(prov["new"]["Provider"][0]["id"])
        inv = await rm.action(test_user["token"], "invoice", "post", provider_id=pid, number="INV-NEG")
        iid = str(inv["new"]["Invoice"][0]["id"])

        with pytest.raises(Exception, match="must be non-negative"):
            await rm.action(test_user["token"], "line", "post", invoice_id=iid, product="Bad", price=-5.0, quantity=1)

    @pytest.mark.asyncio
    async def test_multiple_lines_total(self, rm, test_user):
        """Invoice with multiple lines accumulates the correct total."""
        prov = await make_prov(rm, test_user["token"], "Multi")
        pid = str(prov["new"]["Provider"][0]["id"])
        inv = await rm.action(test_user["token"], "invoice", "post", provider_id=pid, number="INV-MULTI")
        iid = str(inv["new"]["Invoice"][0]["id"])

        await rm.action(test_user["token"], "line", "post", invoice_id=iid, product="A", price=10.0, quantity=2)   # 20
        await rm.action(test_user["token"], "line", "post", invoice_id=iid, product="B", price=5.0, quantity=3)    # 15
        await rm.action(test_user["token"], "line", "post", invoice_id=iid, product="C", price=2.5, quantity=4)    # 10

        r = await rm.action(test_user["token"], "invoice", "get", pks=[iid])
        inv_data = r.get("read", {}).get("Invoice", [])
        assert inv_data[0]["total_amount"] == pytest.approx(45.0), f"Expected 45.0, got {inv_data[0]['total_amount']}"