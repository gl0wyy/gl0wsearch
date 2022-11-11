adPoolExecutor(max_workers=threads) as ex:
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
