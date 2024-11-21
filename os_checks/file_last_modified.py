import os
import datetime

def file_date(filename):
  # Create the file in the current directory
  with open("newfile.txt", "w"):
    pass
  timestamp = os.path.getmtime(os.path.join(os.getcwd(), filename))
  # Convert the timestamp into a readable format, then into a string
  t = datetime.datetime.fromtimestamp(timestamp)
  print(t.date())
  # Return just the date portion 
  # Hint: how many characters are in “yyyy-mm-dd”? 
  #return ("{___}".format(___))
  return(timestamp)

print(file_date("newfile.txt")) 
# Should be today's date in the format of yyyy-mm-dd