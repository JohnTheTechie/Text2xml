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

    '''
    def subelement_creation_strategy(self, level, content, *args, **kwargs):
        
        pass
    '''

    def find_type(self, text=""):
        self.index += 1
        logging.debug(f"line index {self.index} : {text} being parsed")
        temp_stack = []
        temp_stack = text.split(" ")
        logging.debug(f"{text} has been split into stack as {temp_stack}")

        level_type = None
        level_attributes = {}
        content = None

        if not temp_stack[0].isalpha():
            logging.info(f"the text_{self.index}  starts with numerics. topic identified")
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
                content = text.rsplit(" ", 1)[0]
            else:
                level_type = "adi_1"
                content = text
                self.kural_index += 1
            level_attributes["index"] = self.kural_index
        return level_type, content, level_attributes


obj = KuralParser("../raw_resources/kural_text.txt")
obj.parse()
