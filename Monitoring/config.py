import uuid
import os
MON_PORT = 3413 # TODO (ramneek) sync with LoadBalancing/config.py

HOST_PEAK_NET_BIT_RATE = 1024 * 1024 * 50 # 50 MBps,  setup will overwrite this

MONITOR_INTERVAL = 0.5    # Collect stats for each vm and host every `MONITOR_INTERVAL` seconds
TIME_SERIES_LEN = 100
TIME_SERIES_INTERVAL = MONITOR_INTERVAL * TIME_SERIES_LEN
HOST_ID = str(uuid.uuid4()) # TODO put in redis

# TODO (vishal): Pass this using OS parameters
# VMM_REF_DIR = os.environ['VMM_REF']
# '/home/vishal/col732/lab3/vmm-reference'
_script_dir = os.path.dirname(os.path.realpath(__file__))
VMM_REF_DIR = os.path.join(_script_dir, '../vmm-reference')
