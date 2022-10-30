from redis_functions import get_vm_ids
from setup import setup
from typing import Dict
import time
from threading import Thread
from config import MON_PORT, MONITOR_INTERVAL, HOST_ID
from cpu_monitoring import CpuMonitor
from network_monitoring import NetworkMonitor
from memory_monitoring import MemoryMonitor

from concurrent import futures
import logging
import grpc

import mon_pb2 as mon_pb2
import mon_pb2_grpc as mon_pb2_grpc
from rpc_utils import py2grpcStat


def monitoring_thread(cpu_mon: CpuMonitor, mem_mon: MemoryMonitor, net_mon: NetworkMonitor) -> None:
    while True:
        vm_ids = get_vm_ids()
        cpu_mon.update_vm_ids(vm_ids)
        mem_mon.update_vm_ids(vm_ids)
        net_mon.update_vm_ids(vm_ids)

        host_stat, vm_stats = mem_mon.collect_stats()
        mem_mon.update(host_stat, vm_stats)

        host_stat, vm_stats = net_mon.collect_stats()
        net_mon.update(host_stat, vm_stats)

        host_stat, vm_stats = cpu_mon.collect_stats_network_effect(host_stat, vm_stats)
        cpu_mon.update(host_stat, vm_stats)
        
        time.sleep(MONITOR_INTERVAL)


class MonitoringServicer(mon_pb2_grpc.MonitoringServicer):
    def __init__(self, cpu_mon, mem_mon, net_mon) -> None:
        super().__init__()
        self.cpu_mon = cpu_mon
        self.net_mon = net_mon
        self.mem_mon = mem_mon

    def GetStats(self, request, context):
        cpu_stat = py2grpcStat(self.cpu_mon.get_host_stats(), self.cpu_mon.get_vm_stats())
        net_stat = py2grpcStat(self.net_mon.get_host_stats(), self.net_mon.get_vm_stats())
        mem_stat = py2grpcStat(self.mem_mon.get_host_stats(), self.mem_mon.get_vm_stats())
        return mon_pb2.Stats(cpu=cpu_stat, net=net_stat, mem=mem_stat)



# Main function of Monitoring Service
# This script will run in all hosts.
# And will set up RPC Calls / Other API for the Load balancer to use.
if __name__ == '__main__':
    setup()
    logging.basicConfig()
    cpumon = CpuMonitor()
    netmon = NetworkMonitor()
    memmon = MemoryMonitor()

    th = Thread(target=monitoring_thread, args=(cpumon, memmon, netmon), daemon=True)
    th.start()
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mon_pb2_grpc.add_MonitoringServicer_to_server(
        MonitoringServicer(cpumon, memmon, netmon), server)
    server.add_insecure_port(f'[::]:{MON_PORT}')
    print(f"Listening on port {MON_PORT}...")
    server.start()
    server.wait_for_termination()
