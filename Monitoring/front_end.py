from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def show_resource_util():
    cpu_percentage = 100
    memory_percentage = 50
    net_usage = 1000
    data_unit = "MB"
    
    hosts_id = [0,1,2,3]
    hosts_vms_num = [1,1,1,1]
    hosts_cpu_usage = [20.00,30.00,40.00,50.00]
    hosts_mem_usage = [80.00,85.55,90.50,12.6]
    hosts_net_usage = [100,200,300,128]
    #assuming that 0th host has 0th to hosts_vms_num index values
    
    total_ids=7
    vms_id = list(range(total_ids));
    vms_cpu_usage = [20 for i in range(total_ids)]
    vms_mem_usage = [80 for i in range(total_ids)]
    vms_net_usage = [100 for i in range(total_ids)];
    #histogram dict datas
    host_cpu_usage_histogram = {0 : 0.05, 5 : 0.05, 10: 0.05, 15: 0.05, 20: 0.05, 25: 0.05, 30: 0.05, \
        35: 0.05, 40: 0.05, 45: 0.05, 50: 0.05, 55: 0.05, 60: 0.05, 65: 0.05, \
            70: 0.05, 75: 0.05, 80: 0.05, 85: 0.05, 90: 0.05, 95: 0.05, 100: 0.05}
    host_mem_usage_histogram = {0 : 0.2, 5 : 0.2, 10: 0.2, 15: 0.2, 20: 0.2, 25: 0.2, 30: 0.2, \
        35: 0.2, 40: 0.2, 45: 0.2, 50: 0.2, 55: 0.2, 60: 0.2, 65: 0.2, \
            70: 0.2, 75: 0.2, 80: 0.2, 85: 0.2, 90: 0.2, 95: 0.2, 100: 0.2}
    host_net_usage_histogram = {0 : 0.1, 5 : 0.1, 10: 0.1, 15: 0.1, 20: 0.1, 25: 0.1, 30: 0.1, \
        35: 0.1, 40: 0.1, 45: 0.1, 50: 0.1, 55: 0.1, 60: 0.1, 65: 0.1, \
            70: 0.1, 75: 0.1, 80: 0.1, 85: 0.1, 90: 0.1, 95: 0.1, 100: 0.1}
    cpu_usage = []
    for key,value in host_cpu_usage_histogram.items():
        cpu_usage.append({"usage":key,"probability":value});
    mem_usage = []
    for key,value in host_mem_usage_histogram.items():
        mem_usage.append({"usage":key,"probability":value});
    network_usage = []
    for key,value in host_net_usage_histogram.items():
        network_usage.append({"usage":key,"probability":value});

    return render_template('resource_usage.html',avg_cpu_usage=cpu_percentage, mem_usage=memory_percentage,net_usage=net_usage,data_unit=data_unit,hosts_id = hosts_id, hosts_vms_num = hosts_vms_num, hosts_cpu_usage = hosts_cpu_usage, hosts_mem_usage = hosts_mem_usage, hosts_net_usage = hosts_net_usage,hosts_num=len(hosts_id),vms_id=vms_id, vms_cpu_usage=vms_cpu_usage,vms_mem_usage=vms_mem_usage, vms_net_usage=vms_net_usage,vm_num=len(vms_id),histogram_cpu_usage=cpu_usage,histogram_mem_usage=mem_usage,histogram_net_usage=network_usage)

if __name__ == '__main__':
    app.run()
