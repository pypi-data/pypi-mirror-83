import json
import unittest
from unittest.mock import patch

from action import AspectParser, KeywordLibraryLoader


class TestKeywordLibraryLoader(unittest.TestCase):

    def test_getAllResourcePath(self):
        library_loader = KeywordLibraryLoader()
        get_path = library_loader.get_all_resource_path()

        self.assertGreater(len(get_path), 0, 'Did not get any resource path.')
        self.assertRegex(get_path[0], '_akw.robot$', 'File name should end with _akw.robot')


class TestPaserAspect(unittest.TestCase):

    def test_onePreAspectWihBasedFormat(self):
        with patch('__main__.AspectParser.read_aspect_files') as fake_data:

            fake_data.return_value = [
                {
                    "pointcut":{"when": "pre", "what":"Open Main Page And Login"},
                    "advice": {"keyword": "Pre Action Keyword"}
                }
            ]
            parse = AspectParser()

            self.assertEqual(len(parse.pre_action_map), 1)
            self.assertEqual(len(parse.post_action_map), 0)
            self.assertEqual(parse.pre_action_map[0]['pointcut'].when, 'pre')
            self.assertEqual(parse.pre_action_map[0]['pointcut'].what, 'Open Main Page And Login')
            self.assertEqual(parse.pre_action_map[0]['advice'].keyword, 'Pre Action Keyword')

    def test_onePostAspectWithStatusAndPriority(self):
        with patch('__main__.AspectParser.read_aspect_files') as fake_data:

            fake_data.return_value = [
                {
                    "pointcut":{"when": "post", "what":"Open Main Page And Login", "status":"fail"},
                    "advice": {"keyword": "Post Action Keyword", "priority":5}
                }
            ]

            parse = AspectParser()

            self.assertEqual(len(parse.pre_action_map), 0)
            self.assertEqual(len(parse.post_action_map), 1)
            self.assertEqual(parse.post_action_map[0]['pointcut'].when, 'post')
            self.assertEqual(parse.post_action_map[0]['pointcut'].what, 'Open Main Page And Login')
            self.assertEqual(parse.post_action_map[0]['pointcut'].status, 'FAIL')
            self.assertEqual(parse.post_action_map[0]['advice'].keyword, 'Post Action Keyword')
            self.assertEqual(parse.post_action_map[0]['advice'].priority, 5)

    def test_searchActionWithPriority(self):
        with patch('__main__.AspectParser.read_aspect_files') as fake_data:

            fake_data.return_value = [
                {"pointcut":{"when": "pre", "what":"BuiltIn.Log To Console"},"advice": {"keyword": "Priority5 Keyword", "priority":5}},
                {"pointcut":{"when": "pre", "what":"BuiltIn.Log To Console"},"advice": {"keyword": "Priority2 Keyword", "priority":2}}
            ]

            corresponed_keywords = AspectParser().search_in_pre_action_map('pre', 'BuiltIn.Log To Console', [])
            self.assertEqual(len(corresponed_keywords), 2)
            self.assertEqual(corresponed_keywords[0], ('Priority2 Keyword', False, None))
            self.assertEqual(corresponed_keywords[1], ('Priority5 Keyword', False, None))

    def test_searchInMultipleActions(self):
        with patch('__main__.AspectParser.read_aspect_files') as fake_data:

            fake_data.return_value = [
                {"pointcut":{"when": "pre",  "what":"BuiltIn.Log To Console"}, "advice": {"keyword": "Priority5 Keyword", "priority":5}},
                {"pointcut":{"when": "pre",  "what":"BuiltIn.Log To Console"}, "advice": {"keyword": "Priority2 Keyword", "priority":2}},
                {"pointcut":{"when": "post", "what":"Go To Profile Page"},     "advice": {"keyword": "Wait Until Profile Page Is Shown"}},
                {"pointcut":{"when": "post", "what":"Open Facebook And Login"},"advice": {"keyword": "Wait Until Facebook Main Page Is Shown"}},
                {"pointcut":{"when": "post", "what":"*", "status": "fail"},    "advice": {"keyword": "Take Screenshot"}}
            ]

            parse = AspectParser()
            keyword_status_is_fail = parse.search_in_post_action_map('post', 'Open Facebook And Login', [], 'fail')
            self.assertEqual(len(keyword_status_is_fail), 2)

    def test_locatorSameAsPointcut(self):
        with patch('__main__.AspectParser.read_aspect_files') as fake_data:

            fake_data.return_value = [
                {
                    "pointcut":{"when": "pre", "what":"SeleniumLibrary.Click Element"},
                    "advice":{"keyword":"Wait Until Element Is Shown On page", "locatorSameAsPointcut":True}
                }
            ]

            parse = AspectParser()
            corresponed_keywords = parse.search_in_pre_action_map('pre', 'SeleniumLibrary.Click Element', [])
            self.assertEqual(len(corresponed_keywords), 1)
            self.assertEqual(corresponed_keywords[0], ('Wait Until Element Is Shown On page', True, None))

if __name__ == '__main__':
    unittest.main()
