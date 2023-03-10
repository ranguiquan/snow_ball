from snow_ball.date_util import DateUtil


class OptionUpOutDownOutMinimal:
    """OptionUpOutDownOutMinimal

    Up out and Down out option with an exotic payoff function.
    When touching the up barrier, the option dies.
    """

    def __init__(
        self,
        R: float,
        date_util: DateUtil,
        up_barrier: float,
        down_barrier: float,
    ) -> None:
        self.R = R
        self.date_util = date_util
        self.up_barrier = up_barrier
        self.down_barrier = down_barrier

    def payoff(self, S: float, S0: float) -> float:
        """Get payoff with S at expiry

        Args:
            S (float): underlying price at expiry

        Returns:
            float: payment. it happens at next trading date
        """
        return min(S / S0, 1)

    def up_out_value(self, t: float):
        """Get option value at time t if surely knock out at now or future

        Args:
            t (float): time (trading calendar scenario)

        Returns:
            _type_: option value at time t
        """
        knock_out_time = -1
        while t <= self.date_util.option_time_collection.end_time:
            if self.date_util.is_time_t_up_out_monitoring(t):
                knock_out_time = t
                break
            t += 1
        if knock_out_time == -1:
            # never knock out cause no monitoring time in the future.
            return -1
        # out and pay 0
        return 0

    def down_out_value(self, t: float):
        """Get option value at time t if surely knock out at now or future

        Args:
            t (float): time (trading calendar scenario)

        Returns:
            _type_: option value at time t
        """
        knock_out_time = -1
        while t <= self.date_util.option_time_collection.end_time:
            if self.date_util.is_time_t_up_out_monitoring(t):
                knock_out_time = t
                break
            t += 1
        if knock_out_time == -1:
            # never knock out cause no monitoring time in the future.
            return -1
        # out and pay 0
        return 0

    def continuation_value(
        self, t: float, S: float, Smax: float, rf: float, S0: float
    ) -> float:
        """Give continuation value at node if it can be inferred from `t` and `S`

        Args:
            t (float): time
            S (float): underlying price

        Returns:
            float: -1 means no continuation value, use FDE value instead. Otherwise use the continuation value
        """
        date_util = self.date_util
        rf_daily = rf / 365
        if t == date_util.option_time_collection.end_time:
            # end boundary
            if S >= self.up_barrier:
                # might knock out
                return self.up_out_value(t)
            days_gap = (
                date_util.option_date_collection.after_end_date
                - date_util.option_date_collection.end_date
            )
            days_gap = days_gap.days
            return self.payoff(S, S0) / (1 + days_gap * rf_daily)
        if S == 0:
            # lower boundary
            # surely knock out ont the next monitoring date
            return self.down_out_value(t)
        if S == Smax:
            # upper boundary
            # surely knock out ont the next monitoring date
            return self.up_out_value(t)
        if date_util.is_time_t_up_out_monitoring(t) and S >= self.up_barrier:
            # up and knock out now
            return self.up_out_value(t)
        if date_util.is_time_t_down_in_monitoring(t) and S < self.down_barrier:
            # down and knock out now
            return self.down_out_value(t)
        # can't infer continuation value, use FDE value instead.
        return -1
