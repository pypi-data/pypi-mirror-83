from byte_utils import *
import pprint

def print_dict(d) :
    pp = pprint.PrettyPrinter(depth=4)
    f = str(pp.pformat(d))
    print(f + "\n")

def pretty_print_byte_array(ba) :
    for i in range(len(ba)) :
        if(i % 16 == 0):
            print()
        print(" " + str(ba[i]).ljust(3),end="")

def printByteArrayToHexString(ba) :
    for i in range(len(ba)):
        if i % 16 == 0:
            print()
        print(" " + format(ba[i], '02x'),end="")
    print("\n")