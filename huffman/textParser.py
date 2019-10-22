from functools import reduce
class TextParser:
    @staticmethod
    def parse_to_text(io):
        return reduce(lambda acc, el: acc + el, io, '')

    @staticmethod
    def get_encoded_data(table, encoded):
        codes = ''.join([f'{code}:{char};' for char, code in table.items()])
        return codes + encoded
