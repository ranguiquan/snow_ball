from snow_ball.option.option_up_out_auto_call import OptionUpOutAutoCall
from snow_ball.date_util import DateUtil
from snow_ball.option.option_up_out_down_out import OptionUpOutDownOut
from snow_ball.option.option_up_out_down_out_minimal import OptionUpOutDownOutMinimal
from snow_ball.option.option_up_out_minimal import OptionUpOutMinimal


class OptionSnowBall:
    def __init__(
        self, R: float, up_barrier: float, down_barrier: float, date_util: DateUtil
    ):
        self.up_out_auto_call = OptionUpOutAutoCall(R, date_util, up_barrier)
        self.up_out_down_out_minimal = OptionUpOutDownOutMinimal(
            R, date_util, up_barrier, down_barrier
        )
        self.up_out_down_out = OptionUpOutDownOut(
            R, date_util, up_barrier, down_barrier
        )
        self.up_out_minimal = OptionUpOutMinimal(R, date_util, up_barrier)
