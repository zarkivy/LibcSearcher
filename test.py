from LibcSearcher import *
obj = LibcSearcher("fgets", 0x7ff39014bd90)
obj.add_condition("atoi", 218527)
obj.dump("system")

