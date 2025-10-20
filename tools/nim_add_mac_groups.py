# The script adds mac_groups on NIM server based on existing frames and hosted lpars 
import subprocess
import shlex

hmc_hostname = "<HMC_FQDN>"
hmc_username = "<HMC_USERNAME"
ssh_key = "<SSH_KEY"
excluded_lpars = ['cluknim1','clirenim1','VIO','os400']
#print('|'.join(excluded_lpars))

ssh_connect_string = "ssh -T -oStrictHostKeyChecking=no -oConnectTimeout=10 -oBatchMode=yes -i {} {}@{}".format(ssh_key,hmc_username,hmc_hostname)
ssh_cmd_get_frames = "lssyscfg -r sys -F name\n"


popen_args = shlex.split(ssh_connect_string)
#print(popen_args)

def ssh_connect(connect_cmd,ssh_command):

  with subprocess.Popen(popen_args,
			stdin=subprocess.PIPE, stdout=subprocess.PIPE,text=True) as ssh:
    out, err = ssh.communicate(ssh_command)

    CIs = out.split('\n')
    CIs = [x for x in CIs if x.strip()]

  return CIs 

def delete_mac_group(frame):

  cmd_del_mac_group = "nim -o remove {}-Group".format(frame)
  cmd_del_mac_group = shlex.split(cmd_del_mac_group)

  rc = subprocess.run(cmd_del_mac_group,
                       stdout = subprocess.DEVNULL,
                       stderr = subprocess.DEVNULL)

  return rc.returncode

def generate_nim_command(frame,lpars):

   mac_group_name = frame + "-Group"
   lpars_string = ' -a add_member='.join(lpars)

   add_mac_group = "nim -o define -t mac_group -a add_member=" + lpars_string + " " + mac_group_name

   return add_mac_group

def exec_cmd_return_code(command):

   rc = subprocess.run(command,
                       stdout = subprocess.DEVNULL,
                       stderr = subprocess.DEVNULL)

   return rc.returncode

def main():

  frames = ssh_connect(popen_args,ssh_cmd_get_frames)

  if frames: 
    for frame in frames:
      cmd_check_mac_groups = "lsnim -l {}-Group".format(frame)
      if exec_cmd_return_code(shlex.split(cmd_check_mac_groups)) == 0:
        print("Deleteing mac_group {}-Group".format(frame))
        delete_mac_group(frame)
        
      ssh_cmd_get_lpars = "lssyscfg -r lpar -m {} -F name,state,lpar_env | grep Running | grep -Ev '{}' | cut -d'-' -f1".format(frame,'|'.join(excluded_lpars)) 
      lpars = ssh_connect(ssh_connect_string,ssh_cmd_get_lpars)
      lpars = [x.lower() for x in lpars] 
      if lpars:
        cmd_add_mac_group = shlex.split(generate_nim_command(frame,lpars))
        if exec_cmd_return_code(cmd_add_mac_group) == 0:
          print("mac_group {}-Group added sucessfully.".format(frame))

if __name__ == "__main__":
   main()
