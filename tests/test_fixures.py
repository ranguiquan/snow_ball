import datetime
import pytest

from snow_ball.date_util import DateUtil, OptionDateCollection
from snow_ball.option.option_up_out_auto_call import OptionUpOutAutoCall

S0 = 5.1
up_barrier = S0 * 1.05
down_barrier = S0 * 0.68


@pytest.fixture
def set_date_util():
    """default DateUtil Object"""
    T0 = datetime.datetime(2019, 1, 3)
    T_start = datetime.datetime(2019, 1, 4)
    T_right = datetime.datetime(2020, 1, 2)
    Tn = datetime.datetime(2019, 12, 27)
    return DateUtil(OptionDateCollection(T0, T_start, Tn, T_right))


@pytest.fixture
def set_option_up_out_auto_call(set_date_util):
    """default OptionAfterUpOut Object"""
    return OptionUpOutAutoCall(0.28, set_date_util, 0.035, 1.05, 3)
