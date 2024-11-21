#!/usr/bin/env python3
import sys
import re
import os

def find_error(log_file):
    error_message = input("Enter the error message: ")
    cron_pattern = r"CRON\[\d+\]"
    
    output = []
    with open(log_file, 'r', encoding='UTF-8') as f:
        for line in f:
            if re.search(cron_pattern, line):
                if re.search(error_message, line):
                    output.append(line.strip())
                    #print(line.strip())

    return output


if __name__ == "__main__":
    log_file = sys.argv[1]
    returned_errors = find_error(log_file)
    for e in returned_errors:
        print(e)
    
    
