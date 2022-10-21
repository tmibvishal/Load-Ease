from time import sleep
from monitor import Monitor
import psutil
from threading import Thread
import config


class CpuMonitor(Monitor):
    def __init__(self, vm_ids=...) -> None:
        super().__init__(vm_ids)

        th = Thread(target=update, args=())
        th.start()

    def update(self):
        #get cpu usage (percentage) of host using psutil
        total_intervals = 0
        while True:
            total_intervals = total_intervals + 1
            host_per_cpu_usage = psutil.cpu_percent(interval=None, percpu=True)
            avg_host_cpu_usage = 0
            for cpu in host_per_cpu_usage:
                avg_host_cpu_usage += cpu
            avg_host_cpu_usage /= len(host_per_cpu_usage)

            # update histogram and timeseries for host
            self.update_histogram(-1, avg_host_cpu_usage, host=True)

            # if total_intervals > config.TIME_SERIES_LEN:
            #     self.host_timeseries.pop(0) 
            #     self.host_timeseries.append(avg_host_cpu_usage)
            # else:
            #     self.host_timeseries[total_intervals-1] = avg_host_cpu_usage


            sleep(config.MONITOR_INTERVAL)


    def get_host_stats() -> Tuple(List[Any], Dict[int : int]):
        pass