import os
from etherscan import Etherscanner
from web3 import Web3
from threading import Thread
from writer import Writer
from tqdm import tqdm
from datetime import datetime
from discord import Discord
import time
import logging
import json


class Blockscanner:
    ANDRE = '0x2d407ddb06311396fe14d4b49da5f0471447d45c'

    def __init__(self):
        # web3 http provider
        http_provider = os.getenv('WEB3_HTTP_URI')
        # discord webhook urls
        dwurl = os.getenv('DWURL')
        dwurl2 = os.getenv('DWURL2')
        self.w3 = Web3(Web3.HTTPProvider(http_provider))
        self.e = Etherscanner()
        self.dwurl = dwurl
        self.dwurl2 = dwurl2

    def handle_contract(self, receipt):
        # call writer and write stuff
        logging.info(f'Getting new contract.. {receipt["contractAddress"]}')
        w = Writer(receipt)
        if w.contract_verified is True:
            logging.info(f'\t \t Contract is verified..')
            w.write_all()
            d = Discord()
            d.send_contract(receipt, self.dwurl, self.dwurl2, receipt['contractAddress'])
        else:
            logging.info(f'\t \t Contract not verified...')
            w.add_to_unverifieds()

    def handle_txn(self, txn):
        # get txn receipt and pass it on
        receipt = self.w3.eth.getTransactionReceipt(txn)
        if receipt['contractAddress'] is not None:
            logging.info(f'\t Handling contract: {receipt["contractAddress"]}')
            self.handle_contract(receipt)

    def handle_block(self, block):

        logging.info(f'Handling block: {block["number"]}')

        # creates the process bar
        tbar = tqdm(iterable=block['transactions'], leave=False, colour='blue',
                    desc=f'{datetime.utcfromtimestamp(block["timestamp"])} processing {block["number"]}..')

        # get txn and pass it on
        for txn in block['transactions']:
            try:
                self.handle_txn(txn)
            except:  # if a transaction got dropped and replaced..
                pass

            tbar.update()

        tbar.close()
        return

    def process_blocks(self, block_filter):
        # pass each new block on into a new thread and process it
        while True:
            for b in block_filter.get_new_entries():
                block = self.w3.eth.getBlock(b)
                worker = Thread(target=self.handle_block, args=[block])
                worker.start()

    def get_latest_block(self):
        # get the latest mined block
        block_filter = self.w3.eth.filter('latest')
        self.process_blocks(block_filter)

    def check_unverifieds(self):
        while True:
            uv = Writer.get_unverifieds()
            duv = []
            for i in uv:
                duv.append(json.loads(i))

            for i in duv:
                if time.time() - i['time'] < 216000:
                    bts = Web3.toBytes(hexstr=i['hash'])
                    self.handle_txn(bts)

            time.sleep(60 * 60 * 10)


if __name__ == '__main__':
    logging.basicConfig(filename='../scrapper.log', filemode='w', format='%(thread)d - %(asctime)s - %(message)s',
                        level=logging.INFO)
    b = Blockscanner()
    Thread(target=b.get_latest_block).start()
    Thread(target=b.check_unverifieds).start()
