from prompt_toolkit.lexers import Lexer
from prompt_toolkit.styles.named_colors import NAMED_COLORS
from prompt_toolkit.completion import NestedCompleter


class RainbowLexer(Lexer):
    def lex_document(self, document):
        colors = list(sorted({"Teal": "#008080"}, key=NAMED_COLORS.get))

        def get_line(lineno):
            return [
                (colors[i % len(colors)], c)
                for i, c in enumerate(document.lines[lineno])
            ]

        return get_line


Completer = NestedCompleter.from_nested_dict({'hello': None, 'exit': None, 'close': None, '.': None,
                                              'change': None, 'phone': None, 'show': None,
                                              'del': None, 'birth': None, 'email': None,
                                              'nxbirth': None, 'sear': None, 'info': None,
                                              'add': None, 'address': None})
