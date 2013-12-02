#! /usr/bin/env python

import praw
import re
import os

regex= [
    (re.compile("https?://[a-zA-Z]*\.m\.wikipedia\.org/wiki/[a-zA-Z0-9_#%]*"), re.compile("m\.")) #wikipedia
    ]

def reply(comment, text):
    text += ("\n\n ^Got ^any ^problems/suggestions ^with ^this ^bot? "
        "^Message ^/u/faerbit ^or ^check ^out ^the ^[code](https://github.com/Faerbit/non-mobile-link)!")
    print("Replying:")
    print(text)
    comment.reply(text)
    already_done.add(comment.id)

def replace_links(text):
    links = []
    for (find_regex, replace_regex) in regex:
        for i in re.findall(find_regex, comment):
            i = re.sub(replace_regex, "", i)
            links.append(j)
    return links

def main():
    user_agent=("Non-mobile link 0.1 by /u/faerbit")
    r = praw.Reddit(user_agent=user_agent)
    already_done = set()
    comments = r.get_subreddit('test').get_comments(limit=500)
    r.login("non-mobile-linkbot", os.environ["NON_MOBILE_LINKBOT_PASSWORD"])
    for comment in comments:
        if comment.id not in already_done:
            text =""
            links = []
            links.append(replace_links(comment.body))
            if len(links) == 1:
                text = "Non-mobile link: "
                text += str(links[0])
                reply(comment, text)
            elif len(links) > 1:
                text = "Non-mobile links:"
                for i in links:
                    text += str(i)
                    text += "\n\n"
                reply(comment, text)

if __name__ == "__main__":
    main()
