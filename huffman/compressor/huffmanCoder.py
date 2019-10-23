from queue import PriorityQueue
from collections import Counter
from functools import reduce


class HuffmanNode(object):
    def __init__(self, symbol=None, weight=0, left=None, right=None):
        self.left = left
        self.right = right
        self.symbol = symbol
        self.weight = weight # used to compare two nodes, which is required by PriorityQueue

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
    def __create_tree(self, text):
        freq_table = Counter(text)
        q = PriorityQueue()
        for symbol in freq_table:
            q.put(HuffmanNode(symbol, freq_table[symbol]))
        while q.qsize() > 1:
            l, r = q.get(), q.get()
            node = HuffmanNode(left=l, right=r, weight=l.weight + r.weight)
            q.put(node)
        return q.get()

    def __assign_codes(self, node, prefix='', codes={}):
        if node.symbol is None:
            self.__assign_codes(node.left, prefix=prefix+'0', codes=codes)
            self.__assign_codes(node.right, prefix=prefix+'1', codes=codes)
        else:
            codes[node.symbol] = prefix
        return codes

    def __encode_huffman_tree(self, node, code=''):
        if node.symbol is not None:
            code += f'1{ord(node.symbol):08b}'
        else:
            code += '0'
            code = self.__encode_huffman_tree(node.left, code)
            code = self.__encode_huffman_tree(node.right, code)

        return code

    def __decode_huffman_tree(self, tree_code_ar):
        code_bit = tree_code_ar[0]
        del tree_code_ar[0]

        if code_bit == '1':
            char = ''
            for _ in range(8):
                char += tree_code_ar[0]
                del tree_code_ar[0]

            return HuffmanNode(chr(int(char, 2)))

        return HuffmanNode(
            None,
            left=self.__decode_huffman_tree(tree_code_ar),
            right=self.__decode_huffman_tree(tree_code_ar)
        )

    def encode(self, text):
        tree = self.__create_tree(text)
        codes_table = self.__assign_codes(tree)

        encoded_text = reduce(lambda accum, char: accum +
                              codes_table[char], list(text), '')
        encoded_tree = self.__encode_huffman_tree(tree)

        # As it is impossible to read file bit by bit in Python (only as bytes),
        # we need to add extra zeros to prevent loss of information (`padding bits`),
        # as well as byte indicating how much bits were added
        num = 8 - (len(encoded_text) + len(encoded_tree)) % 8
        if num != 0:
            encoded_text = num * '0' + encoded_text

        return f'{encoded_tree}{num:08b}{encoded_text}'

    def decode(self, encoded_text):
        tree = self.__decode_huffman_tree(encoded_text)

        # Trimming of `padding bits`
        extra_zeros_number = int(''.join(encoded_text[:8]), 2)
        trimmed = encoded_text[8 + extra_zeros_number:]

        text = ''
        current_node = tree
        for char in trimmed:
            current_node = current_node.left if char == '0' else current_node.right

            if current_node.symbol is not None:
                text += current_node.symbol
                current_node = tree

        return text
