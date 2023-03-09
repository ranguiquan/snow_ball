from snow_ball.date_util import DateUtil


class OptionUpOutMinimal:
    def __init__(
        self,
        R: float,
        S0: float,
        date_util: DateUtil,
        rf: float,
        up_barrier: float,
        Smax: float,
    ) -> None:
        self.R = R
        self.S0 = S0
        self.date_util = date_util
        self.rf = rf
        self.rf_daily = rf / 365
        self.up_barrier = up_barrier
        self.Smax = Smax
        # never knock out, realize at the end
        pay = 1 + self.R * 357 / 365
        days_gap = (
            date_util.option_date_collection.after_end_date
            - date_util.option_date_collection.end_date
        )
        days_gap = days_gap.days
        self.never_out_value = pay / (1 + days_gap * self.rf_daily)

    def payoff(self, S: float) -> float:
        """Get payoff with S at expiry

        Args:
            S (float): underlying price at expiry

        Returns:
            float: payment. it happens at next trading date
        """
        return min(S / self.S0, 1)

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

    def continuation_value(self, t: float, S: float) -> float:
        date_util = self.date_util
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
            return self.payoff(S) / (1 + days_gap * self.rf_daily)
        if S == 0:
            # lower boundary
            # option never knock out, but worthless
            return 0
        if S == self.Smax:
            # upper boundary
            # surely knock out ont the next monitoring date
            return self.up_out_value(t)
        if date_util.is_time_t_up_out_monitoring(t) and S >= self.up_barrier:
            # up and knock out now
            return self.up_out_value(t)
        # can't infer continuation value, use FDE value instead.
        return -1
