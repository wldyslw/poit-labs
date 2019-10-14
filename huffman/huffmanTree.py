from queue import PriorityQueue
from functools import reduce
import operator


class HuffmanNode(object):
    def __init__(self, symbol=None, weight=0, left=None, right=None):
        self.left = left
        self.right = right
        self.symbol = symbol
        self.weight = weight

    def children(self):
        return (self.left, self.right)

    def __lt__(self, other):
        return self.weight < other.weight

    def __gt__(self, other):
        return self.weight > other.weight


class HuffmanCoder:
    def __init__(self, text):
        self.text = text
        self.symbols_freq = self.__create_symbols_dict()
        self.tree = self.__create_tree()
        self.codes = self.__assign_codes()

    def __create_symbols_dict(self):
        symbols = {}
        for symbol in self.text:
            try:
                symbols[symbol] += 1
            except KeyError:
                symbols[symbol] = 1
        return symbols

    def __create_tree(self):
        q = PriorityQueue()
        for symbol in self.symbols_freq:
            q.put(
                HuffmanNode(symbol, self.symbols_freq[symbol])
            )
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

    def __assign_codes(self, node=None, prefix='', codes={}):
        if node is None:
            node = self.tree
        if node.symbol is None:
            self.__assign_codes(node.left, prefix=prefix+'0', codes=codes)
            self.__assign_codes(node.right, prefix=prefix+'1', codes=codes)
        else:
            codes[node.symbol] = prefix
        return codes

    def get_table(self):
        pass

    def encode(self):
        accum = ''
        for char in self.text:
            accum += f'{self.codes[char]} '
        return accum

    def decode(self):
        pass


def main():
    with open('./text.txt') as lines:
        text = reduce(lambda acc, el: acc + el, lines)
        coder = HuffmanCoder(text)
        encoded = coder.encode()
        print(len(text.encode('utf-8')) * 8 / len(encoded.replace(' ', '')))
        # for code in codes:
        #    print('\'{}\' = {}'.format(code, codes[code]))


main()
