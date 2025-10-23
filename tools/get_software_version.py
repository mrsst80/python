#!/opt/freeware/bin/python3.9
# 
import subprocess
import shlex
import re

ssh_key = "id_rsa_hmc"
ssh_user = "stefan"
software_name = "nxlog"

def get_servers_list():
   mac_groups = []
   servers = {}
   cmd_get_mac_groups = "lsnim -t mac_group"
   cmd_get_mac_groups = shlex.split(cmd_get_mac_groups)
   mac_group_pattern = r"(.*Group)" 
   #mac_group_pattern = r"(Power8-S824-Ire-Group)" 
   server_pattern = r"(member.*)= (.*)"
  
   mac_groups_tmp = subprocess.run(cmd_get_mac_groups, text=True,capture_output=True) 
   for line in mac_groups_tmp.stdout.split("\n"):
     match = re.search(mac_group_pattern, line)
     if match:
       mac_groups.append(match.group(0))

   for mac_group in mac_groups:
     cmd_get_servers = "lsnim -l {}".format(mac_group)
     cmd_get_servers = shlex.split(cmd_get_servers)
     servers_list = subprocess.run(cmd_get_servers,text=True,capture_output=True)

     for line in servers_list.stdout.split("\n"):
       match = re.search(server_pattern, line)
       if match:
         servers[match.group(2)] = "1"

   return servers

def get_software_version(servers,software_name):
   for server in servers.keys():
     cmd_get_software_version = "rpm -q {}".format(software_name)
     ssh_connect_string = "ssh -T -oStrictHostKeyChecking=no -oConnectTimeout=10 -oBatchMode=yes -i {} {}@{}".format(ssh_key,ssh_user,server)
     ssh_connect_string = shlex.split(ssh_connect_string)

     proceses = [subprocess.Popen(ssh_connect_string) ]

     with subprocess.Popen(ssh_connect_string,
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE,text=True) as ssh:

       out, err = ssh.communicate(cmd_get_software_version)
       print(out)

def run_ssh_parallel(servers,software_name):
   cmd_get_software_version = "rpm -q {}".format(software_name)

   cmd_list = []
   versions = {}
   
   for server in servers:
     cmd = "ssh -T -q -oStrictHostKeyChecking=no -oConnectTimeout=10 -oBatchMode=yes -i {} -l {} {} \"rpm -q {}\"".format(ssh_key,ssh_user,server,software_name)
     cmd_list.append(cmd)

   procs_list = [subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE) for cmd in cmd_list]
   for proc in procs_list:
     proc.wait()
     #print(proc.args[10])
     if proc.returncode == 0:
        ver = proc.stdout.readlines()[0].strip().decode('UTF-8')
        #print(ver)
        versions[proc.args[10]] = ver
        #print(proc.stdout.readlines()[0].strip().decode('UTF-8'))
     else:
        err = proc.stderr.readlines()[0].strip().decode('UTF-8')
        versions[proc.args[10]] = err
        #versions[proc.args[10]] = proc.stderr.readlines()[0].strip().decode('UTF-8')
        #print(proc.stderr.readlines()[0].strip().decode('UTF-8'))
        #print(err)
 
   return versions
def main():
  servers = get_servers_list()
  
  #get_software_version(servers,software_name)
  versions = run_ssh_parallel(servers,software_name)
  #print(versions)
  
  for key in versions.keys():
    print("{},{}".format(key,versions[key]))
  
if __name__ == "__main__":
   main()

