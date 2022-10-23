MONITOR_INTERVAL = 0.5    # Collect stats for each vm and host every `MONITOR_INTERVAL` seconds
TIME_SERIES_LEN = 100
TIME_SERIES_INTERVAL = MONITOR_INTERVAL * TIME_SERIES_LEN

# TODO (vishal): Pass this using OS parameters
VMM_REF_DIR = '/home/vishal/col732/lab3/vmm-reference'