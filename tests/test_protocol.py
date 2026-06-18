from mt5.protocol import AccountInfo, DealInfo, MT5Adapter, OrderResult, PositionInfo


class TestMT5AdapterProtocol:
    def test_is_protocol(self):
        assert hasattr(MT5Adapter, "__instancecheck__")

    def test_protocol_methods_signatures(self):
        expected_methods = [
            "initialize",
            "login",
            "shutdown",
            "get_account_info",
            "get_symbol_info",
            "get_rates",
            "get_positions",
            "get_orders",
            "send_order",
            "modify_order",
            "modify_position",
            "cancel_order",
            "get_history_deals",
        ]
        for name in expected_methods:
            assert hasattr(MT5Adapter, name), f"Missing method: {name}"
            method = getattr(MT5Adapter, name)
            assert callable(method), f"{name} is not callable"


class TestSharedTypes:
    def test_account_info_fields(self):
        info = AccountInfo(
            balance=10000.0,
            equity=9500.0,
            margin=500.0,
            free_margin=9000.0,
            margin_level=1900.0,
            currency="USD",
            name="Test Account",
            server="TestServer",
            leverage=100,
        )
        assert info.balance == 10000.0
        assert info.equity == 9500.0
        assert info.currency == "USD"

    def test_order_result_fields(self):
        result = OrderResult(ticket=123, filled_volume=1.0, price=1.2345, comment="ok")
        assert result.ticket == 123
        assert result.filled_volume == 1.0

    def test_position_info_fields(self):
        pos = PositionInfo(
            ticket=1,
            symbol="EURUSD",
            volume=0.1,
            type_=0,
            price_open=1.1000,
            sl=0.0,
            tp=0.0,
            profit=25.0,
            swap=-0.5,
            comment="test",
        )
        assert pos.symbol == "EURUSD"
        assert pos.profit == 25.0

    def test_deal_info_fields(self):
        from datetime import datetime
        dt = datetime(2024, 1, 1)
        deal = DealInfo(
            ticket=1,
            symbol="EURUSD",
            volume=0.1,
            type_=0,
            price=1.1000,
            profit=50.0,
            commission=-2.0,
            swap=-0.5,
            open_time=dt,
            close_time=dt,
            comment="test",
        )
        assert deal.symbol == "EURUSD"
        assert deal.profit == 50.0
