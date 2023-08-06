import math

from vocompr.utils import hex_to_bits, bytes_to_hex, char_string_size_in_bits, int_to_bits, hex_to_bytes, bits_to_hex


def vocompr(input_str):
    vocabulary = {}
    for i, c in enumerate(input_str):
        if c not in vocabulary:
            vocabulary[c] = len(vocabulary)

    vocabulary_reverse = {i: char for char, i in vocabulary.items()}
    digest_elem_size = math.ceil(math.log(len(vocabulary), 2))
    data = [int_to_bits(vocabulary[char], digest_elem_size) for char in input_str]
    digest_data = "".join(data)
    digest_voc = ""
    for i in range(len(vocabulary)):
        digest_voc += int_to_bits(ord(vocabulary_reverse[i]), 256)

    res_bits = "1" + int_to_bits(len(vocabulary), 256) + digest_voc + digest_data
    return hex_to_bytes(bits_to_hex(res_bits))


def unvocompr(input_b):
    input = hex_to_bits(bytes_to_hex(input_b))
    input = input[input.index("1") + 1:]
    len_voc_end = 256
    len_voc = int(input[:len_voc_end], 2)
    digest_voc_end = 256 + 256 * len_voc
    digest_voc = input[256: digest_voc_end]

    vocabulary_reverse = {}
    for i in range(len_voc):
        bits = digest_voc[i * 256: i * 256 + 256]
        charcode = int(bits, 2)
        char = chr(charcode)
        vocabulary_reverse[i] = char

    digest_data = input[digest_voc_end:]
    content = ""
    digest_elem_size = math.ceil(math.log(len(vocabulary_reverse), 2))
    n_chars = len(digest_data) / digest_elem_size
    int_n_chars = int(n_chars)
    assert (n_chars == int_n_chars)
    for i in range(int_n_chars):
        bits = digest_data[i * digest_elem_size:i * digest_elem_size + digest_elem_size]
        char_index = int(bits, 2)
        char = vocabulary_reverse[char_index]
        content += char

    return content


def compression_rate(s):
    return len(hex_to_bits(bytes_to_hex(vocompr(s)))) / char_string_size_in_bits(s)
