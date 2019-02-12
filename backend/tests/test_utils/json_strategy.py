from string import printable

from hypothesis.strategies import recursive, booleans, floats, text, lists, dictionaries


recursive_json = recursive(booleans() |
                           floats() |
                           text(printable),
                           lambda children: lists(children, 1) |
                           dictionaries(text(printable), children, min_size=1))  # straight out of the docs
