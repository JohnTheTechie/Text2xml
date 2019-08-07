
import logging
import os.path as fpath
import sys
import xml.etree.ElementTree as ET

from errors import *


class TextParser:
    """
    class for parsing multilevel text documents
    developers using this class must implement interpret()
    """

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
        self.root_element = None
        self.file_for_parsing = self._get_file_to_parse(file_path)
        self.destination_file = None

    def set_priority_for_level(self, level=None, priority=None, **kwargs):
        """
        level identifies the topic level as a string
        prio is a integer value
        :param level: string
        :param priority: integer priority
        :return: None
        """
        if level is not None and priority is not None:
            if level in self.level_prio.keys():
                if self.level_prio[level] != priority:
                    raise Exception("contradicting priority value set for already existing level element in level_prio")
            else:
                self.level_prio[level] = priority
                logging.info(f"level {level} has a priority of {priority}")
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
        :return: None
        """
        self.attributes[tag] = args
        logging.info(f"attributes {args} have been set for the tag {tag}")

    def set_destination_file(self, path="./", name="result.xml"):
        """
        set the name and the location of the end product
        :param path: location path for the product file
        :param name: dest file name
        :return: absolute path of the destination file
        """
        destination_location = fpath.join(path, name)
        self.destination_file = fpath.abspath(destination_location)
        return self.destination_file

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
            print(f"OS error: {FileNotFoundError.__traceback__}")
            logging.critical(f"_get_file_to_parse | {FileNotFoundError}. application need to quit")
            exit(1)

    def _create_root(self, root_tag):
        """
        creates the root element for the xml file
        :param root_tag: string
        :return: xml element
        """
        element = ET.Element(root_tag)
        logging.info(f"root element with tag {root_tag} has been created")
        return element

    def _create_element(self, super_element, element_tag, content, *args):
        """
        creates a subelement for the given super element with the content.
        Attributes should be provided via kwargs
        :param super_element: elementTree.element object
        :param element_tag: string literal, name of the tag
        :param content: content to be added to tag
        :param kwargs: attributes should be added from the self.attributes item
        :return: element
        """
        if len(args[0].items()) == 0:
            element = ET.SubElement(super_element, element_tag)
        else:
            element = ET.SubElement(super_element, element_tag, args[0])
        element.text = content

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

    def split_text(self, text="", separator=' ', split_dir_from_left=True):
        """
        seperate the input text and return a list of words
        :param text: line read from the file
        :param separator: literal at which the text string needs to be split
        :param split_dir_from_left : true is a normal split from left else false for right split
        :return: list of words
        """
        if split_dir_from_left:
            list_words = text.split(separator)
        else:
            list_words = text.rsplit(separator)
        logging.info(f"line parsed into {list_words}")
        return list_words

    def _get_priority_of_level_by_tag(self, level_tag):
        """
        checks all the tags containers for the specified tag and looks up the priority from prio table
        :param level_tag: string tag
        :return: priority in Int
        """
        logging.info(f"priority of tag {level_tag} requested")
        for keys in self.tags_level.keys():
            if self.tags_level[keys] == level_tag:
                return self.level_prio[keys]
        else:
            for keys in self.tags_content.keys():
                if self.tags_content[keys] == level_tag:
                    return self.level_prio[keys]
        raise ElementDoesNotExist(f"level tag {level_tag} does not exist in priority table")

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

    def _get_level_of_tag(self, tag):
        for key in self.tags_level.keys():
            if tag == self.tags_level[key]:
                return key
        raise ElementDoesNotExist(f"level of the tag {tag} does not exist in table")

    def _get_super_element_for_element(self, element_level):
        """
        compares the contents of the element stack contents and the passed element
        returns a suitable super element to which element can be appended
        As standard 0 should have highest priority.
        :param element_level: element level as string. should be retrieved from self.tags_level
        :return:
        """
        element_under_test = self.__element_stack.pop()

        '''
        If the popped alement is the root, then it shall be returned as it is,
        as root has the highest level of element
        '''
        if element_under_test is self.root_element:
            logging.info(f"element {element_under_test.tag} is the root")
            return element_under_test
        '''
        the priorities of the calling tag and the retrieved tags shall be checked
        '''
        element_under_test_priority = self._get_priority_of_level_by_tag(element_under_test.tag)
        element_level_priority = self._get_priority_of_level_by_tag(element_level)
        logging.info(
            f"{element_level}'s super element needs to be found | \
            {element_under_test.tag} with prio:{element_under_test_priority} is the current potential super element")
        '''
        if retrieved element has a higher priority, the same shall be returned.
        Check shall be done to confirm if the returned tag is immediate super tag and warning shall be 
            logged in, if found contrary
        if popped tag has lower priority then the function shall be called recursively
            until suitable tag / root is retrieved from stack
        '''
        if element_under_test_priority < element_level_priority:
            logging.info(f"{element_under_test.tag} has higher priority than {element_level}")
            if element_level_priority - element_under_test_priority > 1:
                logging.warning(f"the element from the stack is of much higher level than the element to be pushed.")
            logging.info(f"{element_under_test.tag} is returned from stack for process")
            return element_under_test

        else:
            logging.info(f"stack needs to be poped further")
            return self._get_super_element_for_element(element_level)

    def __sanity_check(self):
        """
        called before the initiation of parsing process to check if necessary parameters have been added
        :return:
        """
        logging.debug(f"{self.tags_level}")
        logging.debug(f"{self.tags_content}")
        logging.debug(f"{self.level_prio}")

        if self.file_for_parsing is None:
            raise FileNotAdded("Check file object")
        if len(self.tags_content.items()) == 0 or len(self.tags_level.items()) == 0 or len(
                self.level_prio.items()) == 0:
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

    def subelement_creation_strategy(self, level, content, *args, **kwargs):
        """
        the extending class must override this function to redefine the strategy as per need
        implements strategy to interpret lines read from the file
        :param level: the level of the read content. Not the level identifier but the tag
        :param content: The text that should be associated with the tag
        :param args: if there is any attribute list available. Contents should be strictly string
        :param kwargs:
        :return:
        """
        element = self._get_super_element_for_element(self.tags_level[level])
        logging.info(f"super element aquired for processing")
        subelement = self._create_element(element, self.tags_level[level], content, args[0])
        logging.info(f"sub element created")
        self._push_to_the_stack(element, subelement)
        return subelement

    def interpret(self, text):
        """
        must be implemented before usage. raise UnimplementedFunctionError.
        to break the text, dev can use split_text() function
        :param text:
        :return: (super_tag, tag, content, **kwargs), kwargs should specify the attributes for the tag
        """
        raise UnimplementedFunctionError("implement the function first")

    def parse(self):
        """
        This function shall parse the contents of the specified file
        Before calling this function, all necessary tags, priority and attributes need to be set
        :return:
        """
        sLog("sanity check begins")
        self.__sanity_check()
        sLog("sanity check ends")

        self.root_element = self._create_root("root")
        self.__element_stack.append(self.root_element)

        sLog("root element created and added to the stack")

        self.file_for_parsing.readline()
        count = 0
        for text in self.file_for_parsing:
            count += 1
            text = str(text).strip("\n")
            sLog(f"iteration count {count + 1} | parsing text : {text}")
            topic_level, content, attrib_dict = self.interpret(text)
            logging.info(f"calling subelement_creation_strategy({topic_level}, {content}, {attrib_dict})")
            self.subelement_creation_strategy(topic_level, content, attrib_dict)

        tree = self._create_element_tree(self.root_element)
        logging.info(f"tree created")
        tree.write(self.destination_file)
        sLog("tree pushed into file")

        del self.root_element


def sLog(text):
    logging.info("*" * 40)
    logging.info(text)
    logging.info("*" * 40)
