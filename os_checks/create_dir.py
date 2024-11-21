#!/usr/bin/env python3

import os

def new_directory(directory, filename):
  # Before creating a new directory, check to see if it already exists
  original_path = os.getcwd()
  if os.path.isdir(directory) == False:
        os.mkdir(directory)


  # Create the new file inside of the new directory
  os.chdir(directory)
  with open (filename, "w") as file:
    #file.write("test")
    pass

  os.chdir(original_path)
  # Return the list of files in the new directory
  return os.listdir(directory)

print(new_directory("PythonPrograms", "script.py"))