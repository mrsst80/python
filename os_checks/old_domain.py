#!/usr/bin/env python3
import csv
import re


def contains_domain(address, domain):
  pattern = domain
  if re.search(pattern, address) is None:
     return False
  else:
     return True
  """Returns True if the email address contains the given domain,
    in the domain position, false if not."""
  #return False

def replace_domain(address, old_domain, new_domain):
  """Replaces the old domain with the new domain in
    the received address."""
  regex = r"([\w.%+-]+@)([\w.%+-]+)" 
  replace_regex = r"\g<1>" + new_domain
  result = re.search(regex, address)
  return re.sub(regex, replace_regex, address)


def main():
  """Processes the list of emails, replacing any instances of the
    old domain with the new domain."""
with open('domain_users.csv') as csvfile:
    spamreader = csv.reader(csvfile)
    with open('domain_users_new.csv', 'w', newline='\n') as csvfilenew:
      writer = csv.writer(csvfilenew, delimiter=',')
      for row in spamreader:
          if contains_domain(row[1].strip(), 'abc.edu'):
            address = replace_domain(row[1].strip(), 'abc.edu', 'xyz.edu')
            writer.writerow((row[0], address))
            print('{}, {}'.format(row[0], address))
          else:
            writer.writerow((row[0], row[1]))
            print('{}, {}'.format(row[0], row[1]))
            
main()