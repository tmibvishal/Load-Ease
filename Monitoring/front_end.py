from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def show_resource_util():
    cpu_percentage = 100
    memory_percentage = 50
    net_usage = 1000
    data_unit = "MB"

    vms_id = [0,1,2,3];
    vms_cpu_usage = [20.00,30.00,40.00,50.00];
    vms_mem_usage = [80.00,85.55,90.50,12.6];
    vms_net_usage = [100,200,300,128];

    return render_template('resource_usage.html',avg_cpu_usage=cpu_percentage, mem_usage=memory_percentage,net_usage=net_usage,data_unit=data_unit,vms_id=vms_id, vms_cpu_usage=vms_cpu_usage,vms_mem_usage=vms_mem_usage, vms_net_usage=vms_net_usage,vm_num=len(vms_id))

if __name__ == '__main__':
    app.run()