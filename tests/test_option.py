import pytest

from snow_ball.option import OptionAfterDownIn, OptionAfterUpOut, OptionBarrier
from .test_fixures import (
    set_date_util,
    set_option_after_down_in,
    set_option_after_up_out,
    set_option_barrier,
)


class TestOptionAfterUpOut:
    rf_daily = 0.035 / 365

    def test_option_after_up_out_payoff(
        self, set_option_after_up_out: OptionAfterUpOut
    ):
        assert (
            abs(
                set_option_after_up_out.payoff(240)
                - float(1 + set_option_after_up_out.R * 357 / 365)
            )
            < 1e-6
        )

        assert (set_option_after_up_out.payoff(0.5) - 1) < 1e-6
        with pytest.raises(ValueError):
            set_option_after_up_out.payoff(0)
        with pytest.raises(ValueError):
            set_option_after_up_out.payoff(-1)
        with pytest.raises(ValueError):
            set_option_after_up_out.payoff(240.1)
        with pytest.raises(ValueError):
            set_option_after_up_out.payoff(241)

    def test_option_after_up_out_value_at_node(
        self, set_option_after_up_out: OptionAfterUpOut
    ):
        assert (
            not abs(
                set_option_after_up_out.value_at_node(240, self.rf_daily)
                - float(1 + set_option_after_up_out.R * 357 / 365)
            )
            < 1e-6
        )

        assert set_option_after_up_out.value_at_node(0.1, self.rf_daily) < 1
        assert set_option_after_up_out.value_at_node(0.1, self.rf_daily) > 0.99


class TestOptionAfterDownIn:
    def test_option_after_down_in_payoff(
        self, set_option_after_down_in: OptionAfterDownIn
    ):
        assert set_option_after_down_in.payoff(0, 100) == 0
        assert set_option_after_down_in.payoff(90, 100) == 0.9
        assert set_option_after_down_in.payoff(3, 1) == 1
        with pytest.raises(ValueError):
            set_option_after_down_in.payoff(1, 0)
        with pytest.raises(ValueError):
            set_option_after_down_in.payoff(-1, 0)
        with pytest.raises(ValueError):
            set_option_after_down_in.payoff(0, -1)
        with pytest.raises(ValueError):
            set_option_after_down_in.payoff(-1, -1)
        with pytest.raises(ValueError):
            set_option_after_down_in.payoff(0, 0)

    def test_option_after_down_in_value_at_node(
        self, set_option_after_down_in: OptionAfterDownIn
    ):
        assert set_option_after_down_in.value_at_node(240, 2, 1) == 1
        assert set_option_after_down_in.value_at_node(240, 0.5, 1) == 0.5
        with pytest.raises(ValueError):
            set_option_after_down_in.value_at_node(241, 1, 1)


class TestOptionBarrier:
    # need to add more test cases
    rf_daily = 0.035 / 365

    def test_option_barrier_payoff(self, set_option_barrier: OptionBarrier):
        assert set_option_barrier.payoff() == 1 + 0.28 * 357 / 365

    def test_option_barrier_value_at_node(self, set_option_barrier: OptionBarrier):
        assert (
            set_option_barrier.value_at_node(240, 5.1, self.rf_daily, 1)
            == 1 + 0.28 * 357 / 365
        )
