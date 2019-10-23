import re
from os.path import getsize
from functools import reduce
from .huffmanCoder import HuffmanCoder


class TextCompressor:
    def __init__(self):
        self.coder = HuffmanCoder()

    def suggest_output_name(self, input_path):
        return re.sub(r'\.\w+$', '-compressed.bin', input_path)

    def compress_file(self, input_path, output_path=None):
        if output_path is None:
            output_path = self.suggest_output_name(input_path)
        with open(input_path, 'r') as input_f, open(output_path, 'wb') as output_f:
            text = input_f.read()
            encoded_text = self.coder.encode(text)
            arr = bytearray()
            for i in range(0, len(encoded_text), 8):
                arr.append(int(encoded_text[i:i+8], 2))
            output_f.write(arr)

    def decompress_file(self, input_path, output_path=None):
        decoded = ''
        with open(input_path, 'rb') as f:
            lines = f.read()
            text = list(reduce(lambda accum, byte: accum + f'{byte:08b}', lines, ''))
            decoded = self.coder.decode(text)
        if output_path is None:
            print(decoded)
        else:
            with open(output_path, 'w') as f:
                f.write(decoded)

    def print_ratio(self, input_path, output_path):
        before_size = getsize(input_path)
        after_size = getsize(output_path)
        compression_percent = round(100 - after_size / before_size * 100, 1)
        message = (
            f'Compare between {input_path} and {output_path}:\n'
            f'Before: {before_size} bytes\n'
            f'After: {after_size} bytes\n'
            f'Compression rate: {compression_percent}%'
        )
        print(message)
