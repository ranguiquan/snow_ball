import pytest

from snow_ball.option import OptionAfterUpOut
from .test_fixures import set_option_after_up_out, set_date_util


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
