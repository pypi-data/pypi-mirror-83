from print_utils import *
from byte_buffer import *
import pprint

class XDRRuntimeException(Exception):
    pass

class Tag : 

    def __init__(self,file_path, tag_bytes, verbose = True):
        if verbose:
            print("\n\nCURRENT TAG (len = "+str(len(tag_bytes))+") : ===============================================================")        
            printByteArrayToHexString(tag_bytes)
            print("\n")

        buf = ByteBuffer(tag_bytes)
        
        self.compressed_data_size = buf.read_int()
        self.compressed_lookup_size = buf.read_int()
        self.uncompressed_data_size = buf.read_int()
        self.uncompressed_lookup_size = buf.read_int()
        self.number_lines = buf.read_int()
        self.hash_bytes = buf.read_byte_array(16)
        self.optmized = (buf.read_byte() != 0)
        aux = buf.read_int(numBytes=1)
        self.min_ordenator = buf.read_byte_array(79)[0:aux]
        aux = buf.read_int(numBytes=1)
        self.max_ordenator = buf.read_byte_array(79)[0:aux]
        buf.read_byte_array(8) # ModifDate
        self.set_compression_algorithm( buf.read_byte() & 0x000000FF )
        buf.read_byte_array(1) # RegSep
        self.min_reg_date = None
        self.max_reg_date = None
        aux = buf.read_long()
        if aux != 0 :
            self.min_reg_date = str(aux)
        aux = buf.read_long()
        if aux != 0 :
            self.max_reg_date = str(aux)
        buf.read_byte_array(21) # Unused
        self.checksum = buf.read_byte_array(4)
        self.extra_ident = buf.read_int()
        self.ident = buf.read_int()
        self.origin_file_name = file_path

        self.check_ident()


    def __str__(self):
        pp = pprint.PrettyPrinter(depth=4)
        f = str(pp.pformat(self.to_dict()))
        return f + "\n"

    def set_compression_algorithm(self,i : int):
        compression_algs = {}
        compression_algs[0] = "BZ2"
        compression_algs[1] = "LZ4"
        compression_algs[2] = "XZ"
        compression_algs[3] = "ZSTD"
        compression_algs[255] = "NO_COMPRESSION"
        compression_algs[None] = "UNKNOWN"
        self.compression_algorithm = compression_algs[i]

    def check_ident(self):
        if self.extra_ident != 0xA4158F35 or self.ident != 0xD7CD78E3:
            raise XDRRuntimeException("Tag on check_ident(): Invalid block info identifier")

    def to_dict(self):
        return self.__dict__

    def get_block_size(self):
        return self.compressed_data_size + self.compressed_lookup_size

