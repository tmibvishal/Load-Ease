import uuid
import redis

MON_PORT = 3413 # TODO (ramneek) sync with LoadBalancing/config.py

MONITOR_INTERVAL = 0.5    # Collect stats for each vm and host every `MONITOR_INTERVAL` seconds
TIME_SERIES_LEN = 100
TIME_SERIES_INTERVAL = MONITOR_INTERVAL * TIME_SERIES_LEN
HOST_ID = str(uuid.uuid4()) # TODO put in redis
rds = redis.Redis()


# TODO (vishal): Pass this using OS parameters
VMM_REF_DIR = '/home/vishal/col732/lab3/vmm-reference'