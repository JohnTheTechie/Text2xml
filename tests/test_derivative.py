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
        self.set_prio_for_level(level_1=0, level_2=1, level_3=2)
        self.set_tag_for_content(adi_1="Mudhladi", adi_2="Eetradi")
        self.set_attributes_for_tag("level_1", "name", "index")
        self.set_attributes_for_tag("level_2", "name", "index")
        self.set_attributes_for_tag("level_3", "name", "index")
        self.set_attributes_for_tag("level_4", "index")


    def subelement_creation_strategy(self, level, content, *args, **kwargs):
        """

        :param level:
        :param content:
        :param args:
        :param kwargs:
        :return:
        """
        if not level == "empty string":
            element = self._get_super_element_for_elment(self.tags_level[level])
            logging.info(f"super element aquired for processing")
            subelement = self._create_element(element, self.tags_level[level], content, args[0])
            logging.info(f"sub element created")
            self._push_to_the_stack(element, subelement)
            return subelement

        


    def find_type(self, text=""):

        self.index += 1
        logging.debug(f"line index {self.index} : {text} being parsed")
        temp_stack = []
        temp_stack = text.split(" ")
        logging.info(f"{text} has been split into stack as {temp_stack}")
        logging.info(f"{text} has length of {len(text)}")

        level_type = None
        level_attributes = {}
        content = None

        if len(text) == 5:
            logging.info("empty string returned from file")
            level_type = "empty string"
            content = None
        elif not temp_stack[0].isalpha():
            logging.info(f"the text_{self.index}:{text} starts with numerics. topic identified")
            topic_level = temp_stack[0].split(".")
            logging.debug(f"topic indicator : {topic_level}")
            if len(topic_level) == 1:
                level_type = "level_1"
                topic_tuple = text.split(" ", 1)
                logging.debug(f"{text} broken into {topic_tuple}")
                level_attributes["name"] = topic_tuple[1]
            elif len(topic_level) == 2:
                level_type = "level_2"
                topic_tuple = text.split(" ", 1)
                logging.debug(f"{text} broken into {topic_tuple}")
                level_attributes["name"] = topic_tuple[1]
            elif len(topic_level) == 3:
                level_type = "level_3"
                topic_tuple = text.split(" ", 1)
                logging.debug(f"{text} broken into {topic_tuple}")
                level_attributes["name"] = topic_tuple[1]
            elif text == "":
                raise Exception("empty text read from the file")
        else:
            if temp_stack[-1].isnumeric():
                level_type = "adi_2"
                meter, cnt = text.rsplit(" ", 1)[0]
                content = meter
                logging.info(f"second line of poem :{meter}")
            else:
                level_type = "adi_1"
                content = text
                logging.info(f"first line of poem {text}")
                self.kural_index += 1
            level_attributes["index"] = self.kural_index
        logging.info(
            f"info type returns level_type:{level_type}, content:{content}, level_attributes:{level_attributes}")
        return level_type, content, level_attributes


obj = KuralParser("../raw_resources/kural_text.txt")
logging.info("#" * 40)
logging.info("#" * 40)
logging.info("#" * 40)
obj.parse()
