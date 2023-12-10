from flask import Flask, request, jsonify
import sys

sys.path.append("traffic_estimation/")
import estimate as est

app = Flask(__name__)

@app.route('/getTraffic', methods=['GET'])
def getTraffic():
    date = request.args.get('date')
    data = est.get_traffic(date)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)