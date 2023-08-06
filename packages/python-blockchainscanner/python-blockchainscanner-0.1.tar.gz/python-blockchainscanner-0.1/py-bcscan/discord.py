from discord_webhook import DiscordWebhook, DiscordEmbed
from writer import Writer


class Discord:
    def __init__(self):
        pass

    def send_transaction(self):
        pass

    def send_contract(self, receipt, url1, url2, address):
        w = Writer(receipt)

        disc_url = f'https://etherscan.io/address/{address}#code'
        dw = DiscordWebhook(title='New contract deployed', url=url1, content='New contract deployed.')
        embed = DiscordEmbed(title=disc_url, color=242424)
        dw.add_embed(embed)
        dw.execute()

        disc_str = f'```{w.str_nfo()}```'
        dw1 = DiscordWebhook(title='New contract deployed!', url=url2, content=disc_str)
        dw1.execute()
