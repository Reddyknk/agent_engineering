import pytest
from unittest.mock import MagicMock, call
from order import (
    Order,
    InventoryService,
    PaymentGateway,
    InventoryShortageError,
    PaymentFailedError,
    InvalidOrderError,
)

@pytest.fixture
def mock_inventory():
    """Fixture providing a mocked InventoryService with spec."""
    return MagicMock(spec=InventoryService)

@pytest.fixture
def mock_payment():
    """Fixture providing a mocked PaymentGateway with spec."""
    return MagicMock(spec=PaymentGateway)

@pytest.fixture
def regular_order(mock_inventory, mock_payment):
    """Fixture providing a standard draft order for a regular customer."""
    return Order(
        inventory_service=mock_inventory,
        payment_gateway=mock_payment,
        customer_email="user@example.com",
        is_vip=False,
    )

@pytest.fixture
def vip_order(mock_inventory, mock_payment):
    """Fixture providing a draft order for a VIP customer."""
    return Order(
        inventory_service=mock_inventory,
        payment_gateway=mock_payment,
        customer_email="vip@example.com",
        is_vip=True,
    )

# --- Cart Operations Tests ---

class TestCartOperations:
    def test_add_item_new_product(self, regular_order):
        regular_order.add_item("item-1", price=25.0, quantity=2)
        assert regular_order.items == {"item-1": {"price": 25.0, "qty": 2}}

    def test_add_item_existing_product_increases_quantity(self, regular_order):
        regular_order.add_item("item-1", price=25.0, quantity=2)
        regular_order.add_item("item-1", price=25.0, quantity=3)
        assert regular_order.items["item-1"]["qty"] == 5

    def test_add_item_negative_price_raises_value_error(self, regular_order):
        with pytest.raises(ValueError, match="Price cannot be negative"):
            regular_order.add_item("item-1", price=-10.0, quantity=1)

    @pytest.mark.parametrize("invalid_qty", [0, -1, -5])
    def test_add_item_invalid_quantity_raises_value_error(self, regular_order, invalid_qty):
        with pytest.raises(ValueError, match="Quantity must be greater than zero"):
            regular_order.add_item("item-1", price=10.0, quantity=invalid_qty)

    def test_remove_item_existing(self, regular_order):
        regular_order.add_item("item-1", price=10.0, quantity=1)
        regular_order.add_item("item-2", price=20.0, quantity=2)
        regular_order.remove_item("item-1")
        assert "item-1" not in regular_order.items
        assert "item-2" in regular_order.items

    def test_remove_item_non_existent_does_not_raise_error(self, regular_order):
        regular_order.add_item("item-1", price=10.0, quantity=1)
        regular_order.remove_item("non-existent-id")
        assert "item-1" in regular_order.items

    def test_total_price_calculation(self, regular_order):
        regular_order.add_item("item-1", price=15.0, quantity=2)  # 30.0
        regular_order.add_item("item-2", price=45.0, quantity=1)  # 45.0
        assert regular_order.total_price == 75.0


# --- Discount Business Logic Tests ---

class TestDiscountLogic:
    def test_vip_discount_under_100(self, vip_order):
        vip_order.add_item("item-1", price=50.0, quantity=1)
        # 50 * 0.8 = 40.0
        assert vip_order.apply_discount() == 40.0

    def test_vip_discount_over_100(self, vip_order):
        vip_order.add_item("item-1", price=200.0, quantity=1)
        # 200 * 0.8 = 160.0 (VIP 20% overrides regular 10%)
        assert vip_order.apply_discount() == 160.0

    def test_regular_discount_over_100(self, regular_order):
        regular_order.add_item("item-1", price=150.0, quantity=1)
        # 150 * 0.9 = 135.0
        assert regular_order.apply_discount() == 135.0

    def test_regular_discount_exactly_100_no_discount(self, regular_order):
        regular_order.add_item("item-1", price=100.0, quantity=1)
        # Total is 100, not > 100 -> no discount
        assert regular_order.apply_discount() == 100.0

    def test_regular_discount_under_100_no_discount(self, regular_order):
        regular_order.add_item("item-1", price=80.0, quantity=1)
        assert regular_order.apply_discount() == 80.0


# --- Checkout Orchestration & Mocking Tests ---

class TestCheckoutOrchestration:
    def test_checkout_empty_cart_raises_invalid_order_error(self, regular_order):
        with pytest.raises(InvalidOrderError, match="Cannot checkout an empty cart"):
            regular_order.checkout()

    def test_checkout_insufficient_stock_raises_error(self, regular_order, mock_inventory, mock_payment):
        regular_order.add_item("item-1", price=50.0, quantity=5)
        mock_inventory.get_stock.return_value = 2  # Less than requested 5

        with pytest.raises(InventoryShortageError, match="Not enough stock for item-1"):
            regular_order.checkout()

        mock_inventory.get_stock.assert_called_once_with("item-1")
        mock_payment.charge.assert_not_called()
        mock_inventory.decrement_stock.assert_not_called()
        assert not regular_order.is_paid
        assert regular_order.status == "DRAFT"

    def test_checkout_payment_declined_raises_error(self, regular_order, mock_inventory, mock_payment):
        regular_order.add_item("item-1", price=50.0, quantity=1)
        mock_inventory.get_stock.return_value = 10
        mock_payment.charge.return_value = False  # Payment declined

        with pytest.raises(PaymentFailedError, match="Transaction declined by gateway"):
            regular_order.checkout()

        mock_payment.charge.assert_called_once_with(50.0, "USD")
        mock_inventory.decrement_stock.assert_not_called()
        assert not regular_order.is_paid
        assert regular_order.status == "DRAFT"

    def test_checkout_payment_gateway_exception_wrapped(self, regular_order, mock_inventory, mock_payment):
        regular_order.add_item("item-1", price=50.0, quantity=1)
        mock_inventory.get_stock.return_value = 10
        mock_payment.charge.side_effect = ConnectionError("Network timeout")

        with pytest.raises(PaymentFailedError, match="Payment gateway error: Network timeout"):
            regular_order.checkout()

        mock_payment.charge.assert_called_once_with(50.0, "USD")
        mock_inventory.decrement_stock.assert_not_called()

    def test_checkout_success_regular_customer(self, regular_order, mock_inventory, mock_payment):
        regular_order.add_item("item-1", price=150.0, quantity=1)  # Total 150 -> Discounted to 135.0
        mock_inventory.get_stock.return_value = 5
        mock_payment.charge.return_value = True

        result = regular_order.checkout()

        # Assertions
        mock_inventory.get_stock.assert_called_once_with("item-1")
        mock_payment.charge.assert_called_once_with(135.0, "USD")
        mock_inventory.decrement_stock.assert_called_once_with("item-1", 1)
        
        assert regular_order.is_paid is True
        assert regular_order.status == "COMPLETED"
        assert result == {"status": "success", "charged_amount": 135.0}

    def test_checkout_success_vip_customer(self, vip_order, mock_inventory, mock_payment):
        vip_order.add_item("item-1", price=100.0, quantity=2)  # Total 200 -> VIP 20% off = 160.0
        mock_inventory.get_stock.return_value = 10
        mock_payment.charge.return_value = True

        result = vip_order.checkout()

        mock_payment.charge.assert_called_once_with(160.0, "USD")
        mock_inventory.decrement_stock.assert_called_once_with("item-1", 2)
        assert vip_order.is_paid is True
        assert vip_order.status == "COMPLETED"
        assert result == {"status": "success", "charged_amount": 160.0}

    def test_checkout_multiple_items_stock_and_payment_flow(self, regular_order, mock_inventory, mock_payment):
        regular_order.add_item("item-1", price=30.0, quantity=1)
        regular_order.add_item("item-2", price=20.0, quantity=2)  # Total: 30 + 40 = 70.0
        
        # Stock lookup mapping for different items
        mock_inventory.get_stock.side_effect = lambda prod_id: {"item-1": 5, "item-2": 10}[prod_id]
        mock_payment.charge.return_value = True

        result = regular_order.checkout()

        # Verify inventory get_stock calls
        mock_inventory.get_stock.assert_has_calls([call("item-1"), call("item-2")], any_order=False)
        mock_payment.charge.assert_called_once_with(70.0, "USD")
        
        # Verify inventory decrement calls after successful payment
        mock_inventory.decrement_stock.assert_has_calls([call("item-1", 1), call("item-2", 2)], any_order=False)
        
        assert result == {"status": "success", "charged_amount": 70.0}
