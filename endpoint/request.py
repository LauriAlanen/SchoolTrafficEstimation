from flask import Flask, request, jsonify
from flask_cors import CORS
import sys

sys.path.append("traffic_estimation/")
sys.path.append("scraper/")

import estimate as est
import fileOperations as fo

app = Flask(__name__)
CORS(app)

@app.route('/getTraffic', methods=['GET'])
def getTraffic():
    date = request.args.get('date')
    data = est.get_traffic(date)
    
    return jsonify(data)


@app.route('/getDates', methods=['GET'])
def getDates():
    date_from, date_to = fo.get_file_dates()
    traffic_df = fo.read_df_from_file(f"results/traffic/{date_from}_to_{date_to}.csv", silent=False)
    traffic_df.drop(columns=["count"], inplace=True)

    return jsonify(traffic_df.to_dict(orient="records"))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)