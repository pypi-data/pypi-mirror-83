from math import ceil
from random import SystemRandom
from bitstring import Bits, BitStream
from base64 import b85encode, b85decode

rnd = SystemRandom()


class Plex():
    def __init__(self, book):
        self.book = Bits(hex=book)
        self.len = self.book.len
        self.byte_len = ceil(self.len.bit_length() / 8)
        self._check_book()

    def _check_book(self):
        if self.len / 8 < 500000:
            raise Exception('Less than 500k bytes in the book')

    def encode(self, text):
        bits = Bits(bytes=text.encode('utf-8'))
        stream = BitStream(bits)
        out = list()

        while stream.bitpos < stream.len:
            match = list(self.book.findall(
                stream.peek(8),
                bytealigned=True
            ))
            stream.pos += 8
            out.append(rnd.choice(match))
            text = text[2:]
        return out

    def decode(self, array):
        out = ''
        bs = BitStream(self.book)
        for val in array:
            bs.pos = val
            out += bs.read(8).hex
        return Bits(hex=out).tobytes().decode()

    def h_encode(self, text):
        return ' '.join([
            b85encode(i.to_bytes(self.byte_len, byteorder='big')).decode()
            for i in self.encode(text)
        ])

    def h_decode(self, text):
        chunks = text.split(' ')
        return self.decode([
            int.from_bytes(b85decode(chunk), byteorder='big')
            for chunk in chunks
        ])
