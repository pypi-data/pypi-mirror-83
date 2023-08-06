import os
import requests


class Etherscanner:

    def __init__(self):
        self.uri = 'https://api.etherscan.io/api?'
        self.key = os.getenv('ETHERSCAN_TOKEN')

    def get_abi(self, address):
        """
        Polls etherscan api for abi  and returns the results in a list should there be more than one

        :param address: Contract Address
        :type address: str

        :returns ABI
        :rtype list or str
        """
        uri = self.uri + f'module=contract&action=getabi&address={address}&apiKey={self.key}'

        while True:
            try:
                response = requests.get(uri).json()
            except ConnectionError:
                continue
            else:
                break

        return response['result']

    def get_source(self, address):
        """
        Polls etherscan api for source code and returns the results in a list should there be more than one

        :param address: Contract Address
        :type address: str

        :returns SourceCode or None when non-existent
        :rtype list or None
        """

        uri = self.uri + f'module=contract&action=getsourcecode&address={address}&apiKey={self.key}'
        while True:
            try:
                response = requests.get(uri).json()
            except ConnectionError:
                continue
            else:
                break

        result = response['result']

        if result != '':
            source_code = []
            for r in result:
                source_code.append({'name': r['ContractName'], 'src': r['SourceCode']})
            return source_code
        else:
            return None
