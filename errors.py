class UnimplementedFunctionError(Exception):
    """
    raised when a function which should be defined as per the end user needs,
    has not been redefined and called
    """
    pass


class FileNotAdded(Exception):
    """
    When a file path has not been specified for parsing
    """
    pass


class ParserTagsNotConfigured(Exception):
    """
    raised when no tags are attributes data was defined for running parser.
    Attribute should be defined by the extending user
    """
    pass


class ElementDoesNotExist(Exception):
    """
    raised when a referred element is not able to found/ or not defined by the extending user
    """
    pass
