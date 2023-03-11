import numpy as np
from snow_ball.option.snow_ball import OptionSnowBall
from snow_ball.option.option import Option


class SnowBallPricer:
    def __init__(
        self,
        snow_ball: OptionSnowBall,
        rf: float,
        Smax: float,
        S0: float,
        Nt: int,
        Ns: int,
        sigma: float,
    ):
        self.snow_ball = snow_ball
        self.rf = rf
        self.Smax = Smax
        self.S0 = S0
        self.Nt = Nt
        self.Ns = Ns
        self.sigma = sigma

    def price_option_fdm_cn_bs(self, option: Option):
        Nt = self.Nt
        Ns = self.Ns
        S_max = self.Smax
        r = self.rf
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
            # print(f"time: {i * 240 * dt}")
            F = np.zeros(Ns - 1)
            F[0] = -alpha[0] * grid[i + 1][0] - alpha[0] * grid[i][0]
            F[Ns - 2] = (-gamma[Ns - 2] * grid[i + 1][Ns]) - (
                gamma[Ns - 2] * grid[i][Ns]
            )
            b = np.matmul(B, grid[i + 1][1:Ns]) + F
            # for j in range(Ns - 1):
            #     b[j] = (
            #         alpha[j] * grid[i + 1][j - 1]
            #         + (beta[j] + 1) * grid[i + 1][j]
            #         + gamma[j] * grid[i + 1][j + 1]
            #     )
            # Boundary conditions
            # b[0] = 0
            # b[Ns] = S_max - K * np.exp(-r * ((Nt - i) * dt))

            grid[i][1:Ns] = np.linalg.solve(A, b)
            for j in range(1, Ns):
                continuation = option.continuation_value(
                    i * 240 * dt, j * ds, S0, S_max, r
                )
                grid[i][j] = continuation if continuation != -1 else grid[i][j]

        # Return option price at t=0, S=S0
        return grid[0, int(S0 / ds)]
        # return grid
