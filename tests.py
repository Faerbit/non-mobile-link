#!/usr/bin/env python
import praw
import bot
import re
import unittest

class TestWikipediaRegex(unittest.TestCase):
    def test_detect_mobile(self):
        test_string ="https://de.m.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte"
        links =[]
        for i in re.findall(bot.regex.wikipedia_find, test_string):
            links.append(i)
        self.assertEqual(["https://de.m.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte"], links)

    def test_not_detect_not_mobile(self):
        test_string ="https://de.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte"
        links =[]
        for i in re.findall(bot.regex.wikipedia_find, test_string):
            links.append(i)
        self.assertEqual([], links)

    def test_only_detect_mobile(self):
        test_string =("https://de.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte "
            "https://de.m.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte")
        links =[]
        for i in re.findall(bot.regex.wikipedia_find, test_string):
            links.append(i)
        self.assertEqual(["https://de.m.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte"], links)

    def test_detect_mobile_multiple_times(self):
        test_string =("https://de.m.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte "
            "https://de.m.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte")
        links =[]
        for i in re.findall(bot.regex.wikipedia_find, test_string):
            links.append(i)
        self.assertEqual(["https://de.m.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte",
                "https://de.m.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte"], links)

    def test_detect_mobile_multiple_times_with_other_characters(self):
        test_string =("https://de.m.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte "
            "aösldfj aösldfj öalsfdj öalskdjflöska asöldfljk "
            "https://de.m.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte "
            "aösldfj aösldfj öalsfdj öalskdjflöska asöldfljk "
            "https://de.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte")
        links =[]
        for i in re.findall(bot.regex.wikipedia_find, test_string):
            links.append(i)
        self.assertEqual(["https://de.m.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte",
                "https://de.m.wikipedia.org/wiki/Luftselbstverteidigungsstreitkr%C3%A4fte"], links)

if __name__ == "__main__":
    unittest.main()
