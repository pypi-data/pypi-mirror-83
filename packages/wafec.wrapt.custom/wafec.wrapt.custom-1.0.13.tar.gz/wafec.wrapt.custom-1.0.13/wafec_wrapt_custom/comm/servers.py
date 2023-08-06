from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello'


@app.route('/api/proxy/interception/add', methods=['POST'])
def add_proxy_interception_info():
    ps = request.json['ps']
    name = request.json['name']
    x = request.json['x']
    print(f'PROXY INFO ps={ps}, name={name}, x={x}')
    return jsonify({'success': True})


def start_server():
    app.run(host="0.0.0.0", port=6543)


if __name__ == '__main__':
    start_server()
