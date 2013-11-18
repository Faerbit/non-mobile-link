#! /usr/bin/env python

import praw
import re

def reply(comment, text):
    print("Replying:")
    print(text)
    comment.reply(text)
    already_done.add(comment.id)

user_agent=("Non-mobile link 0.1 by /u/faerbit")
r = praw.Reddit(user_agent=user_agent)
already_done = set()
find_expression = re.compile("https?://[a-zA-Z]*\.m\.wikipedia\.org/wiki/[a-zA-Z0-9_#%]*")
comments = r.get_subreddit('test').get_comments(limit=500)
r.login("non-mobile-linkbot", "")
for comment in comments:
    if comment.id not in already_done:
        text =""
        links = re.findall(find_expression, comment.body)
        for i in links:
            i = re.sub("m\.", "", i)
        if len(links) == 1:
            text = "Non-mobile link: "
            text += links[0]
            reply(comment, text)
        elif len(links) > 1:
            text = "Non-mobile links:"
            for i in links:
                text += links[i]
                text += "\n"
            reply(comment, text)


