import json
import sys
import os
import requests
import subprocess
import re

def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

if __name__ == '__main__':

    args = sys.argv

    filen = None
    targetf = None
    if len(args)<2:
        if os.path.exists("upvoted_posts.json"):
            print(f"found upvoted_posts.json")
            filen = "upvoted_posts.json"
        else:
            print(f"provide a relative path to a file containing the links")
            sys.exit(0)
    else:
        filen = args[1]+".json"
    
    if len(args)<3:
        print(f"using default download folder ./download")
        targetf = "./download"
    else:
        targetf = "./"+args[2]

    if not os.path.exists(targetf):
        os.makedirs(targetf)

    links = None

    with open(filen) as jfile:
        links = json.load(jfile)

    maxfnl = int(subprocess.check_output("getconf NAME_MAX .", shell=True))
    
    for l in links:
        ln = links[l]+"___"+l.replace("/","_sl_").replace(":","_co_").replace("\\","_bsl_")
        ln = get_valid_filename(ln)
        ln, lext = os.path.splitext(ln)
        if len(ln)+len(lext)>maxfnl:
            ln = ln[:maxfnl-len(lext)-1]
        fn = targetf+"/"+ln+lext
        if not os.path.exists(fn):
            r = requests.get(l, allow_redirects=True)
            open(fn, 'wb').write(r.content)

