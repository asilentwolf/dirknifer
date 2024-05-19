#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import re
from urllib.parse import urlparse
import os
from random import choice
import json
import warnings

warnings.filterwarnings("ignore")    # ignor any warning in teminal
stdinX = "" 

if sys.stdin.isatty():
    pass
else:
   stdinX = sys.stdin.read().strip()

Worker = None   #Threads
proxy = None
FileX = None
Concurrency = None
TargetHost = None
rawff = None
url = None
pathx = None
header = None
host = None
body = None
datax = None
query = None
frag = None
netloc = None
scheme = None
OwnWords = None

try:
    pattern = re.compile(r'^http')
    if sys.stdin.isatty():
        pass
    elif pattern.match(stdinX):
        url = stdinX
        parsed_url = urlparse(url)
        pathx = parsed_url.path
        host = parsed_url.hostname
        getquery = parsed_url.query
        frag = parsed_url.fragment
        netloc = parsed_url.netloc
        scheme = parsed_url.scheme
        pass
    else:
        pass
except NameError as e:
    print(f"An error occurred: {e}")


#Variables
proxy = {
    'http': 'http://127.0.0.1:8080',  # Replace with your Burp Suite proxy address
    'https': 'http://127.0.0.1:8080',
}

currentdirectory = os.path.dirname(os.path.realpath(__file__))
os.chdir(currentdirectory)
agenttext = os.path.join(currentdirectory, '..', 'db/User-Agents.txt')
func = os.path.join(currentdirectory, '..', 'db/func.txt')
onelistforallmicro = os.path.join(currentdirectory, '..', 'db/onelistforallmicro.txt')
raft = os.path.join(currentdirectory, '..', 'db/raft.txt')
api = os.path.join(currentdirectory, '..', 'db/API.txt')

with open(agenttext, "r") as file:
    user_agents = [line.strip() for line in file]
    UserAgent = choice(user_agents)


#Useful functions
def find_file(file_name):
    # Search for the file in the entire filesystem
    for root, dirs, files in os.walk('/'):  
        if file_name in files:
            return os.path.join(root, file_name)
            break  # Once the file is found, exit the loop
    return None

def removenewlinesfromlist(lst):
    return [string.replace('\n', '') for string in lst]

def removelinefromfile(file_path, text_to_remove):
    # Read the file and store its lines
    with open(file_path, 'r') as file:
        lines = file.readlines()
    # Remove the lines containing the specific text
    modified_lines = [line for line in lines if text_to_remove not in line]
    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(modified_lines)