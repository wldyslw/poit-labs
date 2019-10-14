from functools import reduce
from huffmanTree import HuffmanCoder
from textParser import TextParser

def main():
    with open('./text.txt') as lines:
        text = reduce(lambda acc, el: acc + el, lines)
        coder = HuffmanCoder(text)
        encoded = coder.encode()
        print(len(text.encode('utf-8')) * 8 / len(encoded))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
