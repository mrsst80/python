#!/usr/bin/env python3.12
import re
import sys 

#print(len(sys.argv))
if len(sys.argv) < 2:
  exit("Usage: sys.argv[0] xml_file_name")

xml_file = sys.argv[1]


shadow = False

with open(xml_file) as f:
  for line in f:
     s_line = line.strip()
     if "<!--" in s_line:
        shadow = True
        continue
     elif "-->" in s_line:
        shadow = False
     else:
        #if not shadow and len(s_line) > 0:
        if not shadow:
          print(s_line)
