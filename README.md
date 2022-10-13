# LoadBalancing

# Notes
## CPU Monitoring
### Host  (Ramneek + Tushar + Sahil)
- CPU usage for each VM (just check cpu usage for vm process)
- In CPU monitoring of different VMs, we will not be able to directly monitor the work done during copying from memory to buffers (work done during IO)
    - This work is done by HOST
    - We will assume that no other work is done on host
    - Then we will calculate total IO (Input/Output + Network packets) used in each VM and calculate the total amount of CPU usage in VM as percentage of HOST CPU usage
    - Ignoring Input ourput right now

## Memory Monitoring (Vishal + Saurav)
### Memory Monitoring of VMs
- Total memory for this VM. Done
- Also check total memory usage inside VM

### Memory Monitoring of Host
- Done
- Total swapped memory (Try to keep this as less as possible) -> Try to do it

## Network Monitoring (Amar + Rishi)
- Monitor the tap device (Virtual NIC) in VMM Reference


## Make a histogram (Vishal + Saurav)
Profile generation in Sandpiper
Paper Link: https://www.sciencedirect.com/science/article/pii/S1389128609002035  
We need to dynamically make (they will change) a histogram accumulating resource usage in time intervals making Time Series Profile and also generate Utilization Profile




