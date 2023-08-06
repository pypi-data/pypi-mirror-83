
import binascii

class ByteBuffer :

    def __init__(self,byte_array, endianness = "little"):
        self.array = bytearray(byte_array)
        self.endiannes = endianness
        self.bytes_read = 0
        self.original_size = len(self.array)

    def read_int(self, numBytes=4):
        return int.from_bytes(self.read_byte_array(numBytes),self.endiannes)

    def read_long(self):
        return self.read_int(8)

    def read_byte(self):
        return self.read_byte_array(1)[0]

    def read_byte_array(self,size):
        i = self.array[0:size]
        self.array= self.array[size:]
        self.bytes_read += size
        return i

    def read_hex_byte_array(self,size):
        byteArray = self.read_byte_array(size)
        hex_list = []
        for a in byteArray:
            hex_list.append(str(hex(a).replace("0x","ISO-8859-1")))
        return hex_list
