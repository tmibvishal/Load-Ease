<img width="407" alt="Logo" src="https://user-images.githubusercontent.com/31121102/198831561-6cb6b1ed-c229-4f3c-bcb3-c0dbd43b9e42.png">

# LoadEase

- Load balancer for inhouse cloud service used for programming labs.  

- Uses [psutil](https://pypi.org/project/psutil/) to monitor the network, memory and cpu usage of each VM and each host.   

- Receives incoming create VM requests and routes them to appropiate hosts.  

- Detects overloaded hosts and identifies VMs to migrate to reduce the load.   

- Makes decisions based on %usage history(timeseries) and histogram(probability distribution of %usage).   

- Based on publication: [Sandpiper](https://dl.acm.org/doi/10.1016/j.comnet.2009.04.014)

## Architecture

Stateless loadbalancer and hotspot detection service. Seamlessly add or remove hosts.  

<img width="659" alt="image" src="https://user-images.githubusercontent.com/74413910/203926003-c2c6ec48-237b-49ce-948b-94cf0c845393.png">


## Demo
 
- [Load Balancing](https://youtu.be/suaSnnCDWnY)
- [Live Migration](https://www.youtube.com/watch?v=ZSCNOWrHCPg): [Codebase](https://github.com/RamneekSingh24/live-migration-rust-vmm)

## Dashboard

<img width="658" alt="image" src="https://user-images.githubusercontent.com/74413910/203926626-bdd2f63f-b1ab-4aae-afff-2c03d7b40aff.png">

<img width="656" alt="image" src="https://user-images.githubusercontent.com/74413910/203926662-474ca024-b6e8-46c4-9c16-83769d011cb1.png">

<img width="668" alt="image" src="https://user-images.githubusercontent.com/74413910/203926703-2e34a129-341e-4082-8484-82448d61eecb.png">
