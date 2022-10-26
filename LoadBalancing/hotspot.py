# This file will always run in the background, detect whether the current host
# is overloaded, and then move the appropriate VM to other host.

# Daemon threads are used for long-running background tasks
# Program can exit if all the other threads are done running

# Reference for daemon thread: SuperFastPython.com
import xmlrpc.client
from time import sleep
from random import random
from threading import Thread

from LoadBalancing.config import rds, HOTSPOT_THRESHOLD


def background_task():
  while True:
    # Get host monitor proxies from Redis
    rpc_mon_host_proxies = rds.smembers('rpc_mon_host_proxies')
    overload = False
    vol = []
    hosts = []
    for host_proxy in rpc_mon_host_proxies:
      # TODO (Vishal): Make sure that xmlrpc servers are only sending 32 bit integers
      # host_proxy example for local host http://localhost:8000/
      with xmlrpc.client.ServerProxy(host_proxy) as proxy:
        memory = proxy.memory()[0]
        network = proxy.network()[0]
        cpu = proxy.cpu()[0]

        if cpu > HOTSPOT_THRESHOLD or memory > HOTSPOT_THRESHOLD or network > HOTSPOT_THRESHOLD:
          overload = True

        vol.append((host_proxy, 1 / ((1 - cpu) * (1 - memory) * (1 - network))))

    if overload:
      # Now you need to do the Migration to balance the VMs properly
      vol.sort(key=lambda x: x[1], reverse=True)
      if len(vol) > 1:
        # Where to transfer: Lowest volume host would be perfect for transfer
        # Which VM to transfer. One with the highestr VSM on the highest volume host

        best = None
        lowest_size = -1
        from_host = vol[0][0]
        for vm_id in rds.hget(name=f'vms_on_host', key=from_host):
          d = rds.hgetall(name='vm_info:{vm_id}')
          # Pick the smallest size VM
          if best is None or lowest_size > d['size']:
            best = vm_id
            lowest_size = d['size']

        # You need to migrate the VM with id best
        target_host = vol[-1]

        # Check if vm with id best can be moved to target_host
        # And then start the migration
      

    sleep(5)  # Wait for 5 sec


# create and start the daemon thread
print('Starting background task...')
daemon = Thread(target=background_task, daemon=True, name='Monitor')
daemon.start()
print('Hotspot Detection Started')
while True:
  value = random() * 5
  sleep(value)
