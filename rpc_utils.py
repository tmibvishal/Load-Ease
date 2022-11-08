import mon_pb2

def py2grpcStat(host_stats, vm_stats_py):
    time_series, hist = host_stats
    host_stat = mon_pb2.HostStat(
        histogram = hist)
    host_stat.timeseries.extend(time_series)

    vm_stats = []

    for vm_id, (time_series, hist) in vm_stats_py.items():
        vm_stat = mon_pb2.VmStat(vm_id= vm_id, histogram = hist)
        vm_stat.timeseries.extend(time_series)
        vm_stats.append(vm_stat)

    print(host_stat.timeseries)
    stat = mon_pb2.Stat(host = host_stat)
    stat.vms.extend(vm_stats)
    return stat

def grpcStat2py(stat):
    host_stats = (list(stat.host.timeseries), grpcMap2pyDict(stat.host.histogram))
    vm_stats = {}
    for vm in stat.vms:
        vm_stats[vm.vm_id] = (list(vm.timeseries), grpcMap2pyDict(vm.histogram))
    return host_stats, vm_stats

def grpcMap2pyDict(map):
    return {k: v for k, v in map.items()}