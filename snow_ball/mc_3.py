import math
from numpy.random import random
import numpy as np
from date_util import DateUtil,OptionDateCollection
import datetime
import matplotlib.pyplot as plt

def simulation(S0, miu,  sigma, I,  plotpath, T=240):

    # :param S ：初始价格
    # :param r: 无风险收益率
    # :param T: 到期期限（年）
    # :param sigma: 波动率
    # :param I: 路径
    
    # 
    delta_t = 1/240
    Spath = np.zeros((T + 1, I))
    Spath[0] = S0
    m=[]
    for t in range(1, T + 1):
        z = np.random.standard_normal(I)
        middle1 = Spath[t-1, 0:I] * np.exp((miu - 0.5 * sigma ** 2) * delta_t + sigma * np.sqrt(delta_t) * z)
        uplimit = Spath[t-1] * 1.1
        lowlimit = Spath[t-1] * 0.9
        temp = np.where(uplimit < middle1, uplimit, middle1)
        temp = np.where(lowlimit > middle1, lowlimit, temp)
        Spath[t, 0:I] = temp
        m.append(max(Spath[t, 0:I]))

    if plotpath:
        plt.plot(Spath[:, :])
        plt.plot([0.68*S0]*len(Spath),color='black')
        
        plt.xlabel('time')
        plt.ylabel('price')
        plt.title('Stock Price Simulation')
        plt.grid(True)
        plt.show()
        plt.close()
        


    return m,Spath


def snowball_cashflowbs(price_path, R, I,N,S0,r):


    T0 = datetime.datetime(2019, 1, 3)
    T_start = datetime.datetime(2019, 1, 4)
    T_right = datetime.datetime(2020, 1, 2)
    Tn = datetime.datetime(2019, 12, 27)
    date_util=DateUtil(OptionDateCollection(T0, T_start, Tn, T_right))
    Tout=np.zeros(I)
    pricebs=np.zeros(I)
    #returns=np.zeros(I)

    payoff = np.zeros(I)
    knock_out_times = 0
    knock_in_times = 0
    existence_times = 0
    for i in range(I):

        
        # 收盘价超过敲出线的交易日
        tmp_up_d = np.where(price_path[:, i] > 1.05*S0)[0]+1
        tmp_up_m=list(
            filter(lambda x: date_util.is_time_t_up_out_monitoring(x), tmp_up_d)
        )
        
        # 收盘价低于敲入线的交易日
        tmp_dn_d = np.where(price_path[:, i] < 0.68*S0)[0]+1
        
        

        # 情景1：发生过向上敲出
        if len(tmp_up_m)>0:

            tout = date_util.get_tout_from_t(tmp_up_m[0])
            t=tout+1
            payoff[i] = N * (1+R*(tout/365))
            knock_out_times += 1
            pricebs[i]=payoff[i]/((1+r/365)**t) 
            #returns[i]=((payoff[i]-pricebs)/price[i])
            Tout[i]=tout

        # 情景2：未敲出且未敲入
        elif len(tmp_up_m) == 0 and len(tmp_dn_d)==0:
            t=date_util.get_tout_from_t(240)+1
            payoff[i] = N*(1+R*357/365)
            existence_times += 1
            pricebs[i]=payoff[i]/((1+r/365)**t) 
            #returns[i]=((payoff[i]-price[i])/price[i])
            Tout[i]=t-1


        # 情景3：只发生向下敲入，不发生向上敲出
        elif len(tmp_up_m) == 0 and len(tmp_dn_d) >0:
            
            t=date_util.get_tout_from_t(240)+1
            payoff[i] = N*min(price_path[len(price_path)-1][i]/S0,1)
            knock_in_times += 1
            pricebs[i]=payoff[i]/((1+r/365)**t) 
            #returns[i]=((payoff[i]-price[i])/price[i])
            Tout[i]=t-1

        else:
            print(i)

    return pricebs


def snowball_cashflowreal(price_path, R, I,N,S0,r,pricebs):


    T0 = datetime.datetime(2019, 1, 3)
    T_start = datetime.datetime(2019, 1, 4)
    T_right = datetime.datetime(2020, 1, 2)
    Tn = datetime.datetime(2019, 12, 27)
    date_util=DateUtil(OptionDateCollection(T0, T_start, Tn, T_right))
    Tout=np.zeros(I)
    
    returns=np.zeros(I)

    payoff = np.zeros(I)
    knock_out_times = 0
    knock_in_times = 0
    existence_times = 0
    for i in range(I):

        
        # 收盘价超过敲出线的交易日
        tmp_up_d = np.where(price_path[:, i] > 1.05*S0)[0]+1
        tmp_up_m=list(
            filter(lambda x: date_util.is_time_t_up_out_monitoring(x), tmp_up_d)
        )
        
        # 收盘价低于敲入线的交易日
        tmp_dn_d = np.where(price_path[:, i] < 0.68*S0)[0]+1
        
        

        # 情景1：发生过向上敲出
        if len(tmp_up_m)>0:

            tout = date_util.get_tout_from_t(tmp_up_m[0])
            t=tout+1
            payoff[i] = N * (1+R*(tout/365))
            knock_out_times += 1
            
            returns[i]=((payoff[i]-pricebs)/pricebs)
            Tout[i]=tout

        # 情景2：未敲出且未敲入
        elif len(tmp_up_m) == 0 and len(tmp_dn_d)==0:
            t=date_util.get_tout_from_t(240)+1
            payoff[i] = N*(1+R*357/365)
            existence_times += 1
            
            returns[i]=((payoff[i]-pricebs)/pricebs)
            Tout[i]=t-1


        # 情景3：只发生向下敲入，不发生向上敲出
        elif len(tmp_up_m) == 0 and len(tmp_dn_d) >0:
            
            t=date_util.get_tout_from_t(240)+1
            payoff[i] = N*min(price_path[len(price_path)-1][i]/S0,1)
            knock_in_times += 1
            
            returns[i]=((payoff[i]-pricebs)/pricebs)
            Tout[i]=t-1

        else:
            print(i)

    return payoff,Tout,returns

np.random.seed(0)
sigma = 0.4068869705985794

S0 = 5.1
r=0.045
q=0.02875161161872558

miu = -0.224
#miu=r-q
I = 10000
T=240
R = 0.28
N=1

mbs,price_pathbs = simulation(S0, miu=r-q,  sigma=sigma, I=I, plotpath=False,T=240)
pricebs = snowball_cashflowbs(price_pathbs, R, I,N,S0,r)
pricebs=np.mean(pricebs)
print(np.mean(pricebs))
mreal,price_pathreal = simulation(S0, miu,  sigma, I, plotpath=True,T=240)
payoffreal, Toutreal,returns= snowball_cashflowreal(price_pathreal, R, I,N,S0,r,pricebs=0.969389711022292)

print(np.mean(payoffreal))
#模拟存活时间
print(np.mean(Toutreal))
#真实存活时间：21， 2月1日敲出
print(np.mean(returns))
print(np.median(returns))
print(np.std(returns))
#真实收益
T0 = datetime.datetime(2019, 1, 3)
T_start = datetime.datetime(2019, 1, 4)
T_right = datetime.datetime(2020, 1, 2)
Tn = datetime.datetime(2019, 12, 27)
date_util=DateUtil(OptionDateCollection(T0, T_start, Tn, T_right))
ttrue= date_util.get_tout_from_t(21)
payofftrue= N * (1+R*(ttrue/365))
pricetrue=payofftrue/((1+r/365)**(ttrue+1)) 
returnstrue=((payofftrue-pricetrue)/pricetrue)
print(returnstrue)
#print(Tout)

