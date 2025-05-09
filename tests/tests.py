from dydx_v4_wrapper.dydx_v4_wrapper import DYDX
import pprint
import time


# Example usage
async def run_tests():
    # Replace metamask wallet with your generated dYdX wallet address and dYdX generated mnemonic (available from the front-end)
    dydx_client = DYDX(
        wallet_address='',
        mnemonic=''
    )

    time_delay = 3

    # TEST GET PARAMETERS
    print('Getting fee tiers...')
    params = await dydx_client.get_fee_tiers()
    pprint.pprint(params)
    print()
    time.sleep(time_delay)

    print('Getting equity tiers...')
    params = await dydx_client.get_equity_tier()
    pprint.pprint(params)
    print()
    time.sleep(time_delay)

    print('Getting block rate limit...')
    params = await dydx_client.get_equity_tier()
    pprint.pprint(params)
    print()
    time.sleep(time_delay)

    # # TEST MARKET ORDER
    # order_id, transaction = await dydx_client.create_order('ETH-USD', 'BUY', 0.001)
    # pprint.pprint(order_id)
    # pprint.pprint(transaction)
    # time.sleep(time_delay)

    # TEST LIMIT ORDER
    # order_id, transaction = await dydx_client.create_order('ETH-USD', 'BUY', 0.001, price=1700)
    # pprint.pprint(order_id)
    # pprint.pprint(transaction)
    # print()
    # time.sleep(time_delay)

    # TEST ORDER HISTORY
    print("Getting order history...")
    history = await dydx_client.get_order_history()
    pprint.pprint(history)
    print()
    time.sleep(time_delay)

    # TEST FETCH POSITIONS
    print('Getting positions...')
    positions = await dydx_client.get_positions()
    pprint.pprint(positions)
    print()
    time.sleep(time_delay)

    # # TEST ORDER HISTORY FILTER (for fetching initial data and ID)
    # order_data = await dydx_client.get_order_by_components(client_id=order_id.client_id,
    #                                                   order_flags=order_id.order_flags,
    #                                                   clob_pair_id=order_id.clob_pair_id)
    # pprint.pprint(order_data)
    # print()
    # time.sleep(time_delay)

    # TEST FETCH ORDER (for updating)
    # fetched_order = await dydx_client.fetch_order(order_data['id'])
    # pprint.pprint(fetched_order)
    # print()
    # time.sleep(time_delay)

    # # TEST CANCEL ORDER
    # cancel_txn = await dydx_client.cancel_order(order_data)
    # pprint.pprint(cancel_txn)
    # print()
    # time.sleep(time_delay)