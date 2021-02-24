import requests, json, sys


API_FIND = 'https://libc.rip/api/find' 
API_LIBC = 'https://libc.rip/api/libc/'
HEADERS = {'Content-Type': 'application/json'}


class LibcSearcher(object) :
    def __init__(self, symbol_name:str=None, address:int=None) :
        self.constraint = {}
        self.libc_list  = []
        self.the_libc   = None

        if (symbol_name is not None) and (address is not None) :
            self.add_condition(symbol_name, address)


    def add_condition(self, symbol_name:str, address:int) -> None :
        self.constraint[symbol_name] = address
        self.libc_list = []
        self.the_libc  = None


    def dump(self, symbol_name:str) -> int :
        if self.libc_list == [] :
            self.query_libc()
        if self.the_libc is None :
            self.choose_libc()
        if symbol_name not in self.constraint :
            self.query_symbol(libc_id = self.the_libc['id'], symbol_name = symbol_name)
        return self.constraint[symbol_name]


    def choose_libc(self) -> None :
        if len(self.libc_list) == 0 :
            print("\x1b[1;31m" + "No libc satisfies constraints." + "\x1b[0m")
            sys.exit()

        elif len(self.libc_list) == 1 :
            self.the_libc = self.libc_list[0]

        else :
            print("\x1b[33m" + 
                  "There are multiple libcs that satisfy current constraints :" + 
                  "\x1b[0m")
            for index, libc in enumerate(self.libc_list) :
                print(str(index) + " - " + libc['id'])
            choosen_index = input("\x1b[36mChoose one : \x1b[0m")
            self.the_libc = self.libc_list[int(choosen_index)]


    def query_libc(self) :
        payload = {
                    "symbols" : 
                    { s_name: hex(s_addr) for s_name, s_addr in self.constraint.items() }
                  }
        result = requests.post(API_FIND, data=json.dumps(payload), headers=HEADERS)
        self.libc_list = json.loads(result.text)


    def query_symbol(self, libc_id:str, symbol_name:str) -> int :
        payload = {"symbols": [symbol_name]}
        result = requests.post(API_LIBC+libc_id, data=json.dumps(payload), headers=HEADERS)
        self.constraint[symbol_name] = int(json.loads(result.text)['symbols'][symbol_name], 16)