#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import argparse
import sys
from utils import utils
import concurrent.futures
from urllib.parse import urlparse
from functools import partial


#Colors...
class Colors:
    BOLD = '\033[1m'
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'

#dirknifer...
def dirkniferX(u, type, method):
    parseurl = urlparse(u)
    host = parseurl.hostname
    from utils import knifer
    if type == "func":
        knifer.Main(h=host, m=method, w=utils.func)
    elif type == "api":
        knifer.Main(h=host, m=method, w=utils.api)
    elif type == "ofa":
        knifer.Main(h=host, m=method, w=utils.onelistforallmicro)
    elif type == "own":
        knifer.Main(h=host, m=method, w=utils.OwnWords)
    elif type == "raft":
        knifer.Main(h=host, m=method, w=utils.raft)
    

    #remove URL After DONE
    if utils.FileX:
        url = u
        utils.removelinefromfile(file_path=utils.FileX, text_to_remove=url)
    else:
        pass

    
#ArgParser...
def argparser():
    currentdirectory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(currentdirectory)
    path = os.path.join(currentdirectory)

    parser = argparse.ArgumentParser(description='Happy Hunting! GOOd luck!')
    parser.add_argument('-f', '--file', dest='file', help='Provide Your Urls file!')
    parser.add_argument('-n', '--number', type=int, default=1, help='Numbers for uses')
    parser.add_argument('-p', '--proxy', action='store_true', help='Proxyifing (default: None)')
    parser.add_argument('-t', '--threads', type=int, default=1, help='Numbers of Threads(default: 1)')
    parser.add_argument('-c', '--concurrency', type=int, default=1, help='Numbers of Concurrents features(default: 1)')
    parser.add_argument('-m', '--method', help="Use The Method To Fuzz[POST,GET,PATCH,PUT++] default is GET")
    parser.add_argument('-func', '--func', action='store_true', help="Fuzz The func Words!")
    parser.add_argument('-api', '--api', action='store_true', help="To fuzz API Words!")
    parser.add_argument('-ofa', '--ofa', action='store_true', help="To fuzz One for all Words")
    parser.add_argument('-r', '--raft', action='store_true', help="To fuzz RaftWords")
    parser.add_argument('-w', '--wordf', help="Use Custom Words To Fuzz")
    parser.add_argument('-all', '--all', action='store_true', help="To fuzz all")
    parser.add_argument('-o', '--out', help='To Save Output')

    
    args = parser.parse_args()

    if args.threads is not None:
        utils.Worker = args.threads
    else:
        utils.Worker = 1

    if args.concurrency is not None:
        utils.Concurrency = args.concurrency
    else:
        utils.Concurrency = 1

    if args.proxy == True:
        utils.proxy = {
            'http': 'http://127.0.0.1:8080',  # Replace with your Burp Suite proxy address
            'https': 'http://127.0.0.1:8080',
            }
    else:
        utils.proxy = None
    
    #args
    if args.file is not None:
        print(Colors.BOLD + Colors.CYAN + "╞── Discovering..." + Colors.RESET)
        utils.FileX = utils.find_file(file_name=args.file)
        if args.method is not None:
            method = args.method
        else:
            method = "GET"
        file = utils.FileX
        urlsX = []

        with open(file, "r") as f:
            urls = f.readlines()
            for x in urls:
                urlsX.append(x)
        newlist = utils.removenewlinesfromlist(urlsX)
        finalurl = set(sorted(urlsX))

        if args.func == True:
            try:
                with concurrent.futures.ProcessPoolExecutor(max_workers=utils.Concurrency) as executor:
                    executor.map(partial(dirkniferX, type="func", method=method), (x.strip() for x in finalurl))
                    executor.shutdown(wait=True)
                    
            except KeyboardInterrupt:
                print("Ctrl+C pressed. Shutting down gracefully...")
                executor.shutdown(wait=False)
            except Exception as e:
                print(e)
        elif args.api == True:
            try:
                with concurrent.futures.ProcessPoolExecutor(max_workers=utils.Concurrency) as executor:
                    executor.map(partial(dirkniferX, type="api", method=method), (x.strip() for x in finalurl))
                    executor.shutdown(wait=True)
            except KeyboardInterrupt:
                print("Ctrl+C pressed. Shutting down gracefully...")
                executor.shutdown(wait=False)
            except Exception as e:
                print(e)
        elif args.ofa == True:
            try:
                with concurrent.futures.ProcessPoolExecutor(max_workers=utils.Concurrency) as executor:
                    executor.map(partial(dirkniferX, type="ofa", method=method), (x.strip() for x in finalurl))
                    executor.shutdown(wait=True)
            except KeyboardInterrupt:
                print("Ctrl+C pressed. Shutting down gracefully...")
                executor.shutdown(wait=False)
            except Exception as e:
                print(e)

        elif args.raft == True:
            try:
                with concurrent.futures.ProcessPoolExecutor(max_workers=utils.Concurrency) as executor:
                    executor.map(partial(dirkniferX, type="raft", method=method), (x.strip() for x in finalurl))
                    executor.shutdown(wait=True)
            except KeyboardInterrupt:
                print("Ctrl+C pressed. Shutting down gracefully...")
                executor.shutdown(wait=False)
            except Exception as e:
                print(e)

        elif args.wordf is not None:
            utils.OwnWords = utils.find_file(file_name=args.wordf)
            try:
                with concurrent.futures.ProcessPoolExecutor(max_workers=utils.Concurrency) as executor:
                    executor.map(partial(dirkniferX, type="own", method=method), (x.strip() for x in finalurl))
                    executor.shutdown(wait=True)
            except KeyboardInterrupt:
                print("Ctrl+C pressed. Shutting down gracefully...")
                executor.shutdown(wait=False)
            except Exception as e:
                print(e)

    elif args.file is None:
        print(Colors.BOLD + Colors.CYAN + "╞── Discovering..." + Colors.RESET)
        if args.method is not None:
            method = args.method
        else:
            method = "GET"

        if args.func == True:
            dirkniferX(u=utils.url, type="func", method=method)
        elif args.api == True:
            dirkniferX(u=utils.url, type="api", method=method)
        elif args.ofa == True:
            dirkniferX(u=utils.url, type="ofa", method=method)
        elif args.wordf is not None:
            utils.OwnWords = utils.find_file(file_name=args.wordf)
            dirkniferX(u=utils.url, type="own", method=method)
        elif args.raft == True:
            dirkniferX(u=utils.url, type="raft", method=method)
        elif args.all == True:
            dirkniferX(u=utils.url, type="func", method=method)
            dirkniferX(u=utils.url, type="api", method=method)
            dirkniferX(u=utils.url, type="ofa", method=method)
            dirkniferX(u=utils.url, type="raft", method=method)
    else:
        pass

if __name__ == '__main__':
    argparser()
    sys.exit(1)
