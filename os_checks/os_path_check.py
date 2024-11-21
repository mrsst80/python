#!/usr/bin/env python3
import os

my_file = "joro.txt"

if (not os.path.exists("joro.txt")):
    f = open("joro.txt", "w")
    f.write("bace joro")
else:
    print("File exists!")