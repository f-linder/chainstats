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
    - (index, classification): Tuple of the current index value and it's classification
     (e.g., "Extreme Fear", "Fear", "Neutral", "Greed", "Extreme Greed").
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

        return value, classification

    except requests.RequestException as e:
        return f"Failed with {e}"



