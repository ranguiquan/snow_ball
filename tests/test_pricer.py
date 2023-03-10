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
    def test_price_option_fdm_cn_bs(
        self,
        set_pricer: SnowBallPricer,
        set_option_up_out_auto_call: OptionUpOutAutoCall,
        set_option_up_out_down_out_minimal: OptionUpOutDownOutMinimal,
        set_option_up_out_down_out: OptionUpOutDownOut,
        set_option_up_out_minimal: OptionUpOutMinimal,
    ):
        # np.savetxt('OptionUpOutAutoCall.csv', set_pricer.price_option_fdm_cn_bs(set_option_up_out_auto_call), delimiter=",")
        # np.savetxt('OptionUpOutDownOutMinimal.csv', set_pricer.price_option_fdm_cn_bs(set_option_up_out_down_out_minimal), delimiter=",")
        # np.savetxt('OptionUpOutDownOut.csv', set_pricer.price_option_fdm_cn_bs(set_option_up_out_down_out), delimiter=",")
        # np.savetxt('OptionUpOutMinimal.csv', set_pricer.price_option_fdm_cn_bs(set_option_up_out_minimal), delimiter=",")
        # price_OptionUpOutAutoCall = set_pricer.price_option_fdm_cn_bs(
        #     set_option_up_out_auto_call
        # )
        # price_OptionUpOutDownOutMinimal = set_pricer.price_option_fdm_cn_bs(
        #     set_option_up_out_down_out_minimal
        # )
        # price_OptionUpOutDownOut = set_pricer.price_option_fdm_cn_bs(
        #     set_option_up_out_down_out
        # )
        # price_OptionUpOutMinimal = set_pricer.price_option_fdm_cn_bs(
        #     set_option_up_out_minimal
        # )
        # # assert price_OptionUpOutAutoCall + price_OptionUpOutDownOut + price_OptionUpOutMinimal - price_OptionUpOutDownOutMinimal == 1
        # assert (
        #     float(
        #         price_OptionUpOutAutoCall
        #         + price_OptionUpOutDownOut
        #         + price_OptionUpOutMinimal
        #         - price_OptionUpOutDownOutMinimal
        #     )
        #     == 1
        # )
        pass
