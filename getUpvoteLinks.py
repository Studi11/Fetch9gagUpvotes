
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json
import sys
import re
import time
import random
from signal import signal, SIGINT
import chromedriver_binary
from fake_useragent import UserAgent


posts = {}
posts_file = ""


def configure_driver():
    profile_dir = os.environ['HOME']+"/.config/google-chrome/"
    # print(f"profile: {profile_dir}")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("user-data-dir="+profile_dir)
    ua = UserAgent()
    userAgent = ua.random
    chrome_options.add_argument(f"user-agent={userAgent}")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def getSomeArticles(driver):
    global posts

    stream_list = []
    article_list = []

    def update():
        nonlocal stream_list, article_list
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        stream_list = soup.find_all(id=re.compile('^stream-'))
        
        stream_list = list(map(lambda x: x['id'], stream_list))
        print(f"streams {stream_list}")

        article_list = soup.find_all(id=re.compile('^jsid-post-'))

    update()

    art_i = 0
    while True: # art_i in range(len(article_list)):
        if art_i>=len(article_list):
            break
        art = article_list[art_i]
        if art.header==None:
            #print(f"article has no header\n{art}")
            if art_i==0:
                driver.execute_script("window.scrollBy(0,-window.innerHeight);")
                print("scrolling up")
                update()
            else:
                driver.execute_script("window.scrollBy(0,window.innerHeight);")
                print("scrolling down")
                update()
            continue

        title = art.header.h1.contents[0]

        pc = art.findAll("div", {"class": "post-container"})[0]

        link = pc.picture
        #link = art.picture
        if link:
            link = link.img
        else:
            link = pc.video
            if link!=None:
                link = link.source
        # TODO: check for youtube link
        if not link:
            pc = pc.findAll("div", {"class": "youtube-post"})[0]
            
        if not link:
            print(f"article not recognised: {art.prettify()}")
            with open("errors.txt", "a+") as errorfile:
                errorfile.write(f"article not recognised:\n{art.prettify()}\n\n\n")
            art_i += 1
            continue
        src = link['src']
        print(f"{title}\t\t{src}")
        #posts.append({'src': src, 'title': title})
        if not src in posts:
            posts[src] = title
            savePosts()

        art_i += 1

    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    time.sleep(0.6+random.random()*0.9)
    
    for st in stream_list:
        driver.execute_script(f"var element = document.getElementById('{st}'); element.remove();")

    


    try:
        element = WebDriverWait(driver, 20).until(
            #EC.presence_of_element_located((By.TAG_NAME, "article"))
            EC.presence_of_element_located((By.CLASS_NAME, "post-container"))
        )
    except Exception as ex:
        print(f"no stream found {ex}")
        return False

    return len(article_list)


def handler(a1, a2):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    savePosts()
    sys.exit(0)

def savePosts():
    global posts
    if posts:
        with open(posts_file, "w") as jfile:
            json.dump(posts, jfile, indent=4)


if __name__ == '__main__':
    
    args = sys.argv
    
    signal(SIGINT, handler)

    if len(args)<2:
        print("provide your 9gag username as the first argument")
        sys.exit(0)

    driver = configure_driver()

    driver.get(f"https://9gag.com/u/{sys.argv[1]}/likes")

    #for c in driver.get_cookies():
    #    print(f"{c['domain']}: {c['name']}, {c['secure']}, {c['value']}")
    sessionCookie = any(c['name']=='session' for c in driver.get_cookies())

    if not sessionCookie:
        print(f"no 9gag session cookie found, login on 9gag in your chrome browser with the default profile")
        sys.exit(0)



    posts = {}

    if len(args)<3:
        posts_file = "upvoted_posts.json"
    else:
        posts_file = args[2]+".json"

    if os.path.exists(posts_file):
        with open(posts_file) as jfile:
            posts = json.load(jfile)
            print("loaded posts file")

    articles = True

    while articles:
        articles = getSomeArticles(driver)
        if articles:
            print(f"got {articles} articles")
        else:
            print(f"no more articles found")

    savePosts()



    driver.close()
