from app.models import Invoice, InvoiceStatus


def test_invoice_balance_due_property():
    invoice = Invoice(invoice_number="INV-X", total=250, amount_paid=75, status=InvoiceStatus.sent)
    assert invoice.balance_due == 175

