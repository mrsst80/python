#!/usr/bin/env python3.12
import re
import sys 

if len(sys.argv) == 1:
  exit("Usage: {} xml_file_name".format(sys.argv[0]))

xml_file = sys.argv[1]


shadow = False

with open(xml_file) as f:
  for line in f:
     s_line = line.strip()
     if "<!--" in s_line and "-->" not in s_line:
        shadow = True
        continue
     elif "-->" in s_line and "<!--" not in s_line:
        shadow = False
     elif "<!--" in s_line and "-->" in s_line:
        continue
     else:
        #if not shadow and len(s_line) > 0:
        if not shadow:
          print(s_line)
