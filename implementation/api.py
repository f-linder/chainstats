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


def clear_database():
    table_btc_dominance.delete_many({})
    table_total_mcap.delete_many({})
    table_leaderboard.delete_many({})
    table_fear_and_greed.delete_many({})
    table_tvl.delete_many({})


def populate_database():
    btc_dominance = data.get_btc_dominance()
    btc_dominance['timestamp'] = time.time()
    table_btc_dominance.insert_one(btc_dominance)

    total_mcap = data.get_total_market_cap()
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
    total_mcap = table_total_mcap.find()[0]

    saved_time = total_mcap['timestamp']
    current_time = time.time()

    # interval of time in seconds to pass before the value is updated
    interval = 60 * 10  # 10 min

    if current_time - saved_time >= interval:
        table_total_mcap.delete_many({})
        total_mcap = data.get_total_market_cap()
        total_mcap['timestamp'] = current_time
        table_total_mcap.insert_one(total_mcap)

    return jsonify({key: value for key, value in total_mcap.items()
                    if key != 'timestamp' and key != '_id'}), 200


@app.route('/metrics/fear_and_greed', methods=['GET'])
def metrics_fear_and_greed():
    fear_and_greed = table_fear_and_greed.find()[0]

    saved_time = fear_and_greed['timestamp']
    time_until_update = int(fear_and_greed['time_until_update'])
    current_time = time.time()

    if current_time - saved_time >= time_until_update:
        table_fear_and_greed.delete_many({})
        fear_and_greed = data.get_fear_and_greed()
        fear_and_greed['timestamp'] = current_time
        table_fear_and_greed.insert_one(fear_and_greed)

    return jsonify({key: value for key, value in fear_and_greed.items()
                    if key != 'timestamp' and key != '_id'}), 200


@app.route('/metrics/btc_dominance', methods=['GET'])
def metrics_btc_dominance():
    btc_dominance = table_btc_dominance.find()[0]

    saved_time = btc_dominance['timestamp']
    current_time = time.time()

    # interval of time in seconds to pass before the value is updated
    interval = 60 * 10  # 10 min

    if current_time - saved_time >= interval:
        table_btc_dominance.delete_many({})
        btc_dominance = data.get_btc_dominance()
        btc_dominance['timestamp'] = current_time
        table_total_mcap.insert_one(btc_dominance)

    return jsonify({key: value for key, value in btc_dominance.items()
                    if key != 'timestamp' and key != '_id'}), 200


@app.route('/stats/leaderboard', methods=['GET'])
def stats_leaderboard():
    leaderboard = table_leaderboard.find()[0]

    saved_time = leaderboard['timestamp']
    current_time = time.time()

    # interval of time in seconds to pass before the value is updated
    interval = 60 * 10  # 10 min

    if current_time - saved_time >= interval:
        table_leaderboard.delete_many({})
        leaderboard = data.get_leaderboard(100)
        leaderboard = {'timestamp': current_time,
                       'leaderboard': leaderboard}
        table_leaderboard.insert_one(leaderboard)

    return jsonify({key: value for key, value in leaderboard.items()
                    if key != 'timestamp' and key != '_id'}), 200


@app.route('/stats/tvl', methods=['GET'])
def stats_tvl():
    tvl = table_tvl.find()[0]

    saved_time = tvl['timestamp']
    current_time = time.time()

    # interval of time in seconds to pass before the value is updated
    interval = 60 * 10  # 10 min

    if current_time - saved_time >= interval:
        table_tvl.delete_many({})
        tvl = data.get_leaderboard(100)
        tvl = {'timestamp': current_time,
               'tvls': tvl}
        table_leaderboard.insert_one(tvl)

    return jsonify(tvl['tvls']), 200


if __name__ == '__main__':
    clear_database()
    populate_database()
    app.run(debug=True, port=8087)
