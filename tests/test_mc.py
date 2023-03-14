from snow_ball.mc_3 import (
    delta_hedging_portfolio,
    delta_portfolio_return,
    simulation,
    snowball_cashflow,
)
from tests.test_fixures import (
    R,
    rf,
    S0,
    set_date_util,
    set_pricer,
    set_snow_ball,
    sigma,
)

# def test_simulation():
#     Spath = simulation(S0, rf, sigma, 1000, False)
#     assert Spath.shape[0] == 241
#     assert Spath.shape[1] == 1000

# def test_delta_hedging(set_pricer):
#     Spath = simulation(S0, rf, sigma, 1000, False)
#     delta_hedging_portfolio(Spath, set_pricer)

# def test_delta_potfolio_return(set_pricer):
#     Spath = simulation(S0, rf, sigma, 1000, False)
#     payoff, knock_out_times, knock_in_times, existence_times, Tout = snowball_cashflow(Spath, R, 1000, 1, S0)
#     portfolio = delta_hedging_portfolio(Spath, set_pricer)
#     hedging_payoff = - delta_portfolio_return(portfolio, Spath) + payoff
#     print(hedging_payoff)
