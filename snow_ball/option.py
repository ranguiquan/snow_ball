"""Option related class
"""
from snow_ball.date_util import DateUtil


class OptionAfterUpOut:
    """OptionAfterUpOut

    option after the original up and out
    """

    def __init__(self, R: float, date_util: DateUtil) -> None:
        self.R = R
        self.date_util = date_util

    def payoff(self, t: float) -> float:
        """get payoff at time t

        Args:
            t (float): time (trading calendar scenario)

        Raises:
            ValueError: t beyond range

        Returns:
            float: payment. it happens at next trading date
        """
        if (
            t <= self.date_util.option_time_collection.valuation_time
            or t > self.date_util.option_time_collection.end_time
        ):
            raise ValueError(f"invalid t: {t}")
        tout = self.date_util.get_tout_from_t(t)
        return 1 + self.R * (tout / 365)

    def value_at_node(self, t: float, rf_daily: float):
        """get option value at time t

        Args:
            t (float): time (trading calendar scenario)
            rf_daily (float): risk free rate (daily, natural calendar scenario)

        Returns:
            _type_: option value at time t
        """
        paid_at_next_trade_day = self.payoff(t)
        date_next_trade_day = self.date_util.get_date_from_t(t + 1)
        date_today = self.date_util.get_date_from_t(t)
        days_gap = (date_next_trade_day - date_today).days
        return paid_at_next_trade_day / (1 + days_gap * rf_daily)


class OptionAfterDownIn:
    """OptionAfterDownIn

    option after the original down and in
    """

    def __init__(self, date_util: DateUtil) -> None:
        self.date_util = date_util
        self.expiry = self.date_util.option_time_collection.end_time

    def payoff(self, S: float, S0: float) -> float:
        """option payoff at expiry

        Args:
            S (float): underlying close at expiry
            S0 (float): underlying close at valuation date

        Returns:
            float: option actual return at expiry
        """
        if S < 0:
            raise ValueError("S no less than 0.")
        if S0 <= 0:
            raise ValueError("S0 must bigger than 0.")
        return min(1, S / S0)

    def value_at_node(self, t: float, S: float, S0: float, continuation: float = None):
        """option value at node

        Args:
            t (float): time (trading calendar scenario)
            S (float): underlying price at `t`
            S0 (float): underlying close at valuation date
            continuation (float): upstream option price got from pricer

        Returns:
            _type_: option price at time `t` with underlying price `S`
        """
        if t > self.expiry:
            raise ValueError(f"t value error. biggest {self.expiry}, got {t}")
        if t == self.expiry:
            return self.payoff(S, S0)
        return continuation


class OptionBarrier:
    def __init__(
        self,
        R: float,
        date_util: DateUtil,
        up_barrier: float,
        down_barrier: float,
        up_option: OptionAfterUpOut,
        down_option: OptionAfterDownIn,
    ) -> None:
        self.date_util = date_util
        self.R = R
        self.up_barrier = up_barrier
        self.down_barrier = down_barrier
        self.up_option = up_option
        self.down_option = down_option

        self.expiry = self.date_util.option_time_collection.end_time

    def payoff(self):
        """option pay off at expiry

        Returns:
            _type_: _description_
        """
        natural_days = (
            self.date_util.option_date_collection.end_date
            - self.date_util.option_date_collection.start_date
        ).days
        return 1 + self.R * natural_days / 365

    def value_at_node(
        self,
        t: float,
        S: float,
        rf_daily: float,
        down_in_value_at_node: float,
        continuation: float = None,
    ):
        if S >= self.up_barrier and self.date_util.is_time_t_up_out_monitoring(t):
            return self.up_option.value_at_node(t, rf_daily)
        if S < self.down_barrier and self.date_util.is_time_t_down_in_monitoring(t):
            return down_in_value_at_node
        if t == self.expiry:
            return self.payoff()
        return continuation
