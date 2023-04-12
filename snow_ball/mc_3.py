import math
from numpy.random import random
import numpy as np
from .date_util import DateUtil,OptionDateCollection
import datetime
import matplotlib.pyplot as plt

def simulation(
    S0: float,
    rf: float,
    q: float,
    sigma: float,
    path_count: int,
    is_plot_path: bool,
    T: int = 240,
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
    m=[]
    for t in range(1, T + 1):
        z = np.random.standard_normal(path_count)
        middle1 = Spath[t - 1, 0:path_count] * np.exp(
            (rf - q - 0.5 * sigma**2) * delta_t + sigma * np.sqrt(delta_t) * z
        )
        uplimit = Spath[t - 1] * 1.1
        lowlimit = Spath[t - 1] * 0.9
        temp = np.where(uplimit < middle1, uplimit, middle1)
        temp = np.where(lowlimit > middle1, lowlimit, temp)
        Spath[t, 0:I] = temp
        m.append(max(Spath[t, 0:I]))

    if is_plot_path:
        plt.plot(Spath[:, :])
        plt.plot([0.68*S0]*len(Spath),color='black')
        
        plt.xlabel('time')
        plt.ylabel('price')
        plt.title('Stock Price Simulation')
        plt.grid(True)
        plt.show()
        plt.close()
        


    return m,Spath



def snowball_cashflow(price_path, R, I, N, S0, rf):
    T0 = datetime.datetime(2019, 1, 3)
    T_start = datetime.datetime(2019, 1, 4)
    T_right = datetime.datetime(2020, 1, 2)
    Tn = datetime.datetime(2019, 12, 27)
    date_util=DateUtil(OptionDateCollection(T0, T_start, Tn, T_right))
    Tout=np.zeros(I)
    pricebs=np.zeros(I)
    #returns=np.zeros(I)

    payoff = np.zeros(I)
    payoff_present_value = np.zeros(I)
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
            payoff_present_value[i] = N * (1 + R * (tout / 365)) / (1 + rf / 365 * tout)
            knock_out_times += 1
            pricebs[i]=payoff[i]/((1+r/365)**tout) 
            #returns[i]=((payoff[i]-pricebs)/price[i])
            Tout[i]=tout

        # 情景2：未敲出且未敲入
        elif up_out_flag == False and down_in_flag == False:
            payoff[i] = N * (1 + R * 357 / 365)
            payoff_present_value[i] = N * (1 + R * (357 / 365)) / (1 + rf / 365 * 357)
            existence_times += 1
            pricebs[i]=payoff[i]/((1+r/365)**tout) 
            #returns[i]=((payoff[i]-price[i])/price[i])
            Tout[i]=tout-1


        # 情景3：只发生向下敲入，不发生向上敲出
        elif down_in_flag and up_out_flag == False:
            # 只有向下敲入，没有向上敲出
            payoff[i] = N * min(price_path[len(price_path) - 1][i] / S0, 1)
            payoff_present_value[i] = (
                N
                * min(price_path[len(price_path) - 1][i] / S0, 1)
                / (1 + rf / 365 * 357)
            )

            knock_in_times += 1
            pricebs[i]=payoff[i]/((1+r/365)**tout) 
            #returns[i]=((payoff[i]-price[i])/price[i])
            Tout[i]=tout-1

        else:
            # print(i)
            pass
    # print(knock_in_times)
    return (
        payoff,
        payoff_present_value,
        knock_out_times,
        knock_in_times,
        existence_times,
        Tout,
    )


def delta_portfolio_return(portfolio: np.array, price_path: np.array):
    return_path = np.diff(price_path, axis=0)
    # return_path = np.diff(price_path, axis=0) / price_path[:-1, :]
    portfolio_return = return_path * portfolio[:-1, :]
    res = np.sum(portfolio_return, axis=0)
    return res


# if __name__ == "__main__":
#     np.random.seed(0)
#     sigma = 0.5

# S0 = 5.1
# r=0.045
# q=0.02875161161872558

# miu = -0.224
# #miu=r-q
# I = 10000
# T=240
# R = 0.28
# N=1

# mbs,price_pathbs = simulation(S0, miu=r-q,  sigma=sigma, I=I, plotpath=False,T=240)
# pricebs = snowball_cashflowbs(price_pathbs, R, I,N,S0,r)
# pricebs=np.mean(pricebs)
# print(np.mean(pricebs))
# mreal,price_pathreal = simulation(S0, miu,  sigma, I, plotpath=True,T=240)
# payoffreal, Toutreal,returns= snowball_cashflowreal(price_pathreal, R, I,N,S0,r,pricebs=0.969389711022292)

# print(np.mean(payoffreal))
# #模拟存活时间
# print(np.mean(Toutreal))
# #真实存活时间：21， 2月1日敲出
# print(np.mean(returns))
# print(np.median(returns))
# print(np.std(returns))
# #真实收益
# T0 = datetime.datetime(2019, 1, 3)
# T_start = datetime.datetime(2019, 1, 4)
# T_right = datetime.datetime(2020, 1, 2)
# Tn = datetime.datetime(2019, 12, 27)
# date_util=DateUtil(OptionDateCollection(T0, T_start, Tn, T_right))
# ttrue= date_util.get_tout_from_t(21)
# payofftrue= N * (1+R*(ttrue/365))
# pricetrue=payofftrue/((1+r/365)**(ttrue+1)) 
# returnstrue=((payofftrue-pricetrue)/pricetrue)
# print(returnstrue)
# #print(Tout)

