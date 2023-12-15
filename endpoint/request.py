""" Module for handling requests to the API """

from flask import Flask, request, jsonify
from flask_cors import CORS

from estimation import estimate
from scraper import file_operations

app = Flask(__name__)
CORS(app)


@app.route('/getTraffic', methods=['GET'])
def get_traffic():
    """ Used for getting all the available dates for traffic estimation. """
    date = request.args.get('date')
    data = estimate.get_traffic(date)
    return jsonify(data)


@app.route('/getDates', methods=['GET'])
def get_dates():
    """ Reads argument from the request and returns the estimated traffic. """
    date_from, date_to = file_operations.get_file_dates()
    traffic_df = file_operations.read_df_from_file(
        f"results/traffic/{date_from}_to_{date_to}.csv", silent=False)
    traffic_df.drop(columns=["count"], inplace=True)

    return jsonify(traffic_df.to_dict(orient="records"))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
