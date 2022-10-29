import logging
import subprocess

from flask import Flask, request, jsonify

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
  print(req)

  # Start the VM
  p = subprocess.Popen(['./target/debug/vmm-reference', '--kernel path=./bzimage-hello-busybox', '--net tap=vmtap100', '--memory size_mib=512'], cwd=VMM_REF_DIR)



  return jsonify({'success': True, 'response': 'Successful', 'vm_id': 1, 'host_proxy': '', 'pid': 1, 'tap_device': '', 'vm_attrs': {}})


@app.route('/ping')
def ping():
  return {'success': True}

if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  # app.add_url_rule(
  #   "/user_data/<name>", endpoint="view_file", build_only=True
  # )
  app.run(host='0.0.0.0', debug=True, port=8000, threaded=True)
