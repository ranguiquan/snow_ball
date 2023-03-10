import pytest
from tests.test_fixures import (
    down_barrier,
    rf,
    S0,
    set_date_util,
    set_option_up_out_auto_call,
    set_option_up_out_down_out,
    set_option_up_out_down_out_minimal,
    set_option_up_out_minimal,
    Smax,
    Smin,
    up_barrier,
)
from snow_ball.option.option_up_out_auto_call import OptionUpOutAutoCall
from snow_ball.option.option_up_out_down_out import OptionUpOutDownOut
from snow_ball.option.option_up_out_minimal import OptionUpOutMinimal
from snow_ball.option.option_up_out_down_out_minimal import OptionUpOutDownOutMinimal


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
        assert (
            set_option_up_out_auto_call.continuation_value(240, 2 * S0, S0, Smax, rf)
            > 1
        )
        assert (
            set_option_up_out_auto_call.continuation_value(240, 1 * S0, S0, Smax, rf)
            == 0
        )
        assert (
            set_option_up_out_auto_call.continuation_value(240, 0.5 * S0, S0, Smax, rf)
            == 0
        )

        # upper boundary
        assert set_option_up_out_auto_call.continuation_value(0, Smax, S0, Smax, rf) > 1
        assert (
            set_option_up_out_auto_call.continuation_value(100, Smax, S0, Smax, rf) > 1
        )
        assert (
            set_option_up_out_auto_call.continuation_value(200, Smax, S0, Smax, rf) > 1
        )

        # lower boundary
        assert (
            set_option_up_out_auto_call.continuation_value(0, Smin, S0, Smax, rf) == 0
        )
        assert (
            set_option_up_out_auto_call.continuation_value(100, Smin, S0, Smax, rf) == 0
        )
        assert (
            set_option_up_out_auto_call.continuation_value(200, Smin, S0, Smax, rf) == 0
        )

        # continuation
        assert (
            set_option_up_out_auto_call.continuation_value(0.1, 1 * S0, S0, Smax, rf)
            == -1
        )
        assert (
            set_option_up_out_auto_call.continuation_value(239, 1 * S0, S0, Smax, rf)
            == -1
        )
        assert (
            set_option_up_out_auto_call.continuation_value(239, 2 * S0, S0, Smax, rf)
            == -1
        )
        assert (
            set_option_up_out_auto_call.continuation_value(239, 3 * S0, S0, Smax, rf)
            > 1
        )
        # knock out at 2019-11-25
        assert (
            set_option_up_out_auto_call.continuation_value(
                215, up_barrier, S0, Smax, rf
            )
            > 1
        )
        assert set_option_up_out_auto_call.continuation_value(215, 0, S0, Smax, rf) == 0
        assert set_option_up_out_auto_call.continuation_value(
            220, Smax, S0, Smax, rf
        ) < set_option_up_out_auto_call.continuation_value(239, Smax, S0, Smax, rf)


class TestOptionUpOutDownOut:
    def test_continuation_value(self, set_option_up_out_down_out: OptionUpOutDownOut):
        # end boundary
        assert set_option_up_out_down_out.continuation_value(240, S0, S0, Smax, rf) > 1
        assert (
            set_option_up_out_down_out.continuation_value(240, Smax, S0, Smax, rf) == 0
        )
        assert (
            set_option_up_out_down_out.continuation_value(
                240, down_barrier - 1e-6, S0, Smax, rf
            )
            == 0
        )

        # upper boundary
        assert set_option_up_out_down_out.continuation_value(0, Smax, S0, Smax, rf) == 0
        assert (
            set_option_up_out_down_out.continuation_value(100, Smax, S0, Smax, rf) == 0
        )
        assert (
            set_option_up_out_down_out.continuation_value(200, Smax, S0, Smax, rf) == 0
        )

        # lower boundary
        assert set_option_up_out_down_out.continuation_value(0, Smin, S0, Smax, rf) == 0
        assert (
            set_option_up_out_down_out.continuation_value(100, Smin, S0, Smax, rf) == 0
        )
        assert (
            set_option_up_out_down_out.continuation_value(200, Smin, S0, Smax, rf) == 0
        )

        # continuation
        assert (
            set_option_up_out_down_out.continuation_value(215, 2 * S0, S0, Smax, rf)
            == 0
        )
        assert (
            set_option_up_out_down_out.continuation_value(213, 2 * S0, S0, Smax, rf)
            == -1
        )
        assert (
            set_option_up_out_down_out.continuation_value(215, 0.5 * S0, S0, Smax, rf)
            == 0
        )
        assert (
            set_option_up_out_down_out.continuation_value(213, 0.5 * S0, S0, Smax, rf)
            == 0
        )


class TestOptionUpOutMinimal:
    def test_continuation_value(self, set_option_up_out_minimal: OptionUpOutMinimal):
        # end boundary
        assert set_option_up_out_minimal.continuation_value(240, S0, S0, Smax, rf) <= 1
        assert (
            set_option_up_out_minimal.continuation_value(240, S0 * 0.5, S0, Smax, rf)
            <= 0.5
        )
        assert (
            set_option_up_out_minimal.continuation_value(240, S0 * 1.03, S0, Smax, rf)
            <= 1
        )
        assert (
            set_option_up_out_minimal.continuation_value(240, S0 * 1.03, S0, Smax, rf)
            > 0.9
        )
        assert set_option_up_out_minimal.continuation_value(240, 0, S0, Smax, rf) == 0

        # upper boundary
        assert set_option_up_out_minimal.continuation_value(0, Smax, S0, Smax, rf) == 0
        assert (
            set_option_up_out_minimal.continuation_value(100, Smax, S0, Smax, rf) == 0
        )
        assert (
            set_option_up_out_minimal.continuation_value(200, Smax, S0, Smax, rf) == 0
        )

        # lower boundary
        assert set_option_up_out_minimal.continuation_value(0, Smin, S0, Smax, rf) == 0
        assert (
            set_option_up_out_minimal.continuation_value(100, Smin, S0, Smax, rf) == 0
        )
        assert (
            set_option_up_out_minimal.continuation_value(200, Smin, S0, Smax, rf) == 0
        )

        # continuation
        assert (
            set_option_up_out_minimal.continuation_value(215, up_barrier, S0, Smax, rf)
            == 0
        )
        assert (
            set_option_up_out_minimal.continuation_value(213, 2 * S0, S0, Smax, rf)
            == -1
        )
        assert (
            set_option_up_out_minimal.continuation_value(215, 0.5 * S0, S0, Smax, rf)
            == -1
        )
        assert (
            set_option_up_out_minimal.continuation_value(213, 0.5 * S0, S0, Smax, rf)
            == -1
        )


class TestOptionUpOutDownOutMinimal:
    def test_continuation_value(
        self, set_option_up_out_down_out_minimal: OptionUpOutDownOutMinimal
    ):
        # end boundary
        assert (
            set_option_up_out_down_out_minimal.continuation_value(240, S0, S0, Smax, rf)
            <= 1
        )
        assert (
            set_option_up_out_down_out_minimal.continuation_value(
                240, S0 * 0.5, S0, Smax, rf
            )
            <= 0.5
        )
        assert (
            set_option_up_out_down_out_minimal.continuation_value(
                240, S0 * 1.03, S0, Smax, rf
            )
            <= 1
        )
        assert (
            set_option_up_out_down_out_minimal.continuation_value(
                240, S0 * 1.03, S0, Smax, rf
            )
            > 0.9
        )
        assert (
            set_option_up_out_down_out_minimal.continuation_value(
                240, S0 * 0, S0, Smax, rf
            )
            == 0
        )

        # upper boundary
        assert (
            set_option_up_out_down_out_minimal.continuation_value(0, Smax, S0, Smax, rf)
            == 0
        )
        assert (
            set_option_up_out_down_out_minimal.continuation_value(
                100, Smax, S0, Smax, rf
            )
            == 0
        )
        assert (
            set_option_up_out_down_out_minimal.continuation_value(
                200, Smax, S0, Smax, rf
            )
            == 0
        )

        # lower boundary
        assert (
            set_option_up_out_down_out_minimal.continuation_value(0, Smin, S0, Smax, rf)
            == 0
        )
        assert (
            set_option_up_out_down_out_minimal.continuation_value(
                100, Smin, S0, Smax, rf
            )
            == 0
        )
        assert (
            set_option_up_out_down_out_minimal.continuation_value(
                200, Smin, S0, Smax, rf
            )
            == 0
        )

        # continuation

        assert (
            set_option_up_out_down_out_minimal.continuation_value(
                215, up_barrier, S0, Smax, rf
            )
            == 0
        )
        assert (
            set_option_up_out_down_out_minimal.continuation_value(
                213, 2 * S0, S0, Smax, rf
            )
            == -1
        )
        assert (
            set_option_up_out_down_out_minimal.continuation_value(
                215, 0.5 * S0, S0, Smax, rf
            )
            == 0
        )
        assert (
            set_option_up_out_down_out_minimal.continuation_value(
                213, 0.5 * S0, S0, Smax, rf
            )
            == 0
        )
