import glob
import json
import logging
import os
import pickle
import re
import sys
import unittest
import xml.etree.ElementTree

from robot.libraries.BuiltIn import BuiltIn

logger = logging.getLogger()

class PointCut:
    def __init__(self, when, what, args=[], status=None):
        self.when = when
        self.what = what
        self.args = args
        self.status = status
        if self.status:
            self.status = self.status.upper()

    def __setattr__(self, name, value):
        if name == 'when' and (not isinstance(value, str) or value not in ['pre', 'post', '*']):
            raise ValueError('when: "%s" does not correspond required format!' % value)
        if name == 'what' and not isinstance(value, str):
            raise ValueError('what: "%s" does not correspond required format, must be the string.' % value)
        if name == 'args' and not isinstance(value, list):
            raise ValueError('args: "%s" does not correspond required format, must be the list.' % value)
        if name == 'status' and value is not None and (not isinstance(value, str) or value.upper() not in ['PASS', 'FAIL']):
            raise ValueError('status: "%s" does not correspond required format (PASS or FAIL).' % value)
        object.__setattr__(self, name, value)

    def is_satisfied(self, when, what, args, status=None):
        """
        >>> PointCut('pre', 'BuildIn.*').is_satisfied('pre', 'BuildIn.Should Be Equal', [])
        True
        >>> PointCut('pre', 'BuildIn.*').is_satisfied('post', 'BuildIn.Should Be Equal', [], 'fail')
        False
        >>> PointCut('post', 'BuildIn.*').is_satisfied('post', 'BuildIn.Should Be Equal', [], 'fail')
        True
        >>> PointCut('post', 'BuildIn.*').is_satisfied('pre', 'BuildIn.Should Be Equal', [])
        False
        >>> PointCut('post', '!BuildIn.*').is_satisfied('post', 'BuildIn.Should Be Equal', [], 'fail')
        False
        >>> PointCut('post', 'fbSeleniumLibrary.*').is_satisfied('post', 'BuildIn.Should Be Equal', [], 'fail')
        False
        >>> PointCut('post', '!fbSeleniumLibrary.*').is_satisfied('post', 'BuildIn.Should Be Equal', [], 'fail')
        True
        >>> PointCut('post', '!BuildIn.Should Be Equal').is_satisfied('post', 'BuildIn.Should Be Equal', [], 'fail')
        False
        >>> PointCut('post', '!BuildIn.Should Be Equal', status='fail').is_satisfied('post', 'fbSeleniumLibrary.Should Be Equal', [], 'fail')
        True
        >>> PointCut('post', '!BuildIn.Should Be Equal', status='pass').is_satisfied('post', 'fbSeleniumLibrary.Should Be Equal', [], 'fail')
        False
        >>> PointCut('post', '@fbSeleniumLibrary\..+').is_satisfied('post', 'fbSeleniumLibrary.Should Be Equal', [], 'fail')
        True
        >>> PointCut('post', '@fbSeleniumLibrary\..+').is_satisfied('post', 'BuildIn.Should Be Equal', [])
        False
        >>> PointCut('post', '@fbSeleniumLibrary\..+').is_satisfied('post', 'fbSeleniumLibrary.', [])
        False
        >>> PointCut('post', '@(?!fbSeleniumLibrary\..+)').is_satisfied('post', 'BuildIn.Should Be Equal', [])
        True

        Below are the examples with arguments:
        >>> PointCut('pre', 'BuiltIn.Log To Console', args=['test']).is_satisfied('pre', 'BuiltIn.Log To Console', ['test'])
        True

        Support '|'(or) operator:
        >>> PointCut('pre', 'BuiltIn.Log To Console', args=['test|haha']).is_satisfied('pre', 'BuiltIn.Log To Console', ['haha'])
        True

        >>> PointCut('pre', 'BuiltIn.Log To Console', args=['test']).is_satisfied('pre', 'BuiltIn.Log To Console', ['haha'])
        False

        Poincut defined amount of argement cannot more than the arugement of keyword:
        >>> PointCut('pre', 'BuiltIn.Log To Console', args=['a1', 'a2']).is_satisfied('pre', 'BuiltIn.Log To Console', ['haha'])
        Traceback (most recent call last):
           ...
        ValueError: Argus size of pointcut should not larger than keyword defined argus size.

        Support poincut located more than one arguments:
        >>> PointCut('pre', 'BuiltIn.Should Be Equal', args=['a1', 'a1']).is_satisfied('pre', 'BuiltIn.Should Be Equal', ['a1', 'a1'])
        True
        >>> PointCut('pre', 'BuiltIn.Should Be Equal', args=['a1|a2', 'a1']).is_satisfied('pre', 'BuiltIn.Should Be Equal', ['a1', 'a1'])
        True
        >>> PointCut('pre', 'BuiltIn.Should Be Equal', args=['a1', 'a2']).is_satisfied('pre', 'BuiltIn.Should Be Equal', ['a1', 'a1'])
        False

        Type of Array and Dictionary also can be supported, the data needs to match order.
        """
        if self.args:
            return self.kw_is_satisfied(when, what, status) and self.args_is_satisfied(args)
        return self.kw_is_satisfied(when, what, status)

    def args_is_satisfied(self, args):
        actual_args = self.args_convert_to_actual_value(args)
        return self._match_args(actual_args)

    def _match_args(self, actual_args):
        for point_arg, actual_arg in zip(self.args, actual_args):
            actual_arg = self._convert_to_string(actual_arg)
            if re.match("^%s$" % point_arg
                                .replace('[', '\[')
                                .replace('{', '\{')
                                .replace(' ', ''), actual_arg) is None: return False
        return True

    def _convert_to_string(self, actual_arg):  #For format of dict and list
        if isinstance(actual_arg, list):
            return '[' + ','.join(actual_arg) + ']'
        if isinstance(actual_arg, dict):
            return "{" +",".join(("{}:{}".format(*i) for i in actual_arg.items())) + "}"
        return actual_arg

    def _take_arg_value(self, arg):
        return BuiltIn().get_variable_value(arg) if \
               re.match('^(\$|@|&){[\w]+}$', arg) else arg

    def args_convert_to_actual_value(self, args):
        return [self._take_arg_value(arg) for arg in args]

    def kw_is_satisfied(self, when, what, status=None):
        if self.status:
            return re.match(self.when.replace('*', '.*'), when) != None and self.__match_what(what) and self.status == status.upper()
        return re.match(self.when.replace('*', '.*'), when) != None and self.__match_what(what)

    def __match_what(self, what):
        if self.what.startswith("@"):
            return re.match(self.what[1:], what) != None
        if self.what.startswith("!"):
            return not re.match("^%s$" % self.what[1:].replace('.', '\.').replace('*', '.+'), what)
        return re.match("^%s$" % self.what.replace('.', '\.').replace('*', '.+'), what) != None

class Advice:
    def __init__(self, keyword, priority=1, locatorSameAsPointcut=False, kw_args=None):
        self.keyword = keyword
        self.locator_same_as_pointcut = locatorSameAsPointcut
        self.priority = priority
        self.kw_args = kw_args

    def __setattr__(self, name, value):
        if name == 'keyword' and not isinstance(value, str):
            raise ValueError('keyword: "%s" is not string type!' % value)
        if name == 'priority' and not isinstance(value, int):
            raise ValueError('priority: "%s" is not integer type!' % value)
        if name == 'locator_same_as_pointcut' and not isinstance(value, bool):
            raise ValueError('locatorSameAsPointcut: "%s" is not boolean type!' % value)
        object.__setattr__(self, name, value)

class ActionController:
    def __init__(self):
#       self.library, self.aspect_paser = self.read_objects_in_pickle()
        self.akw_keywords = set()
        self.library = KeywordLibraryLoader()
        self.aspect_paser = AspectParser()

    def read_objects_in_pickle(self):
        if os.path.isfile('listener.pickle'):
            with open('listener.pickle', "rb") as f:
                return pickle.load(f), pickle.load(f)
        else:
            library_object = KeywordLibraryLoader()
            aspect_object = AspectParser()
            with open('listener.pickle', 'wb') as f:
                pickle.dump(library_object, f)
                pickle.dump(aspect_object, f)
        return library_object, aspect_object

    def load_keywords(self):
        self.library.import_related_resources_and_librarys()

    def pre_do(self, when, what, args):
        keyword_list = self.aspect_paser.search_in_pre_action_map(when, what, args)
        self.run_keywords(keyword_list, args)

    def post_do(self, when, what, status, args):
        keyword_list = self.aspect_paser.search_in_post_action_map(when, what, args, status)
        self.run_keywords(keyword_list, args)

    def run_keywords(self, keyword_list, args):
        for keyword, need_args, kw_args in keyword_list:
            self.akw_keywords.add(keyword)
            if need_args and kw_args:
                BuiltIn().run_keyword(keyword, args[0], kw_args)
            elif need_args:
                BuiltIn().run_keyword(keyword, args[0])
            elif kw_args:
                BuiltIn().run_keyword(keyword, *kw_args)
            else:
                BuiltIn().run_keyword(keyword)

    def get_all_run_ass_keywords(self):
        return self.akw_keywords

class KeywordLibraryLoader():
    def __init__(self):
        self.builtin = BuiltIn()
        self.library_name = self.get_all_library_name()
        self.resouce_path = self.get_all_resource_path()

    def parse_library_reference_files(self, file_name):
        if not any(glob.glob(file_name)):
            raise FileNotFoundError
        return (xml.etree.ElementTree.parse(glob.glob(file_name)[0]).
                getroot().findall('referencedLibrary'))

    def get_all_library_name(self):
        library_name = []
        for elem in self.parse_library_reference_files('./red.xml'):
            if elem.get('type') != 'PYTHON':
                continue
            library_name.append(elem.get('name'))
        return library_name

    def get_all_resource_path(self):
        project_path = os.getcwd()
        full_path = os.path.join(project_path, '*_akw.robot')
        all_resource_path = glob.glob(full_path)
        return [resource_path.replace("\\","/") for resource_path in all_resource_path]

    def import_related_resources_and_librarys(self):
        [self.load_library(path) for path in self.library_name]
        [self.builtin.import_resource(path) for path in self.resouce_path]

    def load_library(self, library_name):
        try:
            self.builtin.get_library_instance(library_name)
        except RuntimeError:
            self.builtin.import_library(library_name)

class AspectParser():
    def __init__(self):
        self.data = self.read_aspect_files()
        self.pre_action_map, self.post_action_map = self.separate_action_as_pre_and_post_map()

    def read_aspect_files(self):
        aspect_files = glob.glob('*_aspect.json')   #../*_aspect.json
        return [file_data for file in aspect_files for file_data in self.read_aspect_file(file)]

    def read_aspect_file(self, aspect_file_name):
        with open(aspect_file_name, encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception as e:
                logger.error("Failed to loaded %s file." % aspect_file_name, exc_info=True)

    def separate_action_as_pre_and_post_map(self):
        """
        action_map = [{'pointcut': Pointcut object, 'advice': Advice object}]
        """
        pre_action_map = []
        post_action_map = []
        for action in self.data:

            pointcut = PointCut(**action['pointcut'])
            advice = Advice(**action['advice'])

            if pointcut.when == 'pre':
               pre_action_map.append({'pointcut': pointcut, 'advice': advice})
            elif pointcut.when == 'post':
               post_action_map.append({'pointcut': pointcut, 'advice': advice})
            elif pointcut.when == '*':
                pre_action_map.append({'pointcut': pointcut, 'advice': advice})
                post_action_map.append({'pointcut': pointcut, 'advice': advice})
            else:
                raise Exception('Wrong format, only accept "pre", "post", "*" word.')
        return pre_action_map, post_action_map

    def search_in_pre_action_map(self, when, what, args):
        satisfy_actions = list()
        for action in self.pre_action_map:
            if action.get('pointcut').is_satisfied(when, what, args):
                satisfy_actions.append(action)
        return self.sorted_keywords(satisfy_actions)

    def search_in_post_action_map(self, when, what, args, status):
        satisfy_actions = list()
        for action in self.post_action_map:
            if action.get('pointcut').is_satisfied(when, what, args, status):
                satisfy_actions.append(action)
        return self.sorted_keywords(satisfy_actions)

    def sorted_keywords(self, action_list):
        sorted_action = sorted(action_list, key=lambda k: k['advice'].priority)
        return [(action['advice'].keyword, action['advice'].locator_same_as_pointcut, action['advice'].kw_args) for action in sorted_action]

if __name__ == '__main__':
    unittest.main()
