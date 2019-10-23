# Huffman text file compressor

Package for compressing files with [Huffman coding](https://en.wikipedia.org/wiki/Huffman_coding). Please note that this compressor **works only with ASCII** characters and will crash trying to parse Unicode.

## Try it out

Open project file in console and run step by step:

```sh
python -m compressor constitution.txt

python -m compressor --decompress constitution-compressed.bin
```

For more info run:

```sh
python -m compressor -h
```

## How it works

Compressing:

1. Read text from input file
2. Create frequencies table using `collections.Counter`
3. Create Huffman tree nodes and merge them into tree with help of `PriorityQueue`
4. Create codes mapping table (e.g. `{ 'a': '000', 'b': '010', ... }`)
5. Encode text using table above
6. Encode Huffman tree (`0` for each node, `1` + encoded ASCII char for each leaf)
7. Add padding bits and merge encoded tree and text
8. Save result to binary file

Decompressing:

1. Read encoded data
2. Decode a Huffman tree, also extracting encoded text
3. Remove padding bits
4. Decode text using tree
5. Save result to file or log it to console
