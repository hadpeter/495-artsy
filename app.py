from flask import Flask, jsonify
import aws_controller

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello_world():
    return "Hello, World!"

@app.route('/get-items')
def get_items():
    return jsonify(aws_controller.get_items())


if __name__ == '__main__':
    app.run(port=8001,host='0.0.0.0')

# [ip address]:8001/hello to get to the hello world endpoint on the ec2
