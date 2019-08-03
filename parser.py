
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
            self.file = file

        def __iter__(self):
            return self

        def __next__(self):
            return self.file.readline()


    def __init__(self, file):
        """
        tags_level is a dictionary containing all tags for various topic levels
        tags_content is a dictionary containing tags for various content types/classes

        :param file : location of the file to be parsed

        """
        self.level_prio = {}
        self.tags_level = {}
        self.tags_content = {}
        self.attributes = {}
        self.__element_stack = []
        self.file_for_parsing = self._get_file_to_parse(file)
        logging.basicConfig(filename="./logs/running_log.log", level=logging.INFO)

    def set_prio_for_level(self, level, prio):
        """
        level identifies the topic level as a string
        prio is a integer value
        :param level: string
        :param prio: integer priority
        :return: None
        """
        if level in self.level_prio.keys():
            if self.level_prio[level] != prio:
                raise Exception("contradicting priority value set for already existing level element in level_prio")
        else:
            self.level_prio[level] = prio
            logging.info(f"level {level} has a priority of {prio}")


    def set_tag_for_level(self, level, tag):
        """
        set a tag for storing a topic type
        :param level: topic or header level as a string
        :param tag: xml tag
        :return: None
        """
        self.tags_level[level] = tag
        logging.info(f"xml tag set to {tag} for level_{level}")


    def set_tag_for_content(self, content_class, tag):
        """
        set a tag for storing a content type or class
        :param content_class: content type or class as a string
        :param tag: xml tag
        :return: None
        """
        self.tags_content[content_class] = tag
        logging.info(f"xml tag set to {tag} for content_class {content_class}")

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
        to break the text, dev can use _parse_text() function
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
            file = open(file_path)
            logging.info(f"file {file_path} has been opened")
            return file
        except FileNotFoundError:
            print(f"OS error: {FileNotFoundError}")
            logging.critical(f"{FileNotFoundError}")
        except:
            print(f"error {sys.exc_info()[0]}")
            logging.critical(f"{sys.exc_info()[0]}")
        finally:
            print("check the file and try again")
            logging.critical(f"the path of the file has to be checked")
            exit()

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
        # TODO: finish the function

    def _parse_text(self, text="", seperator=' '):
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

    def _get_priority_of_level(self, level_tag):
        for keys in self.tags_level.keys():
            if self.tags_level[keys] == level_tag:
                return self.level_prio[keys]
        raise ElementDoesNotExist(f"level tag {level_tag} does not exist in priority table")

    def _get_level_of_tag(self, tag):
        for key in self.tags_level.keys():
            if tag == key:
                return key
        raise ElementDoesNotExist(f"level of the tag {tag} does not exist in table")

    def parse(self):
        """

        :return:
        """
        try:
            if self.file_for_parsing is None:
                raise FileNotAdded("Check file object")
            elif self.tags_content.__sizeof__() == 0 or self.tags_level.__sizeof__() == 0 or self.level_prio.__sizeof__():
                raise ParserTagsNotConfigured
        except FileNotAdded as err:
            logging.critical(f"exception occurred: {err}")
        except ParserTagsNotConfigured as err:
            logging.critical(f"exception occurred : {err}")

        root_element = self._create_root("root")
        self.__element_stack.append(root_element)
        logging.info(f"root element created and added to the stack")
        process_flag = True

        for text in TextParser.__TextFileIterator(self.file_for_parsing):
            "break the line and find out the level, get corresponding tag, content and attribute dictionary"
            level, content, attrib_dict = self.find_type(text)
            "get the super element from the stack"
            super = self.__element_stack.pop()
            logging.info(f"super element aquired for processing")
            "create the subelement"
            element = self._create_element(super, self.tags_level[level], content, attrib_dict)
            logging.info(f"sub elemet created")
            self.__element_stack.append(super)
            logging.info(f"super element pushed back into the stack")
            "find out if the new element should be pushed to stack"
            if super is root_element:
                self.__element_stack.append(element)
                logging.info(f"new element pushed into stack")
            elif self._get_priority_of_level(self._get_level_of_tag(super.tag)) < self._get_priority_of_level(level):
                self.__element_stack.append(element)
                logging.info(f"new element pushed into stack")
            else:
                logging.info(f"new element not pushed into stack")

        tree = self._create_element_tree(root_element)
        logging.info(f"tree created")
        tree.write("./raw_resources/xml.xml")
        logging.info(f"tree pushed into file")



class UnimplementedFunctionError(Exception):
    pass


class FileNotAdded(Exception):
    pass


class ParserTagsNotConfigured(Exception):
    pass


class ElementDoesNotExist(Exception):
    pass
