<div align='center'>
<img src='https://user-images.githubusercontent.com/98056797/201240451-d09a459d-175a-45cf-8f75-457247971eed.png'></img>

gl0wsearch is a tool programmed in Python used to brute-force web server directories and vhosts/subdomains. I will be consistently improving the tool and adding new features.

![cmd](https://user-images.githubusercontent.com/98056797/201212419-1e6a62ca-6b36-48c5-aab5-141f7edf7649.png)
</div>

### Download
```
git clone https://github.com/gl0wyy/gl0wsearch
```
### Usage
![image](https://user-images.githubusercontent.com/98056797/201211963-62af51ba-a02c-496a-bd56-d7a1c094668b.png)

### Usage Example (dir)
```
./gl0wsearch.py dir -u http://127.0.0.1 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -e php,zip,txt
```
### Usage Example (vhost)
```
./gl0wsearch.py vhost -u http://127.0.0.1 -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt 
```
