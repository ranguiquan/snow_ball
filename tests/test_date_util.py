import datetime
import pytest

from snow_ball.date_util import DateUtil
from tests.test_fixures import set_date_util


def test_get_date_from_t(set_date_util: DateUtil):
    assert set_date_util.get_date_from_t(4.5) == datetime.datetime(2019, 1, 10)
    assert set_date_util.get_date_from_t(5) == datetime.datetime(2019, 1, 10)


def test_get_date_from_t_value_error(set_date_util: DateUtil):
    with pytest.raises(ValueError):
        set_date_util.get_date_from_t(-1.1)
    with pytest.raises(ValueError):
        set_date_util.get_date_from_t(241.1)


def test_get_Tout_from_t(set_date_util: DateUtil):
    assert set_date_util.get_tout_from_t(1) == 0
    assert set_date_util.get_tout_from_t(1.1) == 3
    assert set_date_util.get_tout_from_t(239) == 356
    assert set_date_util.get_tout_from_t(239.9) == 357
    assert set_date_util.get_tout_from_t(240) == 357
    assert set_date_util.get_tout_from_t(240.5) == 363


def test_is_time_t_up_out_monitoring(set_date_util: DateUtil):
    assert set_date_util.is_time_t_up_out_monitoring(0) == False
    assert set_date_util.is_time_t_up_out_monitoring(20.5) == True
    assert set_date_util.is_time_t_up_out_monitoring(21) == True
    assert set_date_util.is_time_t_up_out_monitoring(21.5) == False
    assert set_date_util.is_time_t_up_out_monitoring(21.5) == False
    assert set_date_util.is_time_t_up_out_monitoring(240) == True


def test_is_time_t_down_in_monitoring(set_date_util: DateUtil):
    assert set_date_util.is_time_t_down_in_monitoring(0) == False
    assert set_date_util.is_time_t_down_in_monitoring(0.5) == True
    assert set_date_util.is_time_t_down_in_monitoring(1) == True
    assert set_date_util.is_time_t_down_in_monitoring(240) == True
    assert set_date_util.is_time_t_down_in_monitoring(240.5) == False
