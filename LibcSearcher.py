import requests, json


API_FIND = 'https://libc.rip/api/find' 
API_LIBC = 'https://libc.rip/api/libc/'
HEADERS = {'Content-Type': 'application/json'}


class LibcSearcher() :
    def __init__(self, symbol_name:str=None, address:int=None) :
        self.constraint = {}
        self.libc_list  = []
        self.the_libc   = None

        if (symbol_name is not None) and (address is not None) :
            self.add_condition(symbol_name, address)


    def __len__(self) :
        if self.libc_list == [] :
            self.query_libc()
        if self.the_libc is None :
            return len(self.libc_list)
        else : 
            return 1


    def __iter__(self) :
        if self.libc_list == [] :
            self.query_libc()
        return iter([ libc['id'] for libc in self.libc_list ])


    def add_condition(self, symbol_name:str, address:int) -> None :
        self.constraint[symbol_name] = address
        self.libc_list = []
        self.the_libc  = None


    def dump(self, symbol_name:str) -> int :
        if self.libc_list == [] :
            self.query_libc()
        if self.the_libc is None :
            self.determine_the_libc()
        return self.query_symbol(libc_id = self.the_libc['id'], symbol_name = symbol_name)


    def determine_the_libc(self) -> None :
        if len(self.libc_list) == 0 :
            print("\x1b[1;31m" + "[+] No libc satisfies constraints." + "\x1b[0m")
            exit()

        elif len(self.libc_list) == 1 :
            self.the_libc = self.libc_list[0]

        else :
            print("\x1b[33m" + 
                    "[+] There are multiple libc that meet current constraints :" + 
                    "\x1b[0m")
            self.select_libc()
    

    def select_libc(self, chosen_index=-1) :
        if chosen_index == -1 :
            self.query_libc()
            for index, libc in enumerate(self.libc_list) :
                print(str(index) + " - " + libc['id'])
            chosen_index = input("\x1b[33mChoose one : \x1b[0m")
        try :
            self.the_libc = self.libc_list[int(chosen_index)]
        except IndexError :
            print("\x1b[1;31m[+] Index out of bound!\x1b[0;m")
            self.select_libc()
                


    def query_libc(self) :
        payload = {
                    "symbols" : 
                    { s_name: hex(s_addr) for s_name, s_addr in self.constraint.items() }
                  }
        result = requests.post(API_FIND, data=json.dumps(payload), headers=HEADERS)
        self.libc_list = json.loads(result.text)


    def query_symbol(self, libc_id:str, symbol_name:str) -> int :
        payload = {
                    "symbols": 
                    [ symbol_name ]
                  }
        result = requests.post(API_LIBC+libc_id, data=json.dumps(payload), headers=HEADERS)
        return int(json.loads(result.text)['symbols'][symbol_name], 16)