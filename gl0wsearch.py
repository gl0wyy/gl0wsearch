#!/usr/bin/env python3
import argparse
from termcolor import colored
import sys
import requests
from concurrent.futures import ThreadPoolExecutor
import pyfiglet
from pyfiglet import figlet_format

class color:
   PURPLE = '\033[1;35;48m'
   CYAN = '\033[1;36;48m'
   BOLD = '\033[1;37;48m'
   BLUE = '\033[1;34;48m'
   GREEN = '\033[1;32;48m'
   YELLOW = '\033[1;33;48m'
   RED = '\033[1;31;48m'
   BLACK = '\033[1;30;48m'
   UNDERLINE = '\033[4;37;48m'
   END = '\033[1;37;0m'

parser = argparse.ArgumentParser(usage="%(prog)s [dir|vhost] [options]", add_help=False)


parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit')
parser.add_argument('-u', '--url', help="Target Url or IP Address(e.g): -u http://127.0.0.1", metavar='')
parser.add_argument('-w', '--wordlist', help="Path to wordlist (e.g) -w /usr/share/wordlists/rockyou.txt", metavar='')
parser.add_argument('-e', '--extensions', help="File extensions (e.g) -e php,txt,zip", metavar='')
parser.add_argument('-sf', '--codes', help="Filter status codes (e.g) -sf 404,503 (Default is 503,500,410,404,302)", default="503,500,410,404,302", metavar='')
parser.add_argument('-t', '--threads', help="Set worker thread(s) number (e.g) -t 20 (Default is 15)", default=15, metavar='')
if len(sys.argv) < 3:
    parser.print_help()
    sys.exit()

mode = sys.argv.pop(1)

if mode not in ("dir", "vhost"):
    parser.print_help()
    sys.exit()

args = parser.parse_args()
dir_mode = (True if mode == 'dir' else False)
vhost_mode = (True if mode == 'vhost' else False)

print()
print()
print(f'{color.PURPLE}{colored(figlet_format("gl0wsearch"))}{color.END}')

if dir_mode:
    wordlist = open(args.wordlist)
    url = str(args.url)
    directory = [newline.strip() for newline in wordlist.readlines()]
    codes = [int(code) for code in args.codes.split(",")]
    threads = int(args.threads)

    print(f'{color.GREEN}Url:{color.END}{url}')
    print(f'{color.GREEN}Wordlist:{color.END}{args.wordlist}')
    print(f'{color.GREEN}Threads:{color.END}{threads}')
    print("")
    print(f"{color.YELLOW}Filtering Status Codes{color.END} {color.RED}{codes}{color.END}")
    print("")
    print(f'{color.GREEN}Url\t\t\t\t\t   Status\t\t\t Length{color.END}')

    if not (url.startswith ('http://') or url.startswith ('https://')):
        url = 'http://' + url

    def dirbrute(directory):
        width = 30
        if not len(directory):
            return
        
        if not directory.startswith('#'):
            r = requests.get("{}/{}".format(url, directory))
                    
            if r.status_code not in codes:
                response = f"/{directory}"
                print(f"{response:<{width}} {r.status_code:^{width}} {r.headers['Content-Length']:^{width}}")
            if args.extensions:
                extlist = args.extensions.split(",")
                for extension in extlist:
                    r = requests.get("{}/{}.{}".format(url, directory, extension))
                    if r.status_code not in codes:
                        response = f"/{directory}.{extension}"
                        print (f"{response:<{width}} {r.status_code:^{width}} {r.headers['Content-Length']:^{width}}")
    with ThreadPoolExecutor(max_workers=threads) as ex:
            ex.map(dirbrute, directory)

if vhost_mode:
    wordlist = open(args.wordlist)
    url = str(args.url)
    vhost = [newline.strip() for newline in wordlist.readlines()]
    codes = [int(code) for code in args.codes.split(",")]
    threads = int(args.threads)

    print(f'{color.GREEN}Url:{color.END}{url}')
    print(f'{color.GREEN}Wordlist:{color.END}{args.wordlist}')
    print(f'{color.GREEN}Threads:{color.END}{threads}')
    print("")
    print(f"{color.YELLOW}Filtering Status Codes{color.END} {color.RED}{codes}{color.END}")
    print("")
    print(f'{color.GREEN}Url\t\t\t\t\t   Status\t\t\t{color.END}')
    
    def vhostbrute(url):
        url, vhost = url
        
        #try:        
        url = url.rsplit("://", 1)
        protocol = (url.pop(0) if len(url) == 2 else "http")
        url = url[0].replace("www.", "")
        width = 30
        if not len(vhost):
            return
                
        url = "{}://{}.{}".format(protocol, vhost, url)
        r = requests.get(url)
        if r.status_code not in codes:
            print(f"{url:<{width}} {r.status_code:^{width}}")
        #except Exception as e:
            #print("e")
            
    urls = [[url, o] for o in vhost]
            
    with ThreadPoolExecutor(max_workers=threads) as ex:
            ex.map(vhostbrute, urls)
