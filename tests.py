#!/usr/bin/env python
import praw
import bot
import re
import unittest
import argparse
import sys
import os
import time

class TestRegex(unittest.TestCase):
    non_link_word = "Goat"
    test_links=[
        ("https://de.m.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte",
        "https://de.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte",
        "Wikipedia regex failed.")
        ]
    used_regex = set()

    def helper_test_regex(test_string):
        links = []
        for (find_regex, replace_regex) in bot.regex:
            for i in re.findall(find_regex, test_string):
                #ensure that every regex has it's test case
                TestRegex.used_regex.add(find_regex)
                links.append(i)
        return links

    def test_detect_mobile(self):
        for (mobile_link, non_mobile_link, msg) in TestRegex.test_links:
            test_string=mobile_link
            self.assertEqual(TestRegex.helper_test_regex(test_string), [mobile_link], msg)

    def test_not_detect_not_mobile(self):
        for (mobile_link, non_mobile_link, msg) in TestRegex.test_links:
            test_string=non_mobile_link
            self.assertEqual(TestRegex.helper_test_regex(test_string), [], msg)

    def test_only_detect_mobile(self):
        for (mobile_link, non_mobile_link, msg) in TestRegex.test_links:
            test_string=non_mobile_link + " " + mobile_link
            self.assertEqual(TestRegex.helper_test_regex(test_string), [mobile_link], msg)

    def test_detect_mobile_multiple_times(self):
        for (mobile_link, non_mobile_link, msg) in TestRegex.test_links:
            test_string=mobile_link + " " + non_mobile_link + " " + mobile_link
            self.assertEqual(TestRegex.helper_test_regex(test_string), [mobile_link, mobile_link], msg)

    def test_detect_link_encased_in_brackets(self):
        for (mobile_link, non_mobile_link, msg) in TestRegex.test_links:
            test_string= "(" + mobile_link + ")" + "[" + mobile_link + "]" + "{" + mobile_link + "}" 
            self.assertEqual(TestRegex.helper_test_regex(test_string), [mobile_link, mobile_link, mobile_link], msg)

    def test_detect_mobile_multiple_times_with_other_text(self):
        for (mobile_link, non_mobile_link, msg) in TestRegex.test_links:
            test_string= (TestRegex.non_link_word + " "
                + mobile_link + " " + TestRegex.non_link_word + " " + non_mobile_link 
                + " " + mobile_link + " " + TestRegex.non_link_word)
            self.assertEqual(TestRegex.helper_test_regex(test_string), [mobile_link, mobile_link], msg)

    def test_replace_mobile(self):
        for (mobile_link, non_mobile_link, msg) in TestRegex.test_links:
            test_string=mobile_link
            self.assertEqual(bot.replace_links(test_string), [non_mobile_link], msg)

    def test_not_replace_not_mobile(self):
        for (mobile_link, non_mobile_link, msg) in TestRegex.test_links:
            test_string=non_mobile_link
            self.assertEqual(bot.replace_links(test_string), [], msg)

    def test_only_replace_mobile(self):
        for (mobile_link, non_mobile_link, msg) in TestRegex.test_links:
            test_string=non_mobile_link + " " + mobile_link
            self.assertEqual(bot.replace_links(test_string), [non_mobile_link], msg)

    def test_replace_mobile_multiple_times(self):
        for (mobile_link, non_mobile_link, msg) in TestRegex.test_links:
            test_string=mobile_link + " " + non_mobile_link + " " + mobile_link
            self.assertEqual(bot.replace_links(test_string), [non_mobile_link, non_mobile_link], msg)

    def test_replace_link_encased_in_brackets(self):
        for (mobile_link, non_mobile_link, msg) in TestRegex.test_links:
            test_string= "(" + mobile_link + ")" + "[" + mobile_link + "]" + "{" + mobile_link + "}" 
            self.assertEqual(bot.replace_links(test_string), [non_mobile_link, non_mobile_link, non_mobile_link], msg)

    def test_replace_mobile_multiple_times_with_other_text(self):
        for (mobile_link, non_mobile_link, msg) in TestRegex.test_links:
            test_string= (TestRegex.non_link_word + " "
                + mobile_link + " " + TestRegex.non_link_word + " " + non_mobile_link 
                + " " + mobile_link + " " + TestRegex.non_link_word)
            self.assertEqual(bot.replace_links(test_string), [non_mobile_link, non_mobile_link], msg)

    def test_every_regex_has_been_tested(self):
        bot_regex = set()
        for (find_regex, replace_regex) in bot.regex:
            bot_regex.add(find_regex)
        self.assertEqual(bot_regex, TestRegex.used_regex)

class TestAPI(unittest.TestCase):
    #testAPI=False
    already_checked = set()
    #fake original set
    already_done_submissions = set()
    already_done_comments = set()
    reddit = praw.Reddit(user_agent="Non-mobile link tester by /u/faerbit")
    submission = praw.objects.Submission

    @classmethod
    def setUpClass(cls):
        #if not TestAPI.testAPI:
        #    TestAPI.skipTest(self, "testAPI not specified")
        cls.reddit.login("non-mobile-linkbot", os.environ["NON_MOBILE_LINKBOT_PASSWORD"])
        for attempt in range(11):
            try:
                cls.submission = cls.reddit.submit("test", "non-mobile test", 
                        "https://de.m.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte")
            except praw.errors.RateLimitExceeded:
                time.sleep(60)
                continue
            break
        else:
            raise Exception("Could not submit test link. Is reddit down?")
        cls.submission.add_comment("https://de.m.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte")

    def helper_search_for_comment(comment_text):
        comment_text += ("\n\n ^Got ^any ^problems/suggestions ^with ^this ^bot? "
            "^Message ^/u/faerbit ^or ^check ^out ^the ^[code](https://github.com/Faerbit/non-mobile-link)!")
        comment_author="Redditor(user_name='non-mobile-linkbot')"
        comments = TestAPI.submission.comments
        for i in comments:
            if comment.id not in self.already_checked and comment.author == comment_author 
                and comment_text == i.body:
                already_checked.add(comment.id)
                return True
        return False

    def test_reply_function(self):
        comment = TestAPI.submission.comments[0]
        text="Testing reply function"
        bot.reply(comment, text)
        assertIs(helper_search_for_comment(text), True)

    def test_main_loop(self):
        bot.main(TestAPI.reddit, already_done_comments, already_done_submissions, "test")
        text = "Non-mobile link: https://de.m.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte"
        #test for submission and comment correction
        assertIs(helper_search_for_comment(text), True)
        assertIs(helper_search_for_comment(text), True)
        # test that every link only gets processed once
        bot.main(TestAPI.reddit, already_done_comments, already_done_submissions, "test")
        assertIs(helper_search_for_comment(text), False)


if __name__ == "__main__":
    #if --test RAPI is passed test Reddit API
    #parser = argparse.ArgumentParser()
    #parser.add_argument("--test")
    #arg=parser.parse_args()
    #if arg.test == "RAPI":
    #    TestAPI.testAPI = True
    #del sys.argv[1:]
    unittest.main()
