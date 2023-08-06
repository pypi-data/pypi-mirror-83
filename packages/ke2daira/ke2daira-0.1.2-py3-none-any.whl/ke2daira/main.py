from janome.tokenizer import Tokenizer, Token  # type: ignore
from functools import reduce
from operator import add

t = Tokenizer()

TANGO_SEPARATOR = " "
NO_READING = "*"


def get_reading_from_token(token: Token) -> str:
    if token.reading == NO_READING:
        return token.surface
    return token.reading


def tango2yomi(tango: str) -> str:
    tokens = t.tokenize(tango)
    yomi = reduce(add, map(get_reading_from_token, tokens))
    return yomi


def ke2dairanize(text: str) -> str:
    tangos = text.split(TANGO_SEPARATOR)

    yomis = list(map(tango2yomi, tangos))

    if len(tangos) == 1:
        return tangos[0]

    first_tango = yomis[0]
    first_tango_head = first_tango[0]
    first_tango_tail = first_tango[1:]

    last_tango = yomis[-1]
    last_tango_head = last_tango[0]
    last_tango_tail = last_tango[1:]

    yomis[0] = last_tango_head + first_tango_tail
    yomis[-1] = first_tango_head + last_tango_tail

    return TANGO_SEPARATOR.join(yomis)
