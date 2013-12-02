#!/usr/bin/env python
import praw
import bot
import re
import unittest

class TestRegex(unittest.TestCase):
    non_link_word = "Goat"
    test_links=[
        ("https://de.m.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte",
        "http://de.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte",
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
            result=TestRegex.helper_test_regex(test_string)
            self.assertEqual(result, [mobile_link], msg)

    #def test_not_detect_not_mobile(self):
    #    test_string ="https://de.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte"
    #    links =[]
    #    for i in re.findall(bot.regex.wikipedia_find, test_string):
    #        links.append(i)
    #    self.assertEqual([], links)

    #def test_only_detect_mobile(self):
    #    test_string =("https://de.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte "
    #        "https://de.m.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte")
    #    links =[]
    #    for i in re.findall(bot.regex.wikipedia_find, test_string):
    #        links.append(i)
    #    self.assertEqual(["https://de.m.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte"], links)

    #def test_detect_mobile_multiple_times(self):
    #    test_string =("https://de.m.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte "
    #        "https://de.m.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte")
    #    links =[]
    #    for i in re.findall(bot.regex.wikipedia_find, test_string):
    #        links.append(i)
    #    self.assertEqual(["https://de.m.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte",
    #            "https://de.m.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte"], links)

    #def test_detect_mobile_multiple_times_with_other_characters(self):
    #    test_string =("https://de.m.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte "
    #        "aösldfj aösldfj öalsfdj öalskdjflöska asöldfljk "
    #        "https://de.m.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte "
    #        "aösldfj aösldfj öalsfdj öalskdjflöska asöldfljk "
    #        "https://de.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte")
    #    links =[]
    #    for i in re.findall(bot.regex.wikipedia_find, test_string):
    #        links.append(i)
    #    self.assertEqual(["https://de.m.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte",
    #            "https://de.m.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte"], links)

if __name__ == "__main__":
    unittest.main()
