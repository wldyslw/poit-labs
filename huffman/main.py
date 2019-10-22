from functools import reduce
from huffmanTree import HuffmanCoder
from textParser import TextParser

def main():
    coder = HuffmanCoder()
    encoded_data = ''
    with open('./text.txt') as lines:
        text = TextParser.parse_to_text(lines)
        (table, encoded) = coder.encode(text)
        encoded_data = TextParser.get_encoded_data(table, encoded)
        # print(encoded_data)
        # print(table)
        # print(len(text.encode('utf-8')) * 8 / len(encoded))
    with open('./text-encoded.txt', 'w') as lines:
        lines.write(encoded_data)

    with open('./text-encoded.txt') as lines:
        text = TextParser.parse_to_text(lines)
        table = coder.decode(text)
        print(table)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
