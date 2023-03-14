from snow_ball.date_util import DateUtil
from snow_ball.option.option import Option
import math


class OptionMinimal(Option):
    """OptionUpOutMinimal

    Up and out option with an exotic payoff function.
    When touching the up barrier, the option dies.
    """

    def __init__(
        self,
        R: float,
        date_util: DateUtil,
    ) -> None:
        self.R = R
        self.date_util = date_util

    def payoff(self, S: float, S0: float) -> float:
        """Get payoff with S at expiry

        Args:
            S (float): underlying price at expiry

        Returns:
            float: payment. it happens at next trading date
        """
        return min(S / S0, 1)

    def continuation_value(
        self, t: float, S: float, S0: float, Smax: float, rf: float
    ) -> float:
        """Give continuation value at node if it can be inferred from `t` and `S`

        Args:
            t (float): time
            S (float): underlying price

        Returns:
            float: -1 means no continuation value, use FDE value instead. Otherwise use the continuation value
        """
        rf_daily = math.pow(1 + rf, 1 / 365) - 1
        t = math.ceil(t)
        date_util = self.date_util
        if t == date_util.option_time_collection.end_time:
            # end boundary
            days_gap = (
                date_util.option_date_collection.after_end_date
                - date_util.option_date_collection.end_date
            )
            days_gap = days_gap.days
            return self.payoff(S, S0) / (1 + rf_daily) ** days_gap
        if S == 0:
            # lower boundary
            # worthless
            return 0
        if S == Smax:
            # upper boundary
            days_gap = (
                date_util.option_date_collection.after_end_date
                - date_util.get_date_from_t(t)
            )
            days_gap = days_gap.days
            return 1 / (1 + rf_daily) ** days_gap
        # can't infer continuation value, use FDE value instead.
        return -1
