import json


def get_price(date):
    with open('data.json') as file:
        market_data = json.load(file)
        low = 0
        high = len(market_data) - 1
        mid = (low + high) // 2

        while high >= low:
            mid_time = int(market_data[mid]['time'])
            if mid_time == date:
                return market_data[mid]['high']
            elif date < mid_time:
                high = mid - 1
            else:
                low = mid + 1

            mid = (low + high) // 2
        print(market_data[low])
        return market_data[low]['high']
