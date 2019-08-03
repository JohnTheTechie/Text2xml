
import xml.etree.ElementTree as ET
import logging
import sys
import os.path as fpath

class TextParser:
    """
    class for parsing multilevel text documents
    developers using this class must implement find_type()
    """

    def __init__(self, file):
        """
        tags_level is a dictionary containing all tags for various topic levels
        tags_content is a dictionary containing tags for various content types/classes

        """
        self.tags_level = {}
        self.tags_content = {}
        self.attributes = {}
        self.file_for_parsing = None
        logging.basicConfig(filename="./logs/running_log.log", level=logging.INFO)

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
        :param text:
        :return:
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
        :param root_element:
        :return: tree
        """
        tree = ET.ElementTree(root_element)
        logging.info(f"tree has been created with {root_element} as root")









class UnimplementedFunctionError(Exception):
    pass

