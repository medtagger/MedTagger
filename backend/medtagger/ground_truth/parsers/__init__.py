"""Module responsible for definition of parsers needed for Ground Truth data set generation."""
from typing import Type

from medtagger.database import models
from medtagger.ground_truth.parsers import base, chain, rectangle


def get_parser(label_element_type: Type[models.LabelElement]) -> base.LabelElementParser:
    """Return proper Parser for given Label Element type.

    :param label_element_type: type of a Label Element
    :return: Parser object that should be used to convert given Label Element to numpy array
    """
    available_parsers = {
        models.ChainLabelElement: chain.ChainLabelElementParser,
        models.RectangularLabelElement: rectangle.RectangleLabelElementParser,
    }
    ParserClass = available_parsers.get(label_element_type)
    if not ParserClass:
        raise NotImplementedError(f'There is no parser available for {label_element_type}.')
    return ParserClass()
