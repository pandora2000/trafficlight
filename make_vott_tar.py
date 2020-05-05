import os
vott_path = '/home/zb/works/test/trafficlight'
os.system(f'rm -rf {vott_path}/vott.tar; cd {vott_path}; tar -cvf vott.tar target vott-target; mv {vott_path}/vott.tar ~/downloads/')
