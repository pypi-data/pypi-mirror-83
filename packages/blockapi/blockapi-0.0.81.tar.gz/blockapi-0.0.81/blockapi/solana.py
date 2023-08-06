import asyncio
import websockets
from jsonrpcclient.clients.websockets_client import WebSocketsClient


async def main():
    async with websockets.connect('ws://api.mainnet-beta.solana.com/') as ws:
        response = await WebSocketsClient(ws).request(
            'accountSubscribe',
            '2rPn2kDECLyjY5xLzZ4FqAuE27ApFa8ZpPBw48ZCo31y',
            {"encoding": "base58", "commitment": "max"}
        )
        print(response.data)
        while True:
            print(await ws.recv())


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
    asyncio.get_event_loop().run_forever()
