from queue import PriorityQueue
from functools import reduce


class HuffmanNode(object):
    def __init__(self, symbol=None, weight=0, left=None, right=None):
        self.left = left
        self.right = right
        self.symbol = symbol
        self.weight = weight

    def children(self):
        return (self.left, self.right)

    def __lt__(self, other):
        if not isinstance(other, HuffmanNode):
            raise Exception(
                f'\'<\' operator can only be used with other HuffmanNode, {type(other).__name__} provided instead')
        return self.weight < other.weight

    def __gt__(self, other):
        if not isinstance(other, HuffmanNode):
            raise Exception(
                f'\'>\' operator can only be used with other HuffmanNode, {type(other).__name__} provided instead')
        return self.weight > other.weight


class HuffmanCoder:
    def __init__(self, text, table=None):
        self.text = text
        if table is None:
            freq_table = self.__create_symbols_dict()
            tree = self.__create_tree(freq_table)
            self.codes_table = self.__assign_codes(node=tree)
        else:
            self.codes_table = table

    def __create_symbols_dict(self):
        symbols = {}
        for symbol in self.text:
            try:
                symbols[symbol] += 1
            except KeyError:
                symbols[symbol] = 1
        return symbols

    def __create_tree(self, freq_table):
        q = PriorityQueue()
        for symbol in freq_table:
            q.put(HuffmanNode(symbol, freq_table[symbol]))
        while q.qsize() > 1:
            l, r = q.get(), q.get()
            l, r = (l, r) if l < r else (r, l)
            node = HuffmanNode(
                left=l,
                right=r,
                weight=l.weight + r.weight
            )
            q.put(node)
        return q.get()

    def __assign_codes(self, node, prefix='', codes={}):
        if node.symbol is None:
            self.__assign_codes(node.left, prefix=prefix+'0', codes=codes)
            self.__assign_codes(node.right, prefix=prefix+'1', codes=codes)
        else:
            codes[node.symbol] = prefix
        return codes

    def get_table(self):
        return self.codes_table

    def encode(self):
        accum = ''
        for char in self.text:
            accum += self.codes_table[char]
        return accum

    def decode(self):
        pass

