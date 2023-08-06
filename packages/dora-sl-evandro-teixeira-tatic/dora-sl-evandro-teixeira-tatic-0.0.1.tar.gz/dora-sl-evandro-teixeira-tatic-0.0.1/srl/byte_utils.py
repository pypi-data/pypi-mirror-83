
def byte_to_hex_string(b):
    return format(b, '02x')

def byte_array_to_hex_string(ba) :
    return ' '.join(byte_to_hex_string(x) for x in ba)
