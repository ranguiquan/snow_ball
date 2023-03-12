import numpy
from tests.test_fixures import (
    set_date_util,
    set_option_up_out_auto_call,
    set_option_up_out_down_out,
    set_option_up_out_down_out_minimal,
    set_option_up_out_minimal,
    set_pricer,
    set_snow_ball,
)
from snow_ball.pricer import SnowBallPricer
from snow_ball.option.option_up_out_auto_call import OptionUpOutAutoCall
from snow_ball.option.option_up_out_down_out_minimal import OptionUpOutDownOutMinimal
from snow_ball.option.option_up_out_down_out import OptionUpOutDownOut
from snow_ball.option.option_up_out_minimal import OptionUpOutMinimal
import numpy as np


class TestSnowBallPricer:
    def test_get_snow_ball_price(
        self,
        set_pricer: SnowBallPricer,
    ):
        assert set_pricer.get_snow_ball_price()[0] <= 1

    def test_get_delta(self, set_pricer: SnowBallPricer):
        assert set_pricer.get_delta(1.02, 5) <= 1
