MON_PORT = 3413 # TODO (ramneek) sync with LoadBalancing/config.py

HOST_PEAK_NET_BIT_RATE = 1024 * 1024 * 50 # 50 MBps  TODO (rishi) setup this value using IPERF tool.

MONITOR_INTERVAL = 0.5    # Collect stats for each vm and host every `MONITOR_INTERVAL` seconds
TIME_SERIES_LEN = 100
TIME_SERIES_INTERVAL = MONITOR_INTERVAL * TIME_SERIES_LEN

# TODO (vishal): Pass this using OS parameters
VMM_REF_DIR = '/home/vishal/col732/lab3/vmm-reference'