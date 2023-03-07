import datetime
import pytest

from snow_ball.date_util import DateUtil, OptionDateCollection
from snow_ball.option import OptionAfterUpOut


@pytest.fixture
def set_date_util():
    """default DateUtil Object"""
    T0 = datetime.datetime(2019, 1, 3)
    T_start = datetime.datetime(2019, 1, 4)
    T_right = datetime.datetime(2020, 1, 2)
    Tn = datetime.datetime(2019, 12, 27)
    return DateUtil(OptionDateCollection(T0, T_start, Tn, T_right))


@pytest.fixture
def set_option_after_up_out(set_date_util):
    """default OptionAfterUpOut Object"""
    return OptionAfterUpOut(0.28, set_date_util)