import mon_pb2

def py2grpcStat(host_stats, vm_stats):
    time_series, hist = host_stats
    host_stat = mon_pb2.HostStat(
        histogram = hist,
        timeseries = time_series
    )

    vm_stats = []

    for vm_id, (time_series, hist) in vm_stats.items():
        vm_stats.append(mon_pb2.VmStat(vm_id= vm_id, histogram = hist, timeseries = time_series))

    stat = mon_pb2.Stat(host = host_stat)
    cpu_stat.vms.extend(vm_stats)
    return stat

def grpcStat2py(stat):
    host_stats = (list(host.timeseries), grpcMap2pyDict(host.histogram))
    vm_stats = {}
    for vm in stat.vms:
        vm_stats[vm.vm_id] = (list(vm.timeseries), grpcMap2pyDict(vm.histogram))
    return host_stats, vm_stats

def grpcMap2pyDict(map):
    return {k: v for k, v in map.items()}