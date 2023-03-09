import pytest
from tests.test_fixures import (
    set_date_util,
    set_option_up_out_auto_call,
    set_option_up_out_down_out,
)
from snow_ball.option.option_up_out_auto_call import OptionUpOutAutoCall
from snow_ball.option.option_up_out_down_out import OptionUpOutDownOut


class TestOptionUpOutAutoCall:
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
        # end boundary
        assert set_option_up_out_auto_call.continuation_value(240, 2) > 1
        assert set_option_up_out_auto_call.continuation_value(240, 1) == 0
        assert set_option_up_out_auto_call.continuation_value(240, 0.5) == 0

        # upper boundary
        assert set_option_up_out_auto_call.continuation_value(0, 3) > 1
        assert set_option_up_out_auto_call.continuation_value(100, 3) > 1
        assert set_option_up_out_auto_call.continuation_value(200, 3) > 1

        # lower boundary
        assert set_option_up_out_auto_call.continuation_value(0, 0) == 0
        assert set_option_up_out_auto_call.continuation_value(100, 0) == 0
        assert set_option_up_out_auto_call.continuation_value(200, 0) == 0

        # continuation
        assert set_option_up_out_auto_call.continuation_value(0.1, 1) == -1
        assert set_option_up_out_auto_call.continuation_value(239, 1) == -1
        assert set_option_up_out_auto_call.continuation_value(239, 2) == -1
        assert set_option_up_out_auto_call.continuation_value(239, 3) > 1
        # knock out at 2019-11-25
        assert set_option_up_out_auto_call.continuation_value(215, 2) > 1
        assert set_option_up_out_auto_call.continuation_value(215, 0) == 0
        assert set_option_up_out_auto_call.continuation_value(
            220, 3
        ) < set_option_up_out_auto_call.continuation_value(239, 3)


class TestOptionUpOutDownOut:
    def test_continuation_value(self, set_option_up_out_down_out: OptionUpOutDownOut):
        # end boundary
        assert set_option_up_out_down_out.continuation_value(240, 1) > 1
        assert set_option_up_out_down_out.continuation_value(240, 1.05) == 0
        assert set_option_up_out_down_out.continuation_value(240, 0.68 - 1e-6) == 0

        # upper boundary
        assert set_option_up_out_down_out.continuation_value(100, 3) == 0
        assert set_option_up_out_down_out.continuation_value(200, 3) == 0
        assert set_option_up_out_down_out.continuation_value(0, 3) == 0

        # lower boundary
        assert set_option_up_out_down_out.continuation_value(100, 0) == 0
        assert set_option_up_out_down_out.continuation_value(200, 0) == 0
        assert set_option_up_out_down_out.continuation_value(0, 0) == 0

        # continuation
        assert set_option_up_out_down_out.continuation_value(215, 2) == 0
        assert set_option_up_out_down_out.continuation_value(213, 2) == -1
        assert set_option_up_out_down_out.continuation_value(215, 0.5) == 0
        assert set_option_up_out_down_out.continuation_value(213, 0.5) == 0
