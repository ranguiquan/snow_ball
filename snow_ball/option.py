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
