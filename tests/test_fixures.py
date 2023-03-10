import datetime
import pytest

from snow_ball.date_util import DateUtil, OptionDateCollection
from snow_ball.option.option_up_out_down_out import OptionUpOutDownOut
from snow_ball.option.option_up_out_auto_call import OptionUpOutAutoCall
from snow_ball.option.option_up_out_minimal import OptionUpOutMinimal
from snow_ball.option.option_up_out_down_out_minimal import OptionUpOutDownOutMinimal

S0 = 5.1
up_barrier = S0 * 1.05
down_barrier = S0 * 0.68
R = 0.28
rf = 0.035
Smax = S0 * 3
Smin = 0


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
    """default OptionUpOutAutoCall Object"""
    return OptionUpOutAutoCall(R, set_date_util, up_barrier)


@pytest.fixture
def set_option_up_out_down_out(set_date_util):
    """default OptionUpOutDownOut Object"""
    return OptionUpOutDownOut(R, set_date_util, up_barrier, down_barrier)


@pytest.fixture
def set_option_up_out_minimal(set_date_util):
    """default OptionUpOutMinimal Object"""
    return OptionUpOutMinimal(R, set_date_util, up_barrier)


@pytest.fixture
def set_option_up_out_down_out_minimal(set_date_util):
    """default OptionUpOutDownOutMinimal Object"""
    return OptionUpOutDownOutMinimal(R, set_date_util, up_barrier, down_barrier)
