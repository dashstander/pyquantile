import numpy as np

class QuantileElement:
    def __init__(self, value, min_rank, max_rank):
        self.value = value
        self.min_rank = min_rank
        self.max_rank = max_rank