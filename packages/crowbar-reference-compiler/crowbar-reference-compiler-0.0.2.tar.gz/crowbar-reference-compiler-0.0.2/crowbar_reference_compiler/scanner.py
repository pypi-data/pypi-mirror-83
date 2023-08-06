from dataclasses import dataclass
from typing import Optional, overload, List, Union

import regex as re  # type: ignore


@dataclass
class Token:
    type: str
    data: Optional[str] = None

    def __repr__(self) -> str:
        if self.data is not None:
            return "{}: {}".format(self.type, repr(self.data))
        else:
            return repr(self.type)


class GenerousTokenList(List[Token]):
    def __getitem__(self, i):
        try:
            return super(GenerousTokenList, self).__getitem__(i)
        except IndexError:
            return Token('')


KEYWORD = re.compile("bool|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|function|if|include|int|long|return|short|signed|sizeof|struct|switch|typedef|unsigned|void|while")
IDENTIFIER = re.compile(r"[\p{L}\p{Pc}\p{Cf}\p{Sk}\p{Mn}][\p{L}\p{Pc}\p{Cf}\p{Sk}\p{Mn}\p{N}]*")
CONSTANT = re.compile(r"""([0-9_]+)|(0[bB][01_]+)|(0[xX][0-9a-fA-F_]+)|([0-9_]+(\.[0-9_]+|[eE][0-9_]+|\.[0-9_]+[eE][0-9_]+))|('([^\'\\]|\\'|\\"|\\\\|\\r|\\n|\\t|\\0|\\x[0-9a-fA-F]{2}|\\u[0-9a-fA-F]{4}|\\U[0-9a-fA-F]{8})')""")
STRING_LITERAL = re.compile(r'''"([^\\"]|\\'|\\"|\\\\|\\r|\\n|\\t|\\0|\\x[0-9a-fA-F]{2}|\\u[0-9a-fA-F]{4}|\\U[0-9a-fA-F]{8})*"''')
PUNCTUATOR = re.compile(r"->|\+\+|--|>>|<<|<=|>=|&&|\|\||[=!+\-*/%&|^]=|[\[\](){}.,+\-*/%;!&|^~><=]")
WHITESPACE = re.compile(r"[\p{Zs}\p{Cc}]+")
COMMENT = re.compile(r"(//[^\n]*\n)|(/\*.*?\*/)", re.DOTALL)


def scan(code):
    result = []
    remaining = code

    while len(remaining) > 0:
        match = COMMENT.match(remaining)
        if match:
            remaining = remaining[match.end():]
            continue
        match = WHITESPACE.match(remaining)
        if match:
            remaining = remaining[match.end():]
            continue
        match = KEYWORD.match(remaining)
        if match:
            result.append(Token(match.group()))
            remaining = remaining[match.end():]
            continue
        match = IDENTIFIER.match(remaining)
        if match:
            result.append(Token('identifier', match.group()))
            remaining = remaining[match.end():]
            continue
        match = CONSTANT.match(remaining)
        if match:
            result.append(Token('constant', match.group()))
            remaining = remaining[match.end():]
            continue
        match = STRING_LITERAL.match(remaining)
        if match:
            result.append(Token('string_literal', match.group()))
            remaining = remaining[match.end():]
            continue
        match = PUNCTUATOR.match(remaining)
        if match:
            result.append(Token(match.group()))
            remaining = remaining[match.end():]
            continue
        raise ValueError("unrecognized code in scanner: {}".format(repr(remaining[:20])))

    return GenerousTokenList(result)
