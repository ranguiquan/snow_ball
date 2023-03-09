from snow_ball.date_util import DateUtil


class OptionUpOutDownOut:
    def __init__(
        self,
        R: float,
        date_util: DateUtil,
        rf: float,
        up_barrier: float,
        down_barrier: float,
        Smax: float,
    ) -> None:
        self.R = R
        self.date_util = date_util
        self.rf = rf
        self.rf_daily = rf / 365
        self.up_barrier = up_barrier
        self.down_barrier = down_barrier
        self.Smax = Smax
        # never knock out, realize at the end
        pay = 1 + self.R * 357 / 365
        days_gap = (
            date_util.option_date_collection.after_end_date
            - date_util.option_date_collection.end_date
        )
        days_gap = days_gap.days
        self.never_out_value = pay / (1 + days_gap * self.rf_daily)

    def up_out_value(self, t: float):
        knock_out_time = -1
        while t <= self.date_util.option_time_collection.end_time:
            if self.date_util.is_time_t_up_out_monitoring(t):
                knock_out_time = t
                break
            t += 1
        if knock_out_time == -1:
            # never knock out cause no monitoring time in the future.
            return self.never_out_value
        # out and pay 0
        return 0

    def down_out_value(self, t: float):
        knock_out_time = -1
        while t <= self.date_util.option_time_collection.end_time:
            if self.date_util.is_time_t_down_in_monitoring(t):
                knock_out_time = t
                break
            t += 1
        if knock_out_time == -1:
            # never knock out cause no monitoring time in the future.
            return self.never_out_value
        # out and pay 0
        return 0

    def continuation_value(self, t: float, S: float) -> float:
        date_util = self.date_util
        if t == date_util.option_time_collection.end_time:
            # end boundary
            if S >= self.up_barrier:
                return self.up_out_value(t)
            if S < self.down_barrier:
                return self.down_out_value(t)
            return self.never_out_value
        if S == 0:
            # lower boundary
            # surely knock out ont the next monitoring date
            return self.down_out_value(t)
        if S == self.Smax:
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