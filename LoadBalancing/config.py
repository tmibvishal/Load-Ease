import redis
from threading import Lock

# rpc_mon_host_proxys = []  # TODO (Ramneek)
# This will now be present in Redis
# In this way, you can keep starting new hosts and hotspot will dynamically
# manage it
MON_PORT = 3413

HOTSPOT_THRESHOLD = 0.80
NUM_INTERVALS_FOR_HOTSPOT_CONF = 10

rds = redis.Redis()
# Run redis on main server
# We can also use proper distributed databases for better fault tolerance

migration_lock = Lock()
