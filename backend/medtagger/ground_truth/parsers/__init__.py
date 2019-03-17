from typing import Type

from medtagger.database import models
from medtagger.ground_truth.parsers import base, chain, rectangle


def get_parser(label_element_type: Type[models.LabelElement]) -> base.GeneratorParser:
    available_parsers = {
        models.ChainLabelElement: chain.ChainParser,
        models.RectangularLabelElement: rectangle.RectangleParser,
    }
    ParserClass = available_parsers.get(label_element_type)
    if not ParserClass:
        raise NotImplementedError(f'There is no parser available for {label_element_type}.')
    return ParserClass()
