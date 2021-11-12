#!/usr/bin/env python3
from struct import pack, unpack
import argparse


class LZW:
    @staticmethod
    def compress(data: str) -> str:
        dictionary_size = 256
        dictionary = {chr(i): i for i in range(dictionary_size)}
        bits_number = 16
        max_dict_size = pow(2, bits_number)
        input = ''
        compressed_data = []
        for char in data:
            input_plus_char = input + char
            if input_plus_char in dictionary:
                input = input_plus_char
            else:
                compressed_data.append(dictionary[input])
                if len(dictionary) <= max_dict_size:
                    dictionary[input_plus_char] = dictionary_size
                    dictionary_size += 1
                input = char
        if input in dictionary:
            compressed_data.append(dictionary[input])
        result = []
        for data in compressed_data:
            result.append(pack('>H', int(data)))
        return b''.join(result)

    @staticmethod
    def decompress(compressed_data: str) -> str:
        dictionary_size = 256
        dictionary = dict([(x, chr(x)) for x in range(dictionary_size)])
        bits_number = 16
        max_dict_size = pow(2, bits_number)
        input = ''
        decompressed_data = ''
        data = []
        i = 0
        compressed_data = bytearray(compressed_data)
        while i < len(compressed_data):
            print(chr(compressed_data[i]).encode(), chr(compressed_data[i + 1]).encode())
            # rec = chr(compressed_data[i]).encode() + chr(compressed_data[i + 1]).encode()
            rec = chr(compressed_data[i]).encode() + chr(compressed_data[i + 1]).encode()
            if len(rec) != 2:
                # i += 2
                continue
            (temp, ) = unpack('>H', rec)
            data.append(temp)
            i += 2
        #print(data)
        for code in data:
            if not code in dictionary:
                dictionary[code] = input + input[0]
            decompressed_data += dictionary[code]
            if not len(input) == 0:
                dictionary[dictionary_size] = input + dictionary[code][0]
                dictionary_size += 1
            input = dictionary[code]
        print(decompressed_data)
        return decompressed_data.encode()


class File:
    @staticmethod
    def read(filename: str, bytemode: bool=False) -> str:
        mode = 'rb' if bytemode is True else 'r'
        with open(filename, mode) as file:
            data = file.read()
        return data

    @staticmethod
    def write(filename: str, data: str, bytemode: bool=False) -> None:
        mode = 'wb' if bytemode else 'w'
        with open(filename, mode) as file:
            file.write(data)


def parse_args():
    # To create interface for cli tool
    parser = argparse.ArgumentParser(prog='lzw_algorithm.py',
                                     usage='./lzw_algorithm.py -m compress -if data.txt -of compression.txt',
                                     description='Tool to compress and decompress by LZW algorithm.',
                                     epilog='Written by whatsyourask.')
    parser.add_argument('-m', required=True, help='Compress data from a file.', choices=['compress', 'decompress'], type=str)
    parser.add_argument('-if', required=True, help='Input file.', metavar='INPUT-FILENAME')
    parser.add_argument('-of', required=True, help='Output file.', metavar='OUTPUT-FILENAME')
    argv = vars(parser.parse_args())
    return argv['m'], argv['if'], argv['of']


def main():
    mode, input_file, output_file = parse_args()
    if mode == 'compress':
        data = File.read(input_file)
        compressed_data = LZW.compress(data)
        #print(compressed_data)
        File.write(output_file, compressed_data, True)
    elif mode == 'decompress':
        data = File.read(input_file, True)
        decompressed_data = LZW.decompress(data)
        File.write(output_file, decompressed_data, True)


if __name__=='__main__':
    main()
