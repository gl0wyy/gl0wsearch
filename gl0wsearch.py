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

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                    help='Show this help message and exit')
parser.add_argument('dir', help="Directory Search")
#parser.add_argument('vhost', help="vHost Search")
parser.add_argument('-u', '--url', help="Target Url or IP Address(e.g): -u http://127.0.0.1", metavar='')
parser.add_argument('-w',  help="wordlist")
parser.add_argument('-e',  help="File Extensions(e.g): -e php,zip,txt") # FILE EXTENSION ARG
parser.add_argument('-sf', help="Filter status codes -sf 404,202", default="503,500,410,404,302")
parser.add_argument('-t',  help="Set worker thread(s) number", default=15)
args = parser.parse_args()

print()
print()
print((colored(figlet_format("gl0wsearch"), color="red")))

if args.dir:
    wordlist = open(args.w)
    url = str(args.url)
    directory = [newline.strip() for newline in wordlist.readlines()]
    statusfilter = [int(code) for code in args.sf.split(",")]
    threads = int(args.t)

    print(f'{color.GREEN}Url:{color.END}{url}')
    print(f'{color.GREEN}Wordlist:{color.END}{args.w}')
    print(f'{color.GREEN}Threads:{color.END}{threads}')
    print("")
    print(f"{color.YELLOW}Filtering Status Codes{color.END} {color.RED}{statusfilter}{color.END}")
    print("")
    print(f'{color.GREEN}Url\t\t\t\t\t   Status\t\t\t Length{color.END}')

    if not (url.startswith ('http://') or url.startswith ('https://')):
        url = 'http://' + url

    def b(directory):
        width = 30
        if not len(directory):
            return
        
        if not directory.startswith('#'):
            r = requests.get("{}/{}".format(url, directory))
                    
            if r.status_code not in statusfilter:
                response = f"/{directory}"
                print(f"{response:<{width}} {r.status_code:^{width}} {r.headers['Content-Length']:^{width}}")
            if args.e:
                extlist = args.e.split(",")
                for extension in extlist:
                    r = requests.get("{}/{}.{}".format(url, directory, extension))
                    if r.status_code not in statusfilter:
                        response = f"/{directory}.{extension}"
                        print (f"{response:<{width}} {r.status_code:^{width}} {r.headers['Content-Length']:^{width}}")
    with ThreadPoolExecutor(max_workers=threads) as ex:
            ex.map(b, directory)

