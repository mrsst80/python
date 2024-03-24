#!/usr/bin/python
#
#
# This script defines enforcement mode of policies under default archetypes in Azure CAF terraform module.
# By default all policies are set in DoNotEnforce mode. This can be overwritten if archetype name is added to enforced_policies list.
# List of additional policies, not included in default archetype policy list are defined in include_policies dictionary.
# Before using the script the caf_ver variable needs to be defined to version the script will use.
# The output of the script is in terraform syntax.
#
#
import os
import json
import git
import shutil

# Change to caf module version you want to use as a source
caf_ver = "<Define CAF Module version>"
local_path = "azurerm-caf-enterprise-scale"

# List of 
include_policies = { 'es_online': ['Audit-AppGW-WAF'], 'es_root': ['Deny-Public-Endpoints','Enforce-TLS-SSL','Deny-Resource-Locations'] }

# List of archetypes, which policies are Enforced.
enforced_policies = [ 'es_sandboxes' ]

def clone_git_repo():
  repo_url = "https://github.com/Azure/terraform-azurerm-caf-enterprise-scale.git"  
  if not os.path.exists(local_path):
    repo = git.Repo.clone_from(repo_url, local_path)    	   
  else:
    repo = git.Repo(local_path)

  repo.head.reference = repo.commit(caf_ver)
  repo.head.reset(index=True, working_tree=True)

  return 0

def print_json():
  main_path = local_path + "/modules/archetypes/lib/archetype_definitions/"
  files = os.listdir(main_path)

  print("locals {")
  print("\tpolicy_enforce_mode = {".expandtabs(2))
  for archetype in files:
    full_path = main_path + archetype
    f = open(full_path)
    data = json.load(f)
    for key in data:
      print("\t\t".expandtabs(2)+ key + " = {")

      for i in data[key]:
        if i == "policy_assignments":
          for j in data[key][i]:
            if key in enforced_policies:
              enforce_policy = "true"
            else:
              enforce_policy = "false"
            print("\t\t\t\t".expandtabs(2) + j + "\t\t\t= " + enforce_policy )

      if key in include_policies.keys():
        for j in include_policies[key]:
            if key in enforced_policies:
              enforce_policy = "true"
            else:
              enforce_policy = "false"
            print("\t\t\t\t".expandtabs(2) + j + "\t\t\t= " + enforce_policy )
      print("\t\t}".expandtabs(2))

  print("\t}".expandtabs(2))
  print("}")
  
  return 0

def remove_repo_dir():
  shutil.rmtree(local_path)

def main():
  clone_git_repo()
  print_json()
  remove_repo_dir()

if __name__ == "__main__":
  main()

