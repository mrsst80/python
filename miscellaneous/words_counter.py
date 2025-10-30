#!/usr/bin/env python3.12
import sys
import os
import re
from collections import Counter

target = sys.argv[1]

if len(sys.argv) == 1:
  exit("Usage: {} file_name\n".format(sys.argv[0]))


def parse_file(file: str) -> dict:
  results = {}
  stats = os.stat(file)
  print("os stats {}".format(stats))

  try:

    with open(file,"r") as f:
      for line in f:
        line_split = line.strip().split()

        if len(line_split) == 0:
          continue
        for word in line_split:
          word = re.sub(r"\W","", word)
          if len(word) > 2 and word.isalpha():
            word = word.lower()
            results[word] = 1 + results.get(word, 0)
  except Exception as error:
    print("Cannot proceed {}".format(error))
  
  return results

print(Counter(parse_file(target)).most_common(10))

