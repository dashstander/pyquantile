
from pyquantile.quantile_element import QuantileElement


class QuantileBlock:
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.elements = []
        self.max_element = -2

    def insert(self, value):
        raise NotImplementedError

    def compress(self):
        raise NotImplementedError

    def merge(self):
        raise NotImplementedError


class InitialBlock(QuantileBlock):
    def __init__(self, max_size: int, stream_size: int):
        super().__init__(max_size)
        self.error = 0

    def insert(self, value: float):
        if value > self.max_element:
            self.max_element = value
        self.elements.append(value)
        if len(self.elements) > self.max_size:
            self.compress()

    def list_to_ranks(self):
        self.elements.sort()
        element_rank_pairs = []
        unique_elements = set()
        rank = 0
        for el in self.elements:
            rank += 1
            if el not in unique_elements and el < self.max_element:
                unique_elements.add(el)
                element_rank_pairs.append((el, rank))
            elif el not in unique_elements and el == self.max_element:
                unique_elements.add(el)
                element_rank_pairs.append(el, len(self.elements))
        return element_rank_pairs
    
    def compress(self):
        element_rank_pairs = self.list_to_ranks()
        return SummaryBlock.make_from_initial(self.max_size, element_rank_pairs)

    def merge(self, other_summary):
        block = self.compress()
        return block.merge(other_summary)

class SummaryBlock(QuantileBlock):
    def __init__(self, max_size: int, error: float):
        super().__init__(max_size)
        self.error = error

    @classmethod
    def make_from_initial(cls, max_size: int, element_rank_pairs):
        new_block = cls(max_size, 0)
        new_block.elements = [QuantileElement(value, rank, rank) for value, rank in element_rank_pairs.items()]
    
    def compress(self):
        new_block = SummaryBlock(self.max_size, 1.0/self.max_size)


    
