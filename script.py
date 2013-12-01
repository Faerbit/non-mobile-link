#! /usr/bin/env python

import praw
import re
import os

def reply(comment, text):
    text += "\n\n ^Got ^any ^problems/suggestions ^with ^this ^bot? ^Message ^/u/faerbit ^or ^check ^out ^the ^[code](https://github.com/Faerbit/non-mobile-link)!"
    print("Replying:")
    print(text)
    comment.reply(text)
    already_done.add(comment.id)

user_agent=("Non-mobile link 0.1 by /u/faerbit")
r = praw.Reddit(user_agent=user_agent)
already_done = set()
find_expression = re.compile("https?://[a-zA-Z]*\.m\.wikipedia\.org/wiki/[a-zA-Z0-9_#%]*")
comments = r.get_subreddit('test').get_comments(limit=500)
r.login("non-mobile-linkbot", os.environ["NON_MOBILE_LINKBOT_PASSWORD"])
for comment in comments:
    if comment.id not in already_done:
        text =""
        links = []
        for i in re.findall(find_expression, comment.body):
            i = re.sub("m\.", "", i)
            links.append(i)
        if len(links) == 1:
            text = "Non-mobile link: "
            text += links[0]
            reply(comment, text)
        elif len(links) > 1:
            text = "Non-mobile links:"
            for i in links:
                text += i
                text += "\n\n"
            reply(comment, text)
