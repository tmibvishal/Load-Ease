import logging
from flask import Flask, request, jsonify
import json

from balancer import create_vm


app = Flask(__name__)


@app.route('/')
def home():
  return 'Welcome to main host. With Regards - Load Balancing Team'


# Create VM - PUT Request
#
# Request
# - Json = {'mem': , 'cpu': , 'disk': , 'image_path': }
# - image_path is the kernel path
#
# Response
# - Json = {'success': , 'response': , 'vm_id': , 'host_proxy': , 'pid': , 'tap_device': , 'vm_attrs' :}
@app.route('/create', methods=['POST'])
def create_vm():
  req = request.get_json()
  req = json.loads(req)
  vm_attrs = create_vm(req)
  print(vm_attrs)
  return jsonify({'success': True, 'response': 'Successful', 'vm_attrs': vm_attrs})


@app.route('/ping')
def ping():
  return {'success': True}

if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  # app.add_url_rule(
  #   "/user_data/<name>", endpoint="view_file", build_only=True
  # )
  app.run(host='0.0.0.0', debug=True, port=8000, threaded=True)
