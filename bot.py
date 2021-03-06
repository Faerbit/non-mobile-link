#! /usr/bin/env python

import praw
import re
import os

regex= [
    (re.compile("https?://[a-zA-Z]*\.m\.wikipedia\.org/wiki/[a-zA-Z0-9_#%]*"), re.compile("m\.")), #wikipedia
    ]

disclaimer = ("\n\n ^Got ^any ^problems ^or ^suggestions ^for ^me? "
        "^Message ^/u/faerbit ^or ^check ^out ^the ^[code](https://github.com/Faerbit/non-mobile-link)!")

def reply(reply_object, text):
    text += disclaimer
    if isinstance(reply_object, praw.objects.Comment):
        reply_object.reply(text)
    if isinstance(reply_object, praw.objects.Submission):
        reply_object.add_comment(text)
    return reply_object.id

def replace_links(text):
    links = []
    for (find_regex, replace_regex) in regex:
        for i in re.findall(find_regex, text):
            i = re.sub(replace_regex, "", i)
            links.append(i)
    return links

def worker(reddit_session, already_done_comments, already_done_submissions, subreddit):
    comments = praw.helpers.flatten_tree(reddit_session.get_comments(subreddit))
    for comment in comments:
        if comment.id not in already_done_comments:
            links = replace_links(comment.body)
            if len(links) == 1:
                text = "Non-mobile link: "
                text += str(links[0])
                already_done_comments.add(reply(comment, text))
            elif len(links) > 1:
                text = "Non-mobile links:"
                for i in links:
                    text += str(links[i])
                    text += "\n\n"
                already_done_comments.add(reply(comment, text))
            already_done_comments.add(comment.id)
    submissions = reddit_session.get_subreddit(subreddit).get_top(limit=None)
    for submission in submissions:
        if submission.id not in already_done_submissions:
            if submission.is_self:
                links = replace_links(submission.selftext)
            else:
                links = replace_links(submission.url)
            if len(links) == 1:
                text = "Non-mobile link: "
                text += str(links[0])
                already_done_submissions.add(reply(submission, text))
            already_done_submissions.add(submission.id)

def main():
    already_done_comments = set()
    already_done_submissions = set()
    user_agent=("Non-mobile link 0.1 by /u/faerbit")
    reddit = praw.Reddit(user_agent=user_agent)
    reddit.login("non-mobile-linkbot", os.environ["NON_MOBILE_LINKBOT_PASSWORD"])
    worker(reddit, already_done_comments, already_done_submissions, "test")

if __name__ == "__main__":
    main()
