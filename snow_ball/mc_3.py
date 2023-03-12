import math
from numpy.random import random
import numpy as np
from date_util import DateUtil, OptionDateCollection
import datetime
import matplotlib.pyplot as plt


def simulation(S0, r, sigma, I, plotpath, T=240):
    # :param S ：初始价格
    # :param r: 无风险收益率
    # :param T: 到期期限（年）
    # :param sigma: 波动率
    # :param I: 路径
    # :param dn: 敲入点
    # :param steps:
    # :param plotpath:
    # :param plothist:
    # :return:
    #
    delta_t = 1 / 240
    Spath = np.zeros((T + 1, I))
    Spath[0] = S0
    m = []
    for t in range(1, T + 1):
        z = np.random.standard_normal(I)
        middle1 = Spath[t - 1, 0:I] * np.exp(
            (r - 0.5 * sigma**2) * delta_t + sigma * np.sqrt(delta_t) * z
        )
        uplimit = Spath[t - 1] * 1.1
        lowlimit = Spath[t - 1] * 0.9
        temp = np.where(uplimit < middle1, uplimit, middle1)
        temp = np.where(lowlimit > middle1, lowlimit, temp)
        Spath[t, 0:I] = temp
        m.append(max(Spath[t, 0:I]))

    if plotpath:
        plt.plot(Spath[:, :])
        plt.plot([0.68 * S0] * len(Spath), color="black")

        plt.xlabel("time")
        plt.ylabel("price")
        plt.title("price Simulation")
        plt.grid(True)
        plt.show()
        plt.close()

    return m, Spath


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
        tmp_up_d = np.where(price_path[:, i] > 1.05 * S0)[0] + 1
        if len(tmp_up_d) == 0:
            tmp_up_m = False

        else:
            # tmp_up_d = np.array(list(map(date_util.get_tout_from_t,tmp_up_d)))
            tmp_up_m = any(list(map(date_util.is_time_t_up_out_monitoring, tmp_up_d)))

        # 收盘价低于敲入线的交易日

        tmp_dn_d = np.where(price_path[:, i] < 0.68 * S0)[0] + 1
        if len(tmp_dn_d) == 0:
            tmp_dn_m = False
        else:
            tmp_dn_m = True
        # 根据合约条款判断现金流

        # 情景1：发生过向上敲出
        if tmp_up_m:
            tout = date_util.get_tout_from_t(tmp_up_d[0])
            payoff[i] = N * (1 + R * (tout / 365))
            knock_out_times += 1
            Tout.append(tout)

        # 情景2：未敲出且未敲入
        elif tmp_up_m == False and tmp_dn_m == False:
            payoff[i] = N * (1 + R * 357 / 365)
            existence_times += 1

        # 情景3：只发生向下敲入，不发生向上敲出
        elif tmp_dn_m and tmp_up_m == False:
            # 只有向下敲入，没有向上敲出
            payoff[i] = N * min(price_path[len(price_path) - 1][i] / S0, 1)
            knock_in_times += 1
        else:
            print(i)
    return payoff, knock_out_times, knock_in_times, existence_times, Tout


np.random.seed(0)
sigma = 0.5

S0 = 5.1
r = 0.04
I = 100000
T = 240
R = 0.28
N = 1


m, price_path = simulation(S0, r, sigma, I, plotpath=True, T=240)
print(max(m))
# plt.plot(price_path[:, :])
# plt.plot(0.68*S0*len(price_path))
# plt.ylim((0,max(m)+1))
# plt.xlabel('time')
# plt.ylabel('price')
# plt.title('price Simulation')
# plt.grid(True)
# plt.show()
payoff, knock_out_times, knock_in_times, existence_times, Tout = snowball_cashflow(
    price_path, R, I, N, S0
)
print(np.mean(payoff))
# print(Tout)
b = 1
