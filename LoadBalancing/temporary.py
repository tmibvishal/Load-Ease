import logging
import json
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


@app.route('/')
def home():
    return 'Welcome to main host. With Regards - Load Balancing Team'

PORT = 8011
@app.route('/create', methods=['POST'])
def create_vm():
    req = request.get_json()
    req = json.loads(req)
    print(req)
    # req['mem'], req['cpu'], req['disk'], req['image_path']
    # new_req = {
    #     'cpu_snapshot_path': './cpu_snap.snap',
    #     'memory_snapshot_path': './mem_snap.snap',
    #     'kernel_path': './bzimage-hello-busybox',
    #     'tap_device': 'vm_tap_100',
    #     'resume': False
    # }
    resp = requests.post(f'10.237.23.38:{PORT}/create', json=req).json()
    resp = json.loads(resp)
    return resp

@app.route('/snapshot', methods=['POST'])
def create_vm():
    req = request.get_json()
    req = json.loads(req)
    print(req)
    resp = requests.post(f'10.237.23.38:{PORT}/snapshot', json=req).json()
    resp = json.loads(resp)
    print(resp)
    return resp


@app.route('/ping')
def ping():
    return {'success': True}


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(host='0.0.0.0', debug=True, port=5010, threaded=True)
