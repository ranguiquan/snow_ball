import math
from numpy.random import random
import numpy as np
from snow_ball.date_util import DateUtil, OptionDateCollection
import datetime
import matplotlib.pyplot as plt
from snow_ball.pricer import SnowBallPricer


def simulation(
    S0: float, rf: float, sigma: float, path_count: int, is_plot_path: int, T: int = 240
) -> np.array:
    """generate underlying price paths

    Args:
        S0 (float): underlying initial price
        rf (float): risk free rate
        sigma (float): underlying sigma
        path_count (int): count of path
        is_plot_path (int): plot the paths or not
        T (int, optional): _description_. Defaults to 240.

    Returns:
        np.array: [T + 1, path_count] matrix
    """

    # time (year)
    T_model = T / 240
    # time step (year)
    delta_t = T_model / T
    Spath = np.zeros((T + 1, path_count))
    Spath[0] = S0
    # m = []
    for t in range(1, T + 1):
        z = np.random.standard_normal(path_count)
        middle1 = Spath[t - 1, 0:path_count] * np.exp(
            (rf - 0.5 * sigma**2) * delta_t + sigma * np.sqrt(delta_t) * z
        )
        uplimit = Spath[t - 1] * 1.1
        lowlimit = Spath[t - 1] * 0.9
        temp = np.where(uplimit < middle1, uplimit, middle1)
        temp = np.where(lowlimit > middle1, lowlimit, temp)
        Spath[t, 0:path_count] = temp
        # m.append(max(Spath[t, 0:I]))

    if is_plot_path:
        plt.plot(Spath[:, :])
        plt.plot([0.68 * S0] * len(Spath), color="black")

        plt.xlabel("time")
        plt.ylabel("price")
        plt.title("price Simulation")
        plt.grid(True)
        plt.show()
        plt.close()

    return Spath
    # return m, Spath


def snowball_cashflow(price_path, R, I, N, S0):
    T0 = datetime.datetime(2019, 1, 3)
    T_start = datetime.datetime(2019, 1, 4)
    T_right = datetime.datetime(2020, 1, 2)
    Tn = datetime.datetime(2019, 12, 27)
    date_util = DateUtil(OptionDateCollection(T0, T_start, Tn, T_right))
    Tout = []

    payoff = np.zeros(I)
    knock_out_times = 0
    knock_in_times = 0
    existence_times = 0
    for i in range(I):
        # 收盘价超过敲出线的交易日
        up_out_dates = np.where(price_path[:, i] > 1.05 * S0)[0]
        up_out_dates = list(
            filter(lambda x: date_util.is_time_t_up_out_monitoring(x), up_out_dates)
        )
        if len(up_out_dates) == 0:
            up_out_flag = False

        else:
            # tmp_up_d = np.array(list(map(date_util.get_tout_from_t,tmp_up_d)))
            # tmp_up_m = any(list(map(date_util.is_time_t_up_out_monitoring, tmp_up_d)))
            up_out_flag = True

        # 收盘价低于敲入线的交易日

        down_in_dates = np.where(price_path[:, i] < 0.68 * S0)[0]
        if len(down_in_dates) == 0:
            down_in_flag = False
        else:
            down_in_flag = True
        # 根据合约条款判断现金流

        # 情景1：发生过向上敲出
        if up_out_flag:
            tout = date_util.get_tout_from_t(up_out_dates[0])
            # print(tout)
            payoff[i] = N * (1 + R * (tout / 365))
            knock_out_times += 1
            Tout.append(tout)

        # 情景2：未敲出且未敲入
        elif up_out_flag == False and down_in_flag == False:
            payoff[i] = N * (1 + R * 357 / 365)
            existence_times += 1

        # 情景3：只发生向下敲入，不发生向上敲出
        elif down_in_flag and up_out_flag == False:
            # 只有向下敲入，没有向上敲出
            payoff[i] = N * min(price_path[len(price_path) - 1][i] / S0, 1)
            knock_in_times += 1
        else:
            # print(i)
            pass
    # print(knock_in_times)
    return payoff, knock_out_times, knock_in_times, existence_times, Tout


def delta_hedging_portfolio(price_path: np.array, pricer: SnowBallPricer) -> np.array:
    date_util = pricer.snow_ball.date_util
    S0 = pricer.S0
    # state of the snow ball option
    # 0 means original state
    # 1 means knock in
    # 2 means knock out
    states = np.zeros((price_path.shape[0], price_path.shape[1]))
    portfolio = np.zeros((price_path.shape[0], price_path.shape[1]))
    # time length
    T = price_path.shape[0]
    # path_count
    path_count = price_path.shape[1]

    for i in range(path_count):
        # 收盘价低于敲入线的交易日

        down_in_dates = np.where(price_path[:, i] < 0.68 * S0)[0]
        states[down_in_dates, i] = 1
        if len(down_in_dates) == 0:
            down_in_flag = False
        else:
            down_in_flag = True

        # 收盘价超过敲出线的交易日
        up_out_dates = np.where(price_path[:, i] > 1.05 * S0)[0]
        up_out_dates = list(
            filter(lambda x: date_util.is_time_t_up_out_monitoring(x), up_out_dates)
        )
        states[up_out_dates, i] = 2
        if len(up_out_dates) == 0:
            up_out_flag = False

        else:
            # tmp_up_d = np.array(list(map(date_util.get_tout_from_t,tmp_up_d)))
            # tmp_up_m = any(list(map(date_util.is_time_t_up_out_monitoring, tmp_up_d)))
            up_out_flag = True

        # state matrix
        states[:, i] = np.maximum.accumulate(states[:, i])
        for j in range(T - 1):
            if states[j, i] == 0:
                portfolio[j, i] = -pricer.get_snow_ball_delta(price_path[j, i], j + 1)
            elif states[j, i] == 1:
                portfolio[j, i] = -pricer.get_option_minimal_delta(
                    price_path[j, i], j + 1
                )
            else:
                break
    return portfolio


def delta_portfolio_return(portfolio: np.array, price_path: np.array):
    return_path = np.diff(price_path, axis=0)
    # return_path = np.diff(price_path, axis=0) / price_path[:-1, :]
    portfolio_return = return_path * portfolio[:-1, :]
    return np.sum(portfolio_return, axis=0)


if __name__ == "__main__":
    np.random.seed(0)
    sigma = 0.5

    S0 = 5.1
    r = 0.04
    path_count = 1000
    T = 240
    R = 0.28
    N = 1

    price_path = simulation(S0, r, sigma, path_count, is_plot_path=False, T=240)
    # print(max(m))
    # plt.plot(price_path[:, :])
    # plt.plot(0.68*S0*len(price_path))
    # plt.ylim((0,max(m)+1))
    # plt.xlabel('time')
    # plt.ylabel('price')
    # plt.title('price Simulation')
    # plt.grid(True)
    # plt.show()*
    payoff, knock_out_times, knock_in_times, existence_times, Tout = snowball_cashflow(
        price_path, R, path_count, N, S0
    )
    print(np.mean(payoff))
    # print(Tout)
    # b = 1
