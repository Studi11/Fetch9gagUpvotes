import json
import sys
import os
import requests

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
        filen = args[1]
    
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

    for l in links:
        ln = l.replace("/","_sl_").replace(":","_co_")
        fn = targetf+"/"+links[l]+"___"+ln
        if not os.path.exists(fn):
            r = requests.get(l, allow_redirects=True)
            open(fn, 'wb').write(r.content)

