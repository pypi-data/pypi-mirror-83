import sys
import zstandard as zstd
from print_utils import *
from byte_buffer import *


class Block :
    data = None
    lookup = None

    def __init__(self,block_bytes, tag, verbose = True):
        buffer = ByteBuffer(block_bytes)
        block_bytes = {}
        data_bytes = buffer.read_byte_array(tag.compressed_data_size)
        lookup_bytes = buffer.read_byte_array(tag.compressed_lookup_size)

        if len(data_bytes) != tag.compressed_data_size :
            print("Error: wrong data size")
            print("Current data size is " + str(len(data_bytes)) + " but expected " + str(tag["compressed-data-size"]))
            sys.exit(1)
        if len(lookup_bytes) != tag.compressed_lookup_size :
            print("Error: wrong lookup size")
            print("Current lookup size is " + str(len(data_bytes)) + " but expected " + str(tag["compressed-lookup-size"]))
            sys.exit(1)

        if verbose:

            print("LOOKUP DATA ( len = "+str(len(lookup_bytes))+" ) : ")
            printByteArrayToHexString(lookup_bytes)

            print("BLOCK DATA ( len = "+str(len(data_bytes))+" ): ")
            printByteArrayToHexString(data_bytes)

        self.data = self.read_block_data(data_bytes,
        tag.uncompressed_data_size,
        verbose = True)

        self.lookup = self.read_block_lookup(lookup_bytes,
        tag.uncompressed_lookup_size,
        verbose = True)


    def read_block_data(self,data_bytes, uncompressed_size, verbose = True):
        regSep = b"\n"
        fieldSep = b"|"
        db = bytes(data_bytes)
        dctx = zstd.ZstdDecompressor()
        decompressed_data = dctx.decompress(db,max_output_size=uncompressed_size)
        lines = decompressed_data.split(regSep)
        block_metadata_separator = '\u0001'.encode("ISO-8859-1")
        parts = []

        for i in range(len(lines)):
            l = lines[i]
            p = l.split(block_metadata_separator)
            if 5 <= len(p) <= 6 :
                parts.append(p)

        if verbose:
            # print("Parts: ")
            # for p in parts:
            #     print("\nLine : ")
            #     for i in range(min(5,len(p))): 
            #         print("    Part ["+str(i+1)+"]: " + str(p[i]))

            print("\nFound  " + str(len(parts))+ " lines\n")
        
        return parts

    def read_block_lookup(self,lookup_bytes, uncompressed_size, verbose = True):
        print("TODO")
