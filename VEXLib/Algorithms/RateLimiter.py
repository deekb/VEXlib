import VEXLib.Math.MathUtil as MathUtil
from time import time


class SlewRateLimiter:
    def __init__(self, positive_rate_limit, negative_rate_limit, initial_value):
        self.m_positive_rate_limit = positive_rate_limit
        self.m_negative_rate_limit = negative_rate_limit
        self.m_prev_val = initial_value
        self.m_prev_time = time()

    def calculate(self, input_val):
        current_time = time()
        elapsed_time = current_time - self.m_prev_time
        self.m_prev_val += MathUtil.clamp(input_val - self.m_prev_val,
                                          self.m_negative_rate_limit * elapsed_time,
                                          self.m_positive_rate_limit * elapsed_time)
        self.m_prev_time = current_time
        return self.m_prev_val

    def reset(self, value):
        self.m_prev_val = value
        self.m_prev_time = time()
