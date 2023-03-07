import datetime
import pytest

from snow_ball.date_util import DateUtil, OptionDateCollection


T0 = datetime.datetime(2019, 1, 3)
T_start = datetime.datetime(2019, 1, 4)
T_right = datetime.datetime(2020, 1, 2)
Tn = datetime.datetime(2019, 12, 27)
date_util = DateUtil(OptionDateCollection(T0, T_start, Tn, T_right))


def test_get_date_from_t():
    assert date_util.get_date_from_t(4.5) == datetime.datetime(2019, 1, 10)
    assert date_util.get_date_from_t(5) == datetime.datetime(2019, 1, 10)


def test_get_date_from_t_value_error():
    with pytest.raises(ValueError):
        date_util.get_date_from_t(-1.1)
    with pytest.raises(ValueError):
        date_util.get_date_from_t(241.1)


def test_get_Tout_from_t():
    assert date_util.get_tout_from_t(1) == 0
    assert date_util.get_tout_from_t(1.1) == 3
    assert date_util.get_tout_from_t(239) == 356
    assert date_util.get_tout_from_t(239.9) == 357
    assert date_util.get_tout_from_t(240) == 357
    assert date_util.get_tout_from_t(240.5) == 363
