#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import utils
from urllib.parse import urlparse, parse_qsl
import copy
import requests as r
import concurrent.futures
import re
from bs4 import BeautifulSoup

proxy = utils.proxy
strings_to_check = ['It looks like you’re lost.', 'Not Found', 'Page Not Found']

class Colors:
    BOLD = '\033[1m'
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'


def Main(url):
    pattern = r'\(([^)]+)\)'
    results = []
    colorx = []
    count = None

    def requester(u):
        headers = {
            "User-Agent": utils.UserAgent,
        }

        try:
            req = r.get(url=u, verify=False, allow_redirects=False, headers=headers, timeout=5)
            found = f"{u} [{len(req.text)}]" + f"[{req.status_code}]"
            soup = BeautifulSoup(req.text, 'html.parser')
            response = len(req.text.splitlines())
            header = len(req.headers)
            count = response + header

            titletag = soup.find('title')
            if titletag:
                title = titletag.get_text()
            else:
                title = None
            if req.status_code != 404 and all(string not in req.text for string in strings_to_check):
                color = Colors.BOLD + Colors.GREEN + "   └── " + Colors.RESET + Colors.CYAN + f"{u} ({count})" + Colors.RESET + Colors.YELLOW + f"[{req.status_code}][{title}]" + Colors.RESET
                results.append(re.sub(r'\033\[\d+m', '', color))
                colorx.append(color)
        except:
            pass
    
    urlX = url.split("\n")
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=utils.Worker) as executor:
            executor.map(requester, urlX)
    except KeyboardInterrupt:
        print("Ctrl+C pressed. Shutting down gracefully...")
        executor.shutdown(wait=False)
    except Exception as e:
        print(e)
    
    all_results = []
    found = []
    for line in results:
        matches = re.findall(pattern, line)
        all_results.extend(matches)
    unieqvalues = set(sorted(all_results))
    for x in unieqvalues:
        for y in results:
            if x in y:
                found.append(y)
                break
    uniqe = set(sorted(found))
    for x in uniqe:
        print(x)

Main(url=utils.stdinX)