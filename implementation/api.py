from flask import Flask, jsonify
from pymongo import MongoClient
import time
import data

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['chainstats']

# bitcoin dominance in percent
# {'timestamp': float, btc_dominance': int}
table_btc_dominance = db['btc_dominance']

# total crypto marketcap
# {'timestamp': float, 'total_mcap': int}
table_total_mcap = db['total_mcap']

# fear and greed index
# {'timestamp': float, 'value': int, 'value_classifying': str}
table_fear_and_greed = db['fear_and_greed']

# information about the top marketcap currencies
# [{'timestamp': float,
#   'name': str,
#   'symbol': str,
#   'price': float,
#   'percent_change_24h': float,
#   'market_cap': float,
#   'market_cap_dominance': float,
#   'volume_24h': float,
#   'volume_change_24h': float,
#   'logo_url': str}]
table_leaderboard = db['leaderboard']

# total value locked for different exchanges
# {'timestamp': float, 'name': str, 'tvl': float, 'logo_url': str}
table_tvl = db['tvl']


def populate_database():
    btc_dominance = data.get_btc_dominance()
    btc_dominance['timestamp'] = time.time()
    table_btc_dominance.insert_one(btc_dominance)

    total_mcap =  data.get_total_market_cap()
    total_mcap['timestamp'] = time.time()
    table_total_mcap.insert_one(total_mcap)

    fear_and_greed = data.get_fear_and_greed()
    fear_and_greed['timestamp'] = time.time()
    table_fear_and_greed.insert_one(fear_and_greed)

    leaderboard = data.get_leaderboard(100)
    leaderboard = {'timestamp': time.time(),
                   'leaderboard': leaderboard}
    table_leaderboard.insert_one(leaderboard)

    tvl = data.get_total_value_locked()
    tvl = {'timestamp': time.time(),
           'tvls': tvl}
    table_tvl.insert_one(tvl)


@app.route('/', methods=['GET'])
def index():
    return 'Welcome to the chainstats API!'


@app.route('/metrics/total_mcap', methods=['GET'])
def metrics_total_mcap():
    # in seconds
    interval = 3600


if __name__ == '__main__':
    populate_database()
    app.run(debug=True)
