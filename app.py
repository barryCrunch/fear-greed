import requests
import math
import json
from utils import get_price
import time

UPPER = 85
LOWER = 15
MULTIPLIER = .01


def generate_trade_signals():
    # Call Fear/Greed API and then take data and order it from oldest -> newest
    response = requests.get(
        "https://api.alternative.me/fng/?limit=0")
    data = response.json()['data']
    data.reverse()

    trades = []
    for i in data:
        value = int(i['value'])
        timestamp = i['timestamp']
        if value >= UPPER:
            trades.append({'trade': 'SELL', 'timestamp': int(timestamp)})
        elif value <= LOWER:
            trades.append({'trade': 'BUY', 'timestamp': int(timestamp)})
    return trades


def buy(timestamp, amount):
    price = get_price(timestamp)
    return amount / price, price


def sell(timestamp, amount):
    price = get_price(timestamp)
    return amount * price


def print_results(balance, crypto_balance, total_trades, average_purchase_price, purchases=[1000 for x in range(0, 50000, 1000)]):
    with open('data.json') as file:
        market_data = json.load(file)
        crypto_total_usd = crypto_balance * market_data[-1]['high']
        print(f'Current USD Balance: ${balance}')
        print(f'Current Crypto Balance: ETH{crypto_balance}')
        print(f'Current Total Balance: ${balance + crypto_total_usd}')
        print(f'Total Trades: {total_trades}')
        print(f'Average Purchase Price: {average_purchase_price}')
        print(f'Total Purchase Amounth: {sum(purchases)}')


# The control case is a DCA purchasing $1000 worth of
# crypto over the same periord of time
def calculate_control(start_time):
    balance = 50000
    crypto_balance = 0
    current_time = start_time
    total_trades = 0
    prices = []
    while balance > 0 and current_time < math.floor(time.time()):
        purchase, price = buy(current_time, 1000)
        crypto_balance = crypto_balance + purchase
        current_time = current_time + 2419200
        balance = balance - 1000
        total_trades += 1
        prices.append(price)
    print_results(balance, crypto_balance, total_trades,
                  (sum(prices)/len(prices)))


def main():
    crypto_balance = 0
    balance = 50000
    signals = generate_trade_signals()
    prices = []
    for signal in signals:

        # If signals a buy action, purchase an amount
        # equal to your MULTIPLIER * balance
        if signal['trade'] == "BUY":
            amount = balance * MULTIPLIER
            purchase, price = buy(signal['timestamp'], amount)
            crypto_balance = crypto_balance + purchase
            balance = balance - amount
            prices.append(price)

        # If signals a sell action, purchase an amount
        # equal to your MULTIPLIER * crypto_balance
        elif signal['trade'] == "SELL":
            amount = crypto_balance * MULTIPLIER
            balance = balance + sell(signal['timestamp'], amount)
            crypto_balance = crypto_balance - amount

    print('*' * 10)
    print('Algo Results')
    print('*' * 10)
    print_results(balance, crypto_balance, len(signals),
                  (sum(prices)/len(prices)), purchases=prices)

    print('*' * 10)
    print('Control DCA')
    print('*' * 10)
    calculate_control(signals[0]['timestamp'])


if __name__ == "__main__":
    main()
