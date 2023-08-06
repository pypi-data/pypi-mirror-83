def int_to_bits(i, fill_to_n=None):
    bits_str = ""
    while i != 0:
        bits_str = str(i % 2) + bits_str
        i = i // 2
    return ((fill_to_n - len(bits_str)) if fill_to_n is not None else 0) * "0" + bits_str


def bits_to_int(b):
    return int(b, 2)


def bits_to_hex(bits):
    res = hex(int(bits, 2))[2:]
    return ("0" if len(res) % 2 else "") + res


def hex_to_bits(h):
    return bin(int(h, 16))[2:]


def hex_to_bytes(h):
    return bytes.fromhex(h)


def bytes_to_hex(b):
    return b.hex()


def char_string_size_in_bits(s):
    return 8 * len(s)
