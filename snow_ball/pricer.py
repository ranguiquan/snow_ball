import numpy as np
from snow_ball.option.snow_ball import OptionSnowBall
from snow_ball.option.option import Option


class SnowBallPricer:
    def __init__(
        self,
        snow_ball: OptionSnowBall,
        rf: float,
        q: float,
        Smax: float,
        S0: float,
        Nt: int,
        Ns: int,
        sigma: float,
    ):
        self.snow_ball = snow_ball
        self.rf = rf
        self.q = q
        self.Smax = Smax
        self.S0 = S0
        self.Nt = Nt
        self.Ns = Ns
        self.sigma = sigma
        self.grid_option_up_out_auto_call = self._get_price_grid_option_fdm_cn(
            snow_ball.up_out_auto_call
        )
        self.grid_option_up_down_out = self._get_price_grid_option_fdm_cn(
            snow_ball.up_out_down_out
        )
        self.grid_option_up_out_minimal = self._get_price_grid_option_fdm_cn(
            snow_ball.up_out_minimal
        )
        self.grid_option_up_out_down_out_minimal = self._get_price_grid_option_fdm_cn(
            snow_ball.up_out_down_out_minimal
        )
        self.grid_option_minimal = self._get_price_grid_option_fdm_cn(snow_ball.minimal)
        self.grid_option_snow_ball = (
            self.grid_option_up_out_auto_call
            + self.grid_option_up_down_out
            + self.grid_option_up_out_minimal
            - self.grid_option_up_out_down_out_minimal
        )

    def _get_price_grid_option_fdm_cn(self, option: Option):
        Nt = self.Nt
        Ns = self.Ns
        S_max = self.Smax
        r = self.rf - self.q
        S0 = self.S0
        sigma = self.sigma
        T = self.snow_ball.date_util.option_time_collection.end_time

        T_model = T / 240

        # Time steps and price steps
        dt = T_model / Nt
        ds = S_max / Ns

        # Define grid
        grid = np.zeros((Nt + 1, Ns + 1))

        # Set up boundary conditions
        # End boundary condition
        for j in range(Ns + 1):
            S = j * ds
            grid[Nt][j] = option.continuation_value(Nt * 240 * dt, S, S0, S_max, r)

        # Upper boundary condition
        for i in range(Nt - 1, -1, -1):
            grid[i][-1] = option.continuation_value(i * 240 * dt, S_max, S0, S_max, r)
            # grid[i + 1][-1] / (1 + r * dt)

        # Lower boundary condition
        for i in range(Nt - 1, -1, -1):
            grid[i][0] = option.continuation_value(i * 240 * dt, 0, S0, S_max, r)

        # Set up coefficients
        alpha = np.zeros(Ns - 1)
        beta = np.zeros(Ns - 1)
        gamma = np.zeros(Ns - 1)
        for j in range(Ns - 1):
            S = j * ds
            alpha[j] = 0.25 * (sigma**2 * S**2 / ds**2 - r * S / ds)
            beta[j] = -0.5 * (sigma**2 * S**2 / ds**2 + r)
            gamma[j] = 0.25 * (sigma**2 * S**2 / ds**2 + r * S / ds)

        # Set up tri-diagonal matrix
        A = np.zeros((Ns - 1, Ns - 1))
        B = np.zeros((Ns - 1, Ns - 1))
        F = np.zeros(Ns - 1)

        for j in range(Ns - 1):
            if j != 0:
                A[j][j - 1] = alpha[j]
                B[j][j - 1] = -alpha[j]
            A[j][j] = beta[j] - 1 / dt
            B[j][j] = -beta[j] - 1 / dt
            if j != Ns - 2:
                A[j][j + 1] = gamma[j]
                B[j][j + 1] = -gamma[j]

        # Compute solution
        for i in range(Nt - 1, -1, -1):
            F = np.zeros(Ns - 1)
            F[0] = -alpha[0] * grid[i + 1][0] - alpha[0] * grid[i][0]
            F[Ns - 2] = (-gamma[Ns - 2] * grid[i + 1][Ns]) - (
                gamma[Ns - 2] * grid[i][Ns]
            )
            b = np.matmul(B, grid[i + 1][1:Ns]) + F
            grid[i][1:Ns] = np.linalg.solve(A, b)
            for j in range(1, Ns):
                continuation = option.continuation_value(
                    i * 240 * dt, j * ds, S0, S_max, r
                )
                grid[i][j] = continuation if continuation != -1 else grid[i][j]

        # Return option price grid
        return grid

    def get_price_from_grid(self, grid: np.array, S: float, t: float) -> float:
        Smax = self.Smax
        Ns = self.Ns
        ds = Smax / Ns
        T = self.snow_ball.date_util.option_time_collection.end_time
        Nt = self.Nt
        dt = T / Nt

        return grid[int(t / dt), int(S / ds)]

    def get_snow_ball_price(self) -> list[float, dict[str, float]]:
        grid_option_list = [
            self.grid_option_up_out_auto_call,
            self.grid_option_up_down_out,
            self.grid_option_up_out_minimal,
            self.grid_option_up_out_down_out_minimal,
        ]
        price_option_list = [
            self.get_price_from_grid(grid, self.S0, 0) for grid in grid_option_list
        ]
        return (
            price_option_list[0]
            + price_option_list[1]
            + price_option_list[2]
            - price_option_list[3],
            price_option_list,
        )

    def get_snow_ball_delta(self, S: float, t: float) -> float:
        Smax = self.Smax
        Ns = self.Ns
        ds = Smax / Ns
        T = self.snow_ball.date_util.option_time_collection.end_time
        Nt = self.Nt
        dt = T / Nt

        index_s = int(S / ds)
        index_t = int(t / dt)
        # if index_s + 1 >= int(self.snow_ball.up_out_auto_call.up_barrier / ds):
        #     return (self.grid_option_snow_ball[index_t][index_s-2] - self.grid_option_snow_ball[index_t][index_s-3]) / ds
        # if index_s - 3 <= int(self.snow_ball.up_out_down_out.down_barrier / ds):
        #     # return (self.grid_option_snow_ball[index_t][index_s + 1] - self.grid_option_minimal[index_t][index_s - 1]) / (ds * 2)
        #     return (self.grid_option_snow_ball[index_t][index_s + 10] - self.grid_option_minimal[index_t][index_s + 9]) / ds
        return (
            self.grid_option_snow_ball[index_t][index_s + 1]
            - self.grid_option_snow_ball[index_t][index_s - 1]
        ) / (2 * ds)

    def get_option_minimal_delta(self, S: float, t: float) -> float:
        Smax = self.Smax
        Ns = self.Ns
        ds = Smax / Ns
        T = self.snow_ball.date_util.option_time_collection.end_time
        Nt = self.Nt
        dt = T / Nt

        index_s = int(S / ds)
        index_t = int(t / dt)
        return (
            self.grid_option_up_down_out[index_t][index_s + 1]
            + self.grid_option_up_out_minimal[index_t][index_s + 1]
            - self.grid_option_up_out_down_out_minimal[index_t][index_s + 1]
            - self.grid_option_up_down_out[index_t][index_s - 1]
            - self.grid_option_up_out_minimal[index_t][index_s - 1]
            + self.grid_option_up_out_down_out_minimal[index_t][index_s - 1]
        ) / (2 * ds)
        # return (
        #     self.grid_option_snow_ball[index_t][index_s + 1]
        #     - self.grid_option_snow_ball[index_t][index_s - 1]
        # ) / 2
