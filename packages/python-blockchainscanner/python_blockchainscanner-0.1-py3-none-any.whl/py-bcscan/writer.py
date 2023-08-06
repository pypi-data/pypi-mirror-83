import json
from etherscan import Etherscanner
import os
import time

class Writer:
    def __init__(self, receipt):
        self.e = Etherscanner()
        self.receipt = receipt
        self.address = receipt['contractAddress']
        self.deployer = receipt['from']
        self.to = receipt['to']
        self.contract_verified = False

        self.contract_src = []
        for i in self.e.get_source(self.address):
            self.contract_src.append(i)
        if self.contract_src[0]['src'] != '':
            self.contract_verified = True
            self.contract_name = self.contract_src[0]['name']
            self.contract_abi = json.loads(self.e.get_abi(receipt['contractAddress']))
            self.functions = self.format_abi()

    def format_function(self, function):

        """"
        Takes an a dict and formats it into human-readable string
        """

        results = []
        name = function['name']
        inputs = ''
        looped = False
        for j in function['inputs']:
            if looped is True:
                inputs += ', '
            looped = True
            inp_str = f'{j["name"]}:{j["type"]}' if j["name"] != "" else f'{j["type"]}'
            inputs += inp_str

        looped = False
        outputs = ''
        for j in function['outputs']:
            if looped is True:
                inputs += ', '
            looped = True
            outputs += f'{j["type"]}'
        out_str = f' > {outputs}' if outputs != '' else ''
        results.append(f'{name} ({inputs}){out_str}')
        return results

    def format_abi(self):
        """"
        Takes an abi, jsonify it's and processes in order to print out the functions
        """

        non_constants = []
        constants = []

        for i in self.contract_abi:
            if i['type'] == 'function':
                if i.get('stateMutability') == 'nonpayable':
                    non_constants.append(self.format_function(i))
                else:
                    constants.append(self.format_function(i))
        out = ''
        out += 'Write functions:\n'
        for i in non_constants:
            out += '  ' + i[0] + '\n'
        out += 'Read functions:\n'
        for j in constants:
            out += '  ' + j[0] + '\n'

        return out

    def str_src(self):
        loop = False
        _str = ''
        for i in self.contract_src:
            if loop is True:
                _str = i['src']
                _str += '+++++++ \n'
            _str += i['src']
            loop = True
        return _str

    def write_src(self):
        with open(os.path.join(f'../contracts/', f'{self.address}.sol'), 'w') as f:
            f.write(self.str_src())

    def str_nfo(self):
        _str = f'https://etherscan.io/address/{self.address}#code\n\n'
        _str = f'Name: {self.contract_name}\n'
        _str += f'+++++++++++\n'
        _str += f'  Deployer: {self.deployer} \n'
        _str += f'+++++++++++\n'
        _str += self.format_abi()
        return _str

    def write_nfo(self):
        with open(os.path.join(f'../contracts/', f'{self.address}.nfo'), 'w') as f:
            f.write(self.str_nfo())

    def str_abi(self):
        _str = ''
        _str = json.dumps(self.contract_abi)
        return _str

    def write_abi(self):
        with open(os.path.join(f'../contracts/', f'{self.address}.abi'), 'w') as f:
            f.write(self.str_abi())

    def write_all(self):
        self.write_nfo()
        self.write_src()
        self.write_abi()

    def add_to_unverifieds(self):
        ts = time.time()

        d = {"time": ts, "address": self.address, "hash": self.receipt['transactionHash']}
        with open(os.path.join(f'../contracts/', 'not_verified.lst'), 'a') as f:
            f.write(str(d))
            f.write('\n')
        return

    @staticmethod
    def get_unverifieds():
        with open(os.path.join(f'../contracts/', f'not_verified.lst'), 'r+') as f:
            uv = f.read().splitlines()
            f.truncate(0)
        return uv
