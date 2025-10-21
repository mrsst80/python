#!/opt/freeware/bin/python3.9
# 
import subprocess
import shlex
import re

#ssh_connect_string = "ssh -T -oStrictHostKeyChecking=no -oConnectTimeout=10 -oBatchMode=yes -i {} {}@{}".format(ssh_key,hmc_username,hmc_hostname)

def get_servers_list():
   mac_groups = []
   servers = []
   cmd_get_mac_groups = "lsnim -t mac_group"
   cmd_get_mac_groups = shlex.split(cmd_get_mac_groups)
   mac_group_pattern = r"(.*Group)" 
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
         servers.append(match.group(2))

   return servers

print(get_servers_list())
  

