"""Option related class edited
"""
from snow_ball.date_util import DateUtil


class OptionUpOutAutoCall:
    """OptionUpOutAutoCall

    Up and out auto call option.
    When touching the up barrier, the option gives coupon rate according to survival time.
    """

    def __init__(self, R: float, date_util: DateUtil, up_barrier: float) -> None:
        self.R = R
        self.date_util = date_util
        self.up_barrier = up_barrier

    def payoff(self, t: float) -> float:
        """Get payoff at time t if surely knock out now.

        Args:
            t (float): time (trading calendar scenario)

        Raises:
            ValueError: t beyond range

        Returns:
            float: payment. it happens at next trading date
        """
        if (
            t < self.date_util.option_time_collection.valuation_time
            or t > self.date_util.option_time_collection.end_time
        ):
            raise ValueError(f"invalid t: {t}")
        tout = self.date_util.get_tout_from_t(t)
        return 1 + self.R * (tout / 365)

    def up_out_value(self, t: float, rf: float):
        """Get option value at time t if surely knock out at now or future

        Args:
            t (float): time (trading calendar scenario)

        Returns:
            _type_: option value at time t
        """
        date_today = self.date_util.get_date_from_t(t)
        rf_daily = rf / 365
        knock_out_time = -1
        while t <= self.date_util.option_time_collection.end_time:
            if self.date_util.is_time_t_up_out_monitoring(t):
                knock_out_time = t
                break
            t += 1
        if knock_out_time == -1:
            # never knock out cause no monitoring time in the future.
            return 0
        paid_at_next_trade_day = self.payoff(knock_out_time)
        date_next_trade_day = self.date_util.get_date_from_t(knock_out_time + 1)
        days_gap = (date_next_trade_day - date_today).days
        return paid_at_next_trade_day / (1 + days_gap * rf_daily)

    def continuation_value(self, t: float, S: float, Smax: float, rf: float) -> float:
        """Give continuation value at node if it can be inferred from `t` and `S`

        Args:
            t (float): time
            S (float): underlying price

        Returns:
            float: -1 means no continuation value, use FDE value instead. Otherwise use the continuation value
        """
        date_util = self.date_util
        if t == date_util.option_time_collection.end_time:
            # end boundary
            if S >= self.up_barrier:
                return self.up_out_value(t, rf)
            return 0
        if S == 0:
            # lower boundary
            # not likely to knock out
            return 0
        if S == Smax:
            # upper boundary
            # surely knock out ont the next monitoring date
            return self.up_out_value(t, rf)
        if date_util.is_time_t_up_out_monitoring(t) and S >= self.up_barrier:
            # knock out now
            return self.up_out_value(t, rf)
        # can't infer continuation value, use FDE value instead.
        return -1
