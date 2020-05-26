import numpy as np

class QuantileSummary:
    def __init__(self, error, stream_size):
        self.error = error
        self.stream_size = stream_size
        self.block_size = np.floor(np.log(self.error * self.stream_size) / self.error)