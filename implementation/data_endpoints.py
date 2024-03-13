import requests


def get_btc_dominance():
    """
    Retrieves the Bitcoin dominance percentage from the CoinMarketCap API.

    Returns:
    - float: Bitcoin dominance percentage.
    - str: Error message in case of failure.
    """

    url = 'https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest'

    header = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': '30a9d585-12b3-4885-95ed-c94d8c5cf8b8',
    }

    try:
        response = requests.get(url, headers=header)
        response.raise_for_status()
        data = response.json()
        btc_dominance = data['data']['btc_dominance']
        return btc_dominance

    except requests.RequestException as e:
        return f"Failed with {e}"


def get_total_market_cap():
    """
    Retrieves the total cryptocurrency market capitalization in USD from the CoinMarketCap API.

    Returns:
    - float: Total market capitalization in USD.
    - str: Error message in case of failure.
    """

    url = 'https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest'

    header = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': '30a9d585-12b3-4885-95ed-c94d8c5cf8b8',
    }

    try:
        response = requests.get(url, headers=header)
        response.raise_for_status()
        data = response.json()
        market_cap = data['data']['quote']['USD']['total_market_cap']
        return market_cap

    except requests.RequestException as e:
        return f"Failed with {e}"


def get_fear_and_greed():
    """
    Retrieves the current Fear and Greed Index from the Alternative.me API.

    Returns:
    - index: Current index value
    - str: Error message in case of failure.
    """

    url = 'https://api.alternative.me/fng/'

    header = {
      'Accepts': 'application/json',
    }

    try:
        response = requests.get(url, headers=header)
        response.raise_for_status()
        data = response.json()
        # data = [{value, value_classification, timestamp, time_until_update}]
        data = list(data['data'])
        value = data[0]['value']

        return value

    except requests.RequestException as e:
        return f"Failed with {e}"


def get_leaderboard(num):
    """
    Retrieves information from the top num cryptocurrencies sorted by
    market capitalization from the CoinMarketCap API.

    Parameters:
    - num: Size of the returned leaderboard

    Returns:
    - list: Where each element is another list of form
    [name, symbol, price usd, % price change 24h, market cap, % market cap dominance, volume 24h, % volume change 24h]
    - str: Error message in case of failure.
    """

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    header = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '30a9d585-12b3-4885-95ed-c94d8c5cf8b8',
    }

    params = {
        'limit': num,
        'sort': 'market_cap',
    }

    try:
        response = requests.get(url, headers=header, params=params)
        response.raise_for_status()
        data = response.json()
        data = list(data['data'])

        ret = []
        # name, symbol, price usd, % price change 24h, market cap, % market cap dominance, volume 24h, volume change 24h
        for c in data:
            name = c['name']
            symbol = c['symbol']
            price = c['quote']['USD']['price']
            percent_change_24h = c['quote']['USD']['percent_change_24h']
            market_cap = c['quote']['USD']['market_cap']
            market_cap_dominance = c['quote']['USD']['market_cap_dominance']
            volume_24h = c['quote']['USD']['volume_24h']
            volume_change_24h = c['quote']['USD']['volume_change_24h']

            ret.append([name, symbol, price, percent_change_24h, market_cap, market_cap_dominance, volume_24h, volume_change_24h])

        return ret

    except requests.RequestException as e:
        return f"Failed with {e}"
