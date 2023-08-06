
from print_utils import *
from tag import *
from block import *
from segment import *

def read_full_dat_file(file_path,verbose = True):

    file_bytes = bytes(open(file_path, "rb").read())
    file_len = len(file_bytes)

    if verbose:
        print("\n\nFILE : ( len = "+str(file_len)+" ) "+ str(file_path) +" \n")
        printByteArrayToHexString(file_bytes)
        print("\n")

    pointer = file_len
    if verbose:
        print("POINTER (end) : " + str(pointer) + "\n")

    results = []
    while(pointer >= 0):
        
        # Jumping the pointer upwards to read a tag: 
        pointer -= 256
        if verbose:
            print("POINTER (tag): " + str(pointer) + "\n")
        tag_bytes = file_bytes[pointer:]
        tag = Tag(file_path,tag_bytes, verbose = verbose)
        

        if verbose:
            print("PARSED METADATA / tag ( len = "+str(len(tag_bytes))+" ) : \n")
            print(str(tag))

        block_size = tag.get_block_size()
        
        # Jumping the pointer upwards to read a block: 
        pointer -= block_size
        if verbose:
            print("POINTER (block): " + str(pointer) + "\n")
            
        block_bytes = file_bytes[pointer:pointer+block_size]
        block = Block(block_bytes,tag)

        segment = Segment(tag,block)
        results.append(segment)

    return results
        


def read_dat_file(  file_path,
                    verbose = True, 
                    tag_func = None, 
                    block_data_func = None, 
                    block_lookup_func = None ,
                    end_func = None):

    file_bytes = bytes(open(file_path, "rb").read())
    file_len = len(file_bytes)

    if verbose:
        print("\n\nFILE : ( len = "+str(file_len)+" ) "+ str(file_path) +" \n")
        printByteArrayToHexString(file_bytes)
        print("\n")

    pointer = file_len
    if verbose:
        print("POINTER (end) : " + str(pointer) + "\n")

    results = []
    while(pointer >= 0):
        
        # Jumping the pointer upwards to read a tag: 
        pointer -= 256
        if verbose:
            print("POINTER (tag): " + str(pointer) + "\n")
        tag_bytes = file_bytes[pointer:]
        tag = Tag(file_path,tag_bytes, verbose = verbose)
        
        if tag_func is not None:
            tag_func(tag)

            if verbose:
                print("PARSED METADATA / tag ( len = "+str(len(tag_bytes))+" ) : \n")
                print(str(tag))

            if block_data_func is not None or block_lookup_func is not None:

                block_size = tag.get_block_size()
                
                # Jumping the pointer upwards to read a block: 
                pointer -= block_size
                if verbose:
                    print("POINTER (block): " + str(pointer) + "\n")
                    
                block_bytes = file_bytes[pointer:pointer+block_size]
                block = Block(block_bytes,tag)

                block_data_func(block.data)
                block_lookup_func(block.lookup)

    return results