from typing import List, Tuple
from pyquantile.quantile_element import QuantileElement


class QuantileBlock:
    def __init__(self, max_size: int) -> None:
        self.max_size = max_size
        self.elements = []
        self.max_element = -2

    def insert(self, value: float) -> None:
        raise NotImplementedError

    def compress(self):
        raise NotImplementedError

    def merge(self, other_summary):
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

    def list_to_ranks(self) -> List[Tuple[float]]:
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

    def merge(self, other_summary: SummaryBlock) -> SummaryBlock:
        block = self.compress()
        return block.merge(other_summary)

class SummaryBlock(QuantileBlock):
    def __init__(self, max_size: int, error: float):
        super().__init__(max_size)
        self.error = error

    @classmethod
    def make_from_initial(cls, max_size: int, element_rank_pairs: List[Tuple[float]] ) -> SummaryBlock:
        new_block = cls(max_size, 0)
        new_block.elements = [QuantileElement(value, rank, rank) for value, rank in element_rank_pairs.items()]
        new_block.max_element = new_block.elements[-1]
        return new_block
    
    def compress(self) -> SummaryBlock:
        new_block = SummaryBlock(self.max_size, 1.0/self.max_size)
        ix = [0] + [i for i in range(1, len(self.elements) - 1, 2)] + [len(self.elements) - 1]
        new_block.elements = [self.elements[i] for i in ix]
        new_block.max_element = self.max_element
        return new_block
    
    def merge(self, other_summary: SummaryBlock) -> SummaryBlock:
        pass



    
