import asyncio
import random
import time
import json
import pprint
from dydx_v4_client import MAX_CLIENT_ID, OrderFlags
from v4_proto.dydxprotocol.clob.order_pb2 import Order
from dydx_v4_client.indexer.rest.constants import OrderType
from dydx_v4_client.indexer.rest.indexer_client import IndexerClient
from dydx_v4_client.network import make_mainnet
from dydx_v4_client.node.client import NodeClient
from dydx_v4_client.node.market import Market
from dydx_v4_client.wallet import KeyPair, Wallet
from decimal import Decimal
import datetime
import aiohttp
from errors import *


"""
    This wrapper was made with help in part by the dydx documentation and the kapa.ai Docs AI.
    Implementation and support is subject to change.
    For more information visit: https://docs.dydx.exchange/
"""


class DYDX:

    def __init__(self, wallet_address, mnemonic):
        self.wallet_address = wallet_address
        self.mnemonic = mnemonic
        self.key_pair = None
        self.indexer_client: IndexerClient = None
        self.node_client = None
        self.wallet = None
        self.sequence = 0

        if not self.wallet_address:
            raise InvalidWallet()

        if not self.mnemonic:
            raise InvalidMnemonic()

        self.rest_indexer = 'https://indexer.dydx.trade'
        self.websocket_indexer = 'wss://indexer.dydx.trade/v4/ws'
        self.node_url = 'dydx-grpc.publicnode.com:443'
        self.grpc_url = 'https://dydx-ops-rest.kingnodes.com'

    async def ensure_initialized_clients(self):
        if not self.indexer_client or not self.node_client:
            await self.initialize_clients()

    async def initialize_clients(self):
        """Initialize clients and wallet"""
        # Connect to mainnet node
        network = make_mainnet(
            rest_indexer=self.rest_indexer,
            websocket_indexer=self.websocket_indexer,
            node_url=self.node_url  # Note: no http/https prefix
        )
        self.node_client = await NodeClient.connect(network.node)

        # Initialize indexer client
        self.indexer_client = IndexerClient(self.rest_indexer)

        # # Initialize key pair
        self.key_pair = KeyPair.from_mnemonic(self.mnemonic)

        # Initialize wallet
        self.wallet = await Wallet.from_mnemonic(
            node=self.node_client,
            mnemonic=self.mnemonic,
            address=self.wallet_address
        )

    async def get_market_data(self, market_id):
        await self.ensure_initialized_clients()

        """Get market data"""
        markets_data = await self.indexer_client.markets.get_perpetual_markets(market_id)
        return markets_data["markets"][market_id]

    async def get_market_info(self, market_id):
        await self.ensure_initialized_clients()

        """Get market information"""
        market_data = self.get_market_data(market_id)
        return market_data["markets"][market_id]['market_info']

    async def get_market_status(self, market_id):
        await self.ensure_initialized_clients()

        market_info = self.get_market_info(market_id)
        status = market_info['status']
        return status

    async def get_market_imf(self, market_id):
        await self.ensure_initialized_clients()

        market_info = self.get_market_info(market_id)
        imf = market_info['initialMarginFraction']
        return imf

    async def get_market_mmf(self, market_id):
        await self.ensure_initialized_clients()

        market_info = self.get_market_info(market_id)
        mmf = market_info['maintenanceMarginFraction']
        return mmf

    async def get_market_tick_size(self, market_id):
        await self.ensure_initialized_clients()

        market_info = self.get_market_info(market_id)
        tick_size = market_info['tickSize']
        return tick_size

    async def get_market_step_size(self, market_id):
        await self.ensure_initialized_clients()

        market_info = self.get_market_info(market_id)
        step_size = market_info['stepSize']
        return step_size

    async def get_block_rate_limit(self, endpoint: str = "/dydxprotocol/clob/block_rate"):
        """
        Query dYdX protocol parameters using a direct HTTP request.

        Args:
            endpoint (str): The specific endpoint to query, defaults to CLOB params

        Returns:
            dict: The JSON response from the endpoint or None if there was an error
        """
        await self.ensure_initialized_clients()

        try:
            # Extract the base URL from the node client's channel
            # This assumes the node client has a channel with a base_url attribute
            # If not, you'll need to construct the URL differently
            base_url = self.grpc_url

            # Ensure the base_url doesn't end with a slash
            if base_url.endswith('/'):
                base_url = base_url[:-1]

            # Ensure the endpoint starts with a slash
            if not endpoint.startswith('/'):
                endpoint = '/' + endpoint

            url = f"{base_url}{endpoint}"

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        print(f"Error querying {url}: HTTP {response.status}")
                        return None

                    return await response.json()

        except Exception as e:
            print(f"Error fetching protocol parameters: {e}")
            return None

    async def get_equity_tier(self, endpoint: str = "/dydxprotocol/clob/equity_tier"):
        """
        Query dYdX protocol parameters using a direct HTTP request.

        Args:
            endpoint (str): The specific endpoint to query, defaults to CLOB params

        Returns:
            dict: The JSON response from the endpoint or None if there was an error
        """
        await self.ensure_initialized_clients()

        try:
            # Extract the base URL from the node client's channel
            # This assumes the node client has a channel with a base_url attribute
            # If not, you'll need to construct the URL differently
            base_url = self.grpc_url

            # Ensure the base_url doesn't end with a slash
            if base_url.endswith('/'):
                base_url = base_url[:-1]

            # Ensure the endpoint starts with a slash
            if not endpoint.startswith('/'):
                endpoint = '/' + endpoint

            url = f"{base_url}{endpoint}"

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        print(f"Error querying {url}: HTTP {response.status}")
                        return None

                    return await response.json()

        except Exception as e:
            print(f"Error fetching protocol parameters: {e}")
            return None

    async def get_fee_tiers(self, endpoint: str = "/dydxprotocol/v4/feetiers/perpetual_fee_params"):
        """
        Query dYdX protocol parameters using a direct HTTP request.

        Args:
            endpoint (str): The specific endpoint to query, defaults to CLOB params

        Returns:
            dict: The JSON response from the endpoint or None if there was an error
        """
        await self.ensure_initialized_clients()

        try:
            # Extract the base URL from the node client's channel
            # This assumes the node client has a channel with a base_url attribute
            # If not, you'll need to construct the URL differently
            base_url = self.grpc_url

            # Ensure the base_url doesn't end with a slash
            if base_url.endswith('/'):
                base_url = base_url[:-1]

            # Ensure the endpoint starts with a slash
            if not endpoint.startswith('/'):
                endpoint = '/' + endpoint

            url = f"{base_url}{endpoint}"

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        print(f"Error querying {url}: HTTP {response.status}")
                        return None

                    return await response.json()

        except Exception as e:
            print(f"Error fetching protocol parameters: {e}")
            return None

    async def create_order(self, market_id, side, size, price=0, slippage=0.01, reduce_only=False, subaccount_number=0):
        """Place a market or limit order on dYdX"""
        await self.ensure_initialized_clients()

        try:
            # Get market information
            market_info = await self.get_market_data(market_id)
            market = Market(market_info)

            # Determine order type and price
            order_type = OrderType.LIMIT if price else OrderType.MARKET

            # Normalize side case to upper
            side = side.upper()

            # Flag for order term length (Long or Short: limit or market)
            order_term = None

            # Get latest oracle price
            oracle_price = Decimal(market.market.get('oraclePrice'))

            # Create target price
            target_price = None

            if order_type == OrderType.MARKET:
                order_term = OrderFlags.SHORT_TERM
                # calculate the nearest target price based on the trade side (for market orders only)
                target_price = Decimal(1.00 + slippage) * oracle_price if side == 'BUY' else Decimal(1 - slippage) * oracle_price

            if order_type == OrderType.LIMIT:
                order_term = OrderFlags.LONG_TERM
                target_price = Decimal(str(price))

                if side == 'BUY' and target_price > oracle_price:
                    raise InvalidPrice(
                        "Buy price too high compared to oracle price",
                        market=market_id,
                        side=side,
                        price=target_price,
                        oracle_price=oracle_price
                    )

                if side == 'SELL' and target_price < oracle_price:
                    raise InvalidPrice(
                        "Sell price too low compared to oracle price",
                        market=market_id,
                        side=side,
                        price=target_price,
                        oracle_price=oracle_price
                    )

            # generate order id
            order_id = market.order_id(self.wallet_address, subaccount_number, random.randint(0, MAX_CLIENT_ID), order_term)

            pprint.pprint(order_id)

            # Determine side
            order_side = Order.Side.SIDE_BUY if side.upper() == 'BUY' else Order.Side.SIDE_SELL

            # Get current block height
            current_block = await self.node_client.latest_block_height()

            # Create order object
            new_order = market.order(
                order_id=order_id,
                order_type=order_type,
                side=order_side,
                size=Decimal(str(size)),
                price=target_price,
                reduce_only=reduce_only,
                time_in_force=Order.TimeInForce.TIME_IN_FORCE_UNSPECIFIED
            )

            if order_type == OrderType.MARKET:
                new_order.good_til_block = current_block + 10
                new_order.time_in_force = Order.TimeInForce.TIME_IN_FORCE_IOC
            if order_type == OrderType.LIMIT:
                # Get current time in seconds since epoch
                current_time = int(time.time())
                # Set goodTilBlockTime (e.g., 24 hours from now)
                good_til_block_time = current_time + (24 * 60 * 60 * 30)  # 30 days from now (max val v4)
                new_order.good_til_block_time = good_til_block_time
                new_order.time_in_force = Order.TimeInForce.TIME_IN_FORCE_POST_ONLY

            # Place the order
            transaction = await self.node_client.place_order(
                wallet=self.wallet,
                order=new_order,
            )

            # Increment wallet sequence for next transaction
            self.wallet.sequence += 1

            if transaction.tx_response.code == 2001:
                raise ReduceOnlyOrderError(tx_hash=transaction.tx_response.txhash,
                                           code=transaction.tx_response.code,
                                           raw_log=transaction.tx_response.raw_log)

            if transaction.tx_response.code == 9003:
                raise ReduceOnlyOrderError(tx_hash=transaction.tx_response.txhash,
                                           code=transaction.tx_response.code,
                                           raw_log=transaction.tx_response.raw_log)

            return order_id, transaction

        except Exception as e:
            print(f"Error placing order: {e}")
            import traceback
            traceback.print_exc()
            return None

    async def get_order_by_components(self, client_id, order_flags, clob_pair_id, subaccount_number=0):
        """
        Fetches the most recent data for an order by matching its components.

        Args:
            client_id (int): The client ID of the order
            order_flags (int): The order flags (e.g., 64 for LONG_TERM)
            clob_pair_id (int): The CLOB pair ID (market ID)
            subaccount_number (int): The subaccount number (default: 0)

        Returns:
            dict: Order data if found, None otherwise
        """
        await self.ensure_initialized_clients()

        try:
            # Ensure indexer client is initialized
            if not self.indexer_client:
                await self.initialize_clients()

            # Get recent orders for the subaccount
            response = await self.indexer_client.account.get_subaccount_orders(
                address=self.wallet_address,
                subaccount_number=subaccount_number,
                limit=100  # Increase if needed to find older orders
            )

            # Find the matching order
            for order in response:
                if (str(order['clientId']) == str(client_id) and
                        str(order['orderFlags']) == str(order_flags) and
                        str(order['clobPairId']) == str(clob_pair_id)):
                    # Since order is already a dictionary, just return it
                    return order

            # No matching order found
            return None

        except Exception as e:
            print(f"Error retrieving order: {e}")
            import traceback
            traceback.print_exc()
            return None

    async def fetch_order(self, order_id: str):
        """
        {'clientId': '1778978642',
          'clientMetadata': '1',
          'clobPairId': '0',
          'createdAtHeight': '43200717',
          'goodTilBlock': '43200723',
          'id': 'f5b992b3-526d-5375-aa9e-a8f46798b7e1',
          'orderFlags': '0',
          'postOnly': False,
          'price': '98614',
          'reduceOnly': False,
          'side': 'BUY',
          'size': '0.0003',
          'status': 'FILLED',
          'subaccountId': 'af709726-bd57-50d5-9210-d4148a1ffcdf',
          'subaccountNumber': 0,
          'ticker': 'BTC-USD',
          'timeInForce': 'IOC',
          'totalFilled': '0.0003',
          'type': 'LIMIT',
          'updatedAt': '2025-04-24T23:53:43.952Z',
          'updatedAtHeight': '43200717'}
        :param order_id:
        :return:
        """

        await self.ensure_initialized_clients()

        order = await self.indexer_client.account.get_order(order_id)
        return order

    async def cancel_order(self, order_data):
        """
        Cancels an order on dYdX.

        Args:
            order_data (dict): Dictionary containing order ID components
                              (client_id, order_flags, clob_pair_id)

        Returns:
            dict: Transaction response
        """
        await self.ensure_initialized_clients()

        try:
            # Extract required fields from order_data
            client_id = order_data.get('clientId') or order_data.get('client_id')
            order_flags = order_data.get('orderFlags') or order_data.get('order_flags')
            clob_pair_id = order_data.get('clobPairId') or order_data.get('clob_pair_id')
            good_til_block = order_data.get('goodTilBlock') or order_data.get('good_til_block')
            good_til_block_time = order_data.get('goodTilBlockTime') or order_data.get('good_til_block_time')

            # Create order_id dictionary
            order_id = {
                'subaccount_id': {
                    'owner': self.wallet_address
                },
                'client_id': int(client_id),
                'order_flags': int(order_flags),
                'clob_pair_id': int(clob_pair_id),
            }

            # For stateful orders (order_flags = 64 for LONG_TERM)
            if int(order_flags) == 64:
                # If goodTilBlockTime is a string (ISO format), convert to timestamp
                if good_til_block_time and isinstance(good_til_block_time, str):
                    datetime_obj = datetime.datetime.fromisoformat(good_til_block_time.replace('Z', '+00:00'))
                    good_til_block_time = int(datetime_obj.timestamp())

                # Get current time if goodTilBlockTime is not provided
                if not good_til_block_time:
                    good_til_block_time = int(time.time()) + (24 * 60 * 60 * 30)  # 90 days from now (max val v4)

                # Cancel the order with goodTilBlockTime
                tx = await self.node_client.cancel_order(
                    wallet=self.wallet,
                    order_id=order_id,
                    good_til_block_time=good_til_block_time
                )
            else:
                # For short-term orders
                tx = await self.node_client.cancel_order(
                    wallet=self.wallet,
                    order_id=order_id,
                    good_til_block=good_til_block
                )

            # Increment wallet sequence for next transaction
            self.wallet.sequence += 1

            return tx

        except Exception as e:
            print(f"Error canceling order: {e}")
            import traceback
            traceback.print_exc()
            return None

    async def get_order_history(self, subaccount_number=0):
        """Get the order history for this wallet's address"""
        await self.ensure_initialized_clients()

        try:
            orders = await self.indexer_client.account.get_subaccount_orders(
                address=self.wallet_address,
                subaccount_number=subaccount_number
            )
            return orders
        except Exception as e:
            print(f"Error getting order history: {e}")
            raise

    async def get_positions(self, subaccount_number=0):
        """
        {'closedAt': None,
                'createdAt': '2025-05-09T19:17:39.436Z',
                'createdAtHeight': '44462866',
                'entryPrice': '2324.4',
                'exitPrice': None,
                'market': 'ETH-USD',
                'maxSize': '0.001',
                'netFunding': '0',
                'realizedPnl': '0',
                'side': 'LONG',
                'size': '0.001',
                'status': 'OPEN',
                'subaccountNumber': 0,
                'sumClose': '0',
                'sumOpen': '0.001',
                'unrealizedPnl': '-0.0004'}
        :param subaccount_number:
        :return:
        """

        """Get the current positions for this wallet"""
        await self.ensure_initialized_clients()

        try:
            positions = await self.indexer_client.account.get_subaccount_perpetual_positions(
                address=self.wallet_address,
                subaccount_number=subaccount_number
            )
            return positions
        except Exception as e:
            print(f"Error getting positions: {e}")
            raise