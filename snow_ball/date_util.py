"""
Date related classed
"""
from dataclasses import dataclass
import datetime
import math
import pandas as pd


@dataclass
class OptionDateCollection:
    """date information of option."""

    valuation_date: datetime.datetime
    start_date: datetime.datetime
    end_date: datetime.datetime
    after_end_date: datetime.datetime


@dataclass
class OptionTimeCollection:
    """time information of option."""

    valuation_time: int
    start_time: int
    end_time: int
    after_end_time: int


class DateUtil:
    """date utils for pricing UO_DI_Barrier_Option"""

    def __init__(self, option_date_collection: OptionDateCollection) -> None:
        """set up date information

        Args:
            option_date_collection (OptionDateCollection): date information of option.
        """
        self.option_date_collection = option_date_collection
        date_sheet = (
            pd.read_csv("./data/Project2 business_day.csv", index_col=0)
            .astype("datetime64[ns]")
            .query(
                "date >= @option_date_collection.valuation_date and date <= @option_date_collection.after_end_date"
            )
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
        self.option_time_collection = OptionTimeCollection(
            0, 1, date_sheet.index.max() - 1, date_sheet.index.max()
        )
        self.up_out_monitoring_time_set = set(
            date_sheet[date_sheet["is_UO_monitoring"] == True].index.unique()
        )
        self.down_in_monitoring_time_set = set(
            date_sheet[date_sheet["is_DI_monitoring"] == True].index.unique()
        )

    def get_date_from_t(self, time: float) -> datetime.datetime:
        """get the actual date from the numerical time space

        Args:
            time (float): numerical time.

            1 means the end of the day 1.

            1.5 means in the middle of the day 2. (trading date)

        Raises:
            ValueError: t must satisfy the trading range.

        Returns:
            datetime.datetime: the actual date at t.
        """
        if (
            time < self.option_time_collection.valuation_time
            or time > self.option_time_collection.after_end_time
        ):
            raise ValueError(
                f"[t] must be between {self.option_time_collection.valuation_time}"
                f"and no bigger than {self.option_time_collection.after_end_time}: "
                f"{time}"
            )
        time = math.ceil(time)
        return self.date_sheet.loc[time, "date"]

    def get_tout_from_t(self, time: float) -> int:
        """get the date gap between option start date and t time.

        Args:
            time (float): numerical time.

            1 means the end of the day 1.

            1.5 means in the middle of the day 2. (trading date)

        Returns:
            int: the date gap
        """
        return (
            self.get_date_from_t(time)
            - self.date_sheet.loc[self.option_time_collection.start_time, "date"]
        ).days

    def is_time_t_up_out_monitoring(self, t: float) -> bool:
        """is time t under up and out monitoring

        Args:
            t (float): time t (trading calendar scenario)

        Returns:
            bool:
        """
        t = math.ceil(t)
        return t in self.up_out_monitoring_time_set

    def is_time_t_down_in_monitoring(self, t: float):
        """is time t under down and in monitoring

        Args:
            t (float): time t (trading calendar scenario)

        Returns:
            _type_:
        """
        t = math.ceil(t)
        return t in self.down_in_monitoring_time_set
