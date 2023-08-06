import xml.etree.ElementTree as ET

class Report:

    def __init__(self, path, assitive_keyword_list):
        self.reported_path = path
        self.hide_assistive_keywords(assitive_keyword_list)

    def hide_assistive_keywords(self, assitive_keyword_list):
        tree = ET.parse(self.reported_path)
        for elem in tree.iter():
            self.deep_find_keyword(elem, assitive_keyword_list)
        tree.write(self.reported_path)

    def compose_keyword_name(self, node):
        return (node.attrib['library'] + '.' + node.attrib['name']
                if 'library' in node.attrib else node.attrib['name'])

    def keyword_is_assitive(self, name, assitive_keyword_list):
        return name in assitive_keyword_list

    def remove_keyword(self, parent_node, remove_list):
        for kw in remove_list:
            parent_node.remove(kw)

    def deep_find_keyword(self, testnode, assitive_keyword_list):
        remove_list = []
        for node in testnode:
            if node.tag == 'kw':
#                 self.name = self.compose_keyword_name(node)
                self.name = node.attrib['name']
                if self.keyword_is_assitive(self.name, assitive_keyword_list):
                    remove_list.append(node)
                else:
                    self.deep_find_keyword(node, assitive_keyword_list)

        self.remove_keyword(testnode, remove_list)
