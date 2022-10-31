import logging
import json
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


@app.route('/')
def home():
    return 'Welcome to main host. With Regards - Load Balancing Team'


@app.route('/create', methods=['POST'])
def create_vm():
    req = request.get_json()
    req = json.loads(req)
    print(req)
    # req['mem'], req['cpu'], req['disk'], req['image_path']
    new_req = {
        'cpu_snapshot_path': './cpu_snap.snap',
        'memory_snapshot_path': './mem_snap.snap',
        'kernel_path': './bzimage-hello-busybox',
        'tap_device': 'vm_tap_100',
        'resume': False
    }
    resp = requests.post(f'10.237.23.38:8011/create', json=new_req).json()
    resp = json.loads(resp)
    print(resp)
    # resp should be a dictionary of format {'rpc_port': , 'pid'}
    if resp:
        return jsonify(
            {'success': True, 'response': 'Successful', 'vm_attrs': {}})
    else:
        return jsonify(
            {'success': False, 'response': 'Successful', 'vm_attrs': {}})


@app.route('/ping')
def ping():
    return {'success': True}


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(host='0.0.0.0', debug=True, port=8000, threaded=True)
