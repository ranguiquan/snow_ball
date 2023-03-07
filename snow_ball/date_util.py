import datetime
import math
import pandas as pd


class DateUtil:
    """date utils for pricing UO_DI_Barrier_Option"""

    def __init__(
        self,
        valuation_date: datetime.datetime,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
        after_end_date: datetime.datetime,
    ) -> None:
        """set up date information

        Args:
            valuation_date (datetime.datetime): valuation date.
            start_date (datetime.datetime): transaction start date.
            end_date (datetime.datetime): transaction end date.
            after_end_date (datetime.datetime): next trading date after ends.
        """
        self.valuation_date = valuation_date
        self.start_date = start_date
        self.end_date = end_date
        self.after_end_date = after_end_date
        date_sheet = (
            pd.read_csv("./data/Project2 business_day.csv", index_col=0)
            .astype("datetime64[ns]")
            .query("date >= @valuation_date and date <= @after_end_date")
            .reset_index(drop=True)
        )
        down_in_monitoring_day = date_sheet.loc[1 : len(date_sheet) - 2, :]
        up_out_monitoring_day = pd.read_csv("./data/UO_monitoring_day.csv").astype(
            "datetime64[ns]"
        )
        date_sheet["is_UO_monitoring"] = date_sheet["date"].isin(
            up_out_monitoring_day["UO_monitoring_day"]
        )
        date_sheet["is_DI_monitoring"] = date_sheet["date"].isin(
            down_in_monitoring_day["date"]
        )
        self.date_sheet = date_sheet
        self.t_valuation = 0
        self.t_start = 1
        self.t_end = date_sheet.index.max() - 1
        self.t_after_end = date_sheet.index.max()

    def get_date_from_t(self, t: float) -> datetime.datetime:
        """get the actual date from the numerical time space

        Args:
            t (float): numerical time.

        Raises:
            ValueError: t must satisfy the trading range.

        Returns:
            datetime.datetime: the actual date at t.
        """
        if t < self.t_valuation or t > self.t_after_end:
            raise ValueError(
                f"[t] must be between {self.t_valuation} and no bigger than {self.t_after_end}: {t}"
            )
        t = math.ceil(t)
        return self.date_sheet.loc[t, "date"]

    def get_tout_from_t(self, t: float) -> int:
        """get the date gap between option start date and t time.

        Args:
            t (float): numerical time.

        Returns:
            int: the date gap
        """
        return (
            self.get_date_from_t(t) - self.date_sheet.loc[self.t_start, "date"]
        ).days
