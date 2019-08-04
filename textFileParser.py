
import logging
import os.path as fpath
import sys
import xml.etree.ElementTree as ET


class TextParser:
    """
    class for parsing multilevel text documents
    developers using this class must implement find_type()
    """

    class __TextFileIterator:
        """
        iterator class for file contents.
        returns contents line by line
        """

        def __init__(self, file):
            logging.info(f"iterator created")
            self.file = file

        def __iter__(self):
            return self

        def __next__(self):
            line = self.file.readline()
            logging.info(f'{[elem.encode("hex") for elem in line]} returned from iterator')
            return line

    def __init__(self, file_path):
        """
        tags_level is a dictionary containing all tags for various topic levels
        tags_content is a dictionary containing tags for various content types/classes

        :param file_path : location of the file to be parsed

        """
        logging.basicConfig(filename="../logs/logs.txt", filemode="w", level=logging.DEBUG)
        self.level_prio = {}
        self.tags_level = {}
        self.tags_content = {}
        self.attributes = {}
        self.__element_stack = []
        self.file_for_parsing = self._get_file_to_parse(file_path)

    def set_prio_for_level(self, level=None, prio=None, **kwargs):
        """
        level identifies the topic level as a string
        prio is a integer value
        :param level: string
        :param prio: integer priority
        :return: None
        """
        if level is not None and prio is not None:
            if level in self.level_prio.keys():
                if self.level_prio[level] != prio:
                    raise Exception("contradicting priority value set for already existing level element in level_prio")
            else:
                self.level_prio[level] = prio
                logging.info(f"level {level} has a priority of {prio}")
        else:
            for item in kwargs.items():
                if item not in kwargs.keys():
                    self.level_prio[item[0]] = item[1]
                    logging.info(f"level_prio | priority for level : {item[0]} added to dictionary as {item[1]}")
                else:
                    logging.info(f"{item} already exist in self.level_prio")

    def set_tag_for_level(self, level=None, tag=None, **kwargs):
        """
        set a tag for storing a topic type
        :param level: topic or header level as a string
        :param tag: xml tag
        :return: None
        """
        logging.debug(f"level:{level},   tag:{tag},    dict:{kwargs}")
        if level is not None and tag is not None:
            self.tags_level[level] = tag
            logging.info(f"xml tag set to {tag} for level_{level}")
        else:
            for item in kwargs.items():
                if item[0] not in self.tags_level.keys():
                    print(f"wtf da {item}")
                    self.tags_level[item[0]] = item[1]
                    logging.info(f"tags_level | tag for level : {item[0]} added to dictionary as {item[1]}")
                else:
                    logging.info(f"{item} already exist in self.tags_level")

    def set_tag_for_content(self, content_class=None, tag=None, **kwargs):
        """
        set a tag for storing a content type or class
        :param content_class: content type or class as a string
        :param tag: xml tag
        :return: None
        """
        if content_class is not None and tag is not None:
            self.tags_content[content_class] = tag
            logging.info(f"xml tag set to {tag} for content_class {content_class}")
        else:
            for item in kwargs.items():
                if item not in kwargs:
                    self.tags_content[item[0]] = item[1]
                    logging.info(f"tags_content | tag for content : {item[0]} added to dictionary as {item[1]}")
                else:
                    logging.info(f"{item} already exist in self.tags_content")

    def set_attributes_for_tag(self, tag, *args):
        """
        set a list of attributes for each tag
        :param tag: tag to which attributes are needed to be attached
        :param attribute_set: list of attributes
        :return: None
        """
        self.attributes[tag] = args
        logging.info(f"attributes {args} have been set for the tag {tag}")


    def find_type(self, text):
        """
        must be implemented before usage. raise UnimplementedFunctionError.
        to break the text, dev can use parse_text() function
        :param text:
        :return: (super_tag, tag, content, **kwargs), kwargs should specify the attributes for the tag
        """
        raise UnimplementedFunctionError("implement the function first")

    def _get_file_to_parse(self, file_path):
        """
        function parses the address and returns the file object
        :param file_path: location of the file to be parsed
        :return: file_object
        """
        try:
            abs_path = fpath.abspath(file_path)
            logging.info(f"absolute path of the raw file aquired: {abs_path}")
            if fpath.exists(abs_path):
                file = open(file=abs_path, encoding="UTF-8")
                logging.debug(f"file opened at {abs_path}")
                logging.info(f"file {file_path} has been opened")
                return file
            else:
                logging.critical(f"file does not exist at the specified path {abs_path}")
                raise FileNotFoundError
        except FileNotFoundError:
            print(f"OS error: {FileNotFoundError}, {sys.call_tracing()}")
            logging.critical(f"{FileNotFoundError}. application need to quit")
            exit(1)


    def _create_xml_file(self, path_xml_file, name_xml_file=None):
        """
        creates and returns an xml file
        :param path_xml_file: path where the file needs to be created
        :param name_xml_file: name of the file. If name inclued in python, no need to specify this param
        :return: file object
        """
        if name_xml_file is None:
            path, filename = fpath.split(path_xml_file)
        else:
            path, filename = path_xml_file, name_xml_file

        try:
            file = open(fpath.join(path, filename), "w")
            logging.info(f"file {filename} has been created at {path}")
            return file
        except:
            print(f"error {sys.exc_info()[0]}")
        finally:
            print("check whether the path is available first")
            logging.critical(f"file {filename} not able to be created at {path}")

    def _create_root(self, root_tag):
        """
        creates the root element for the xml file
        :param root_tag: string
        :return: xml element
        """
        element = ET.Element(root_tag)
        logging.info(f"root element with tag {root_tag} has been created")
        return element

    def _create_element_tree(self, root_element):
        """
        creates tree with the root element specified.
        :param root_element: root as ET.element object
        :return: tree
        """
        tree = ET.ElementTree(root_element)
        logging.info(f"tree has been created with {root_element} as root")
        return tree

    def _create_element(self, super_element, element_tag, content, *args, **kwargs):
        """
        creates a subelement for the given super element with the content.
        Attributes should be provided via kwargs
        :param super_element: elementTree.element object
        :param element_tag: string literal, name of the tag
        :param content: content to be added to tag
        :param kwargs: attributes should be added from the self.attributes item
        :return: element
        """
        element = ET.SubElement(super_element, element_tag, args[0])
        element.text = content

        return element

    def parse_text(self, text="", seperator=' '):
        """
        seperate the input text and return a list of words
        :param text: line read from the file
        :param seperator: literal at which the text string needs to be split
        :return: list of words
        """
        list_words = text.split(seperator)
        logging.info(f"line parsed into {list_words}")
        return list_words

    '''
    def _find_element(self, level_tag, topic_name, root_element):
        """
        searches the tree for the subelement with the specified topic name under root_element
        :param topic_name: topic as string
        :param root_element: element object
        :return: element object
        """
        for ele in root_element.findall(level_tag):
            for key in ele.attrib:
                if ele.attrib[key] == topic_name:
                    return ele
    '''

    def _get_priority_of_level_by_tag(self, level_tag):
        for keys in self.tags_level.keys():
            if self.tags_level[keys] == level_tag:
                return self.level_prio[keys]
        raise ElementDoesNotExist(f"level tag {level_tag} does not exist in priority table")

    def _get_level_of_tag(self, tag):
        for key in self.tags_level.keys():
            if tag == self.tags_level[key]:
                return key
        raise ElementDoesNotExist(f"level of the tag {tag} does not exist in table")

    def __sanity_check(self):
        """
        called before the initiation of parsing process to check if necessary parameters have been added
        :return:
        """

        if self.file_for_parsing is None:
            raise FileNotAdded("Check file object")
        elif len(self.tags_content.items()) == 0 or len(self.tags_level.items()) == 0 or len(
                self.level_prio.items()) == 0:
            logging.debug(f"{self.tags_level}")
            logging.debug(f"{self.tags_content}")
            logging.debug(f"{self.level_prio}")
            raise ParserTagsNotConfigured("configure tgs first")

        return True

    def _push_to_the_stack(self, element, subelement):
        """
        add elements to stack in prio order
        :param element:
        :param subelement:
        :return:
        """
        self.__element_stack.append(element)
        self.__element_stack.append(subelement)
        logging.info(f"{element.tag} and {subelement.tag} pushed to the stack")

    def _get_super_element_for_elment(self, element_level):
        """
        compares the contents of the element stack contents and the passed element
        returns a suitable super element to which element can be appended
        :param element_level: element level as string. should be retrieved from self.tags_level
        :return:
        """
        temp_stack = []
        element_under_test = self.__element_stack.pop()
        if element_under_test is self.root_element:
            logging.info(f"element {element_under_test.tag} is the root")
            return element_under_test
        elif self._get_priority_of_level_by_tag(element_under_test.tag) < self._get_priority_of_level_by_tag(
                element_level):
            if self._get_priority_of_level_by_tag(element_level) - self._get_priority_of_level_by_tag(
                    self._get_level_of_tag(element_under_test.tag)) > 1:
                logging.warning(f"the element from the stack is of much higher level than the element to be pushed.")
            logging.info(f"{element_under_test.tag} is returned from stack for process")
            return element_under_test
        else:
            logging.info(f"stack needs to be poped further")
            return self._get_super_element_for_elment(element_under_test)

    def subelement_creation_strategy(self, level, content, *args, **kwargs):
        """
        the extending class may override this functio to redife the strategy
        :param level:
        :param content:
        :param args:
        :param kwargs:
        :return:
        """
        element = self._get_super_element_for_elment(self.tags_level[level])
        logging.info(f"super element aquired for processing")
        subelement = self._create_element(element, self.tags_level[level], content, args[0])
        logging.info(f"sub element created")
        self._push_to_the_stack(element, subelement)
        return subelement

    def parse(self):
        """
        This functiona shall parse the contents of the specified file
        Before calling this function, all necessary tags, priority and attributes need to be set
        :return:
        """

        self.__sanity_check()

        self.root_element = self._create_root("root")
        self.__element_stack.append(self.root_element)
        logging.info(f"root element created and added to the stack")

        for text in TextParser.__TextFileIterator(self.file_for_parsing):
            "break the line and find out the level, get corresponding tag, content and attribute dictionary"
            logging.debug(f"{__name__} | {text} has been returned from iterator")
            try:
                topic_level, content, attrib_dict = self.find_type(text)
                self.subelement_creation_strategy(topic_level, content, attrib_dict)
            except Exception:
                print("exception occurred")

        tree = self._create_element_tree(self.root_element)
        logging.info(f"tree created")
        tree.write("./raw_resources/xml.xml")
        logging.info(f"tree pushed into file")

        del self.root_element




class UnimplementedFunctionError(Exception):
    pass


class FileNotAdded(Exception):
    pass


class ParserTagsNotConfigured(Exception):
    pass


class ElementDoesNotExist(Exception):
    pass