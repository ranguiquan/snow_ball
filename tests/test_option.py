import pytest
from tests.test_fixures import set_option_up_out_auto_call, set_date_util
from snow_ball.option.option_up_out_auto_call import OptionUpOutAutoCall


class TestOptionUpOutAutoCall:
    rf_daily = 0.035 / 365

    def test_payoff(self, set_option_up_out_auto_call: OptionUpOutAutoCall):
        assert (
            abs(
                set_option_up_out_auto_call.payoff(240)
                - float(1 + set_option_up_out_auto_call.R * 357 / 365)
            )
            < 1e-6
        )

        assert (set_option_up_out_auto_call.payoff(0.5) - 1) < 1e-6
        with pytest.raises(ValueError):
            set_option_up_out_auto_call.payoff(-1)
        with pytest.raises(ValueError):
            set_option_up_out_auto_call.payoff(240.1)
        with pytest.raises(ValueError):
            set_option_up_out_auto_call.payoff(241)

    def test_continuation_value(self, set_option_up_out_auto_call: OptionUpOutAutoCall):
        assert set_option_up_out_auto_call.continuation_value(0.1, 1) == -1
        assert set_option_up_out_auto_call.continuation_value(240, 2) > 1
        assert set_option_up_out_auto_call.continuation_value(240, 1) == 0
        assert set_option_up_out_auto_call.continuation_value(239, 1) == -1
        assert set_option_up_out_auto_call.continuation_value(239, 2) == -1
        assert set_option_up_out_auto_call.continuation_value(239, 3) > 1
        # know out at 2019-11-25
        assert set_option_up_out_auto_call.continuation_value(215, 2) > 1
        assert set_option_up_out_auto_call.continuation_value(215, 0) == 0
        assert set_option_up_out_auto_call.continuation_value(
            220, 3
        ) < set_option_up_out_auto_call.continuation_value(239, 3)
