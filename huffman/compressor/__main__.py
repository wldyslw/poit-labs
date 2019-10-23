import argparse
from .huffmanCoder import HuffmanCoder
from .textCompressor import TextCompressor


def main():
    compressor = TextCompressor()
    parser = argparse.ArgumentParser('compressor')
    parser.add_argument(
        '-d', '--decompress',
        help='decompress input file into console or plain .txt',
        action="store_true"
    )
    parser.add_argument('input', metavar='input_file', help='input file path')
    parser.add_argument(
        '-o', '--output', metavar='output_file', help='output file path')

    args = parser.parse_args()

    if args.decompress:
        compressor.decompress_file(args.input, args.output)
        if args.output:
            print(f'Decompressed successfully into {args.output}')
        else:
            print('\nDecompressed successfully')
    else:
        compressor.compress_file(args.input, args.output)
        compressor.print_ratio(
            args.input,
            args.output or compressor.suggest_output_name(args.input)
        )


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
