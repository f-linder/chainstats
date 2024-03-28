import requests


def get_btc_dominance():
    """
    Retrieves the Bitcoin dominance percentage from the CoinMarketCap API.

    Returns:
    - dict: {'btc_dominance': int}
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

        return {'btc_dominance': btc_dominance}

    except requests.RequestException as e:
        return f"Failed with {e}"


def get_total_market_cap():
    """
    Retrieves the total cryptocurrency market capitalization in USD from the CoinMarketCap API.

    Returns:
    - dict: {'total_mcap': int}
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

        return {'total_mcap': market_cap}

    except requests.RequestException as e:
        return f"Failed with {e}"


def get_fear_and_greed():
    """
    Retrieves the current Fear and Greed Index from the Alternative.me API.

    Returns:
    - dict: {'value': int, 'value_classification': str}
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
        classification = data[0]['value_classification']

        return {'value': value, 'value_classification': classification}

    except requests.RequestException as e:
        return f"Failed with {e}"


def get_leaderboard(num):
    """
    Retrieves information from the top num cryptocurrencies sorted by
    market capitalization from the CoinMarketCap API.

    Parameters:
    - num: Size of the returned leaderboard

    Returns:
    - list: [{'name': str,
              'symbol': str,
              'price': float,
              'percent_change_24h': float,
              'market_cap': float,
              'market_cap_dominance': float,
              'volume_24h': float,
              'volume_change_24h': float},
              'logo_url': str]
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
        # name, symbol, price usd, % price change 24h, market cap, % market cap dominance, volume 24h, volume change 24h, logo_url
        for c in data:
            d = {'name': c['name'],
                 'symbol': c['symbol'],
                 'price': c['price'],
                 'percent_change_24h': c['percent_change_24h'],
                 'market_cap': c['market_cap'],
                 'market_cap_dominance': c['market_cap_dominance'],
                 'volume_24h': c['volume_24h'],
                 'volume_change_24h': c['volume_change_24h'],
                 'logo_url': f'https://assets.coincap.io/assets/icons/{c["symbol"]}@2x.png'}

            ret.append(d)

        return ret

    except requests.RequestException as e:
        return f"Failed with {e}"


def get_total_value_locked():
    """
    Retrieves the total value locked in different blockchains.

    - list: [{'name': str,
              'tvl': float,
              'logo_url': str}]
    - str: Error message in case of failure.
    """

    url = 'https://api.llama.fi/protocols'

    header = {
        'Accepts': 'application/json',
    }

    try:
        response = requests.get(url, headers=header)
        response.raise_for_status()
        data = response.json()

        ret = []
        for entry in data:
            name = entry['name']
            tvl = entry['tvl']
            logo = entry['logo']
            ret.append({'name': name, 'tvl': tvl, 'logo_url': logo})

        return ret

    except requests.RequestException as e:
        return f"Failed with {e}"
