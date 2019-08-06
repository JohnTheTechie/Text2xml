import logging

import textFileParser


class KuralParser(textFileParser.TextParser):
    """
    extends parser
    """

    def __init__(self, file_path):
        super().__init__(file_path)
        self.index = 0
        self.kural_index = 0
        self.set_tag_for_level(level_1="Pal", level_2="Iyal", level_3="Athigaram", level_4="Kural")
        self.set_priority_for_level(level_1=0, level_2=1, level_3=2, level_4=3, adi_1=4, adi_2=4)
        self.set_tag_for_content(adi_1="Mudhaladi", adi_2="Eetradi")
        self.set_attributes_for_tag("level_1", "name", "index")
        self.set_attributes_for_tag("level_2", "name", "index")
        self.set_attributes_for_tag("level_3", "name", "index")
        self.set_attributes_for_tag("level_4", "index")

    def subelement_creation_strategy(self, level, content, *args, **kwargs):
        """
        implements strategy to interpret lines read from the file
        :param level: the level of the read content. Not the level identifier but the tag
        :param content: The text that should be associated with the tag
        :param args: if there is any attribute list available. Contents should be strictly string
        :param kwargs:
        :return:
        """
        logging.debug(f"subelement_creation_strategy(self, level, content, *args, **kwargs) | \
            args received {self, level, content, args, kwargs}")
        if level == "empty string":
            '''
            if an empty string has been read from the file, 
            the strategy shall simply skip the interpretation
            '''
            print("empty line")

        elif level == "adi_1":
            '''
            when adi_1 is received, a new kural tag is created and pushed. 
            Then same kural shall be retrived and the adi shall be pushed
            '''
            element = self._get_super_element_for_element(self.tags_level["level_4"])
            logging.info(f"super element acquired for processing")
            subelement = self._create_element(element, self.tags_level["level_4"], content, args[0])
            logging.info(f"Kural element created with attributes {args[0]}")
            self._push_to_the_stack(element, subelement)

            element = self._get_super_element_for_element(self.tags_content[level])
            logging.info(f"super element acquired for processing")
            subelement = self._create_element(element, self.tags_content[level], content, {})
            logging.info(f"Mudhaladi element created")
            self._push_to_the_stack(element, subelement)

        elif level == "adi_2":
            '''
            When second adi is is received, super element is retrieved and adi 2 is added
            Since the Kural element has been completed with the second meter,
            the elements shall not be pushed into the stack
            '''
            element = self._get_super_element_for_element(self.tags_content[level])
            logging.info(f"super element acquired for processing")
            self._create_element(element, self.tags_content[level], content, {})
            logging.info(f"Eetradi element created")

        else:
            '''
            other type of tags are all just headers hence shall be treated the same way.
            Super element shall be retrieved and subelement created and pushed to the stack'''
            element = self._get_super_element_for_element(self.tags_level[level])
            logging.info(f"super element aquired for processing")
            subelement = self._create_element(element, self.tags_level[level], content, args[0])
            logging.info(f"sub element created")
            self._push_to_the_stack(element, subelement)

    def interpret(self, text=""):

        self.index += 1
        logging.debug(f"line index {self.index} : {text} being parsed")
        temp_stack = text.split(" ")
        logging.info(f"{text} has been split into stack as {temp_stack}")
        logging.info(f"{text} has length of {len(text)}")

        level_type = None
        level_attributes = {}
        content = None

        if len(text) == 0:
            logging.info("empty string returned from file")
            level_type = "empty string"
            content = None
        elif not temp_stack[0].isalpha():
            logging.info(f"the text_{self.index}:{text} starts with numerics {temp_stack[0]}. topic identified")
            topic_level = temp_stack[0].split(".")
            logging.debug(f"topic indicator : {topic_level}")
            if len(topic_level) == 1:
                level_type = "level_1"
                topic_tuple = text.split(" ", 1)
                logging.debug(f"{text} broken into {topic_tuple}")
                level_attributes["name"] = topic_tuple[1]
                level_attributes["index"] = topic_level[0]
            elif len(topic_level) == 2:
                level_type = "level_2"
                topic_tuple = text.split(" ", 1)
                logging.debug(f"{text} broken into {topic_tuple}")
                level_attributes["name"] = topic_tuple[1]
                level_attributes["index"] = topic_level[1]
            elif len(topic_level) == 3:
                level_type = "level_3"
                topic_tuple = text.split(" ", 1)
                logging.debug(f"{text} broken into {topic_tuple}")
                level_attributes["name"] = topic_tuple[1]
                level_attributes["index"] = topic_level[2]
            elif text == "":
                raise Exception("empty text read from the file")
        else:
            if temp_stack[-1].isnumeric():
                level_type = "adi_2"
                meter, cnt = text.rsplit(" ", 1)
                content = meter
                logging.info(f"second line of poem :{meter}")
            else:
                level_type = "adi_1"
                content = text
                logging.info(f"first line of poem {text}")
                self.kural_index += 1
                level_attributes["index"] = str(self.kural_index)
        logging.info(
            f"info type returns level_type:{level_type}, content:{content}, level_attributes:{level_attributes}")
        return level_type, content, level_attributes


obj = KuralParser("../raw_resources/kural_text.txt")
logging.info("#" * 40)
logging.info("#" * 40)
logging.info("#" * 40)
obj.parse()
