from ..config import escape_sequence as esc
from ..utils import interpreters, checkers
from ..data import styles as ANSI_styles
from ..data import styles_clear
from ..utils.format import bold

class Style:

    def __init__(self, *styles):
        '''
            PURPOSE
            Manages styles that can be applied to text in the terminal

            PARAMETERS
            styles          Any number of <str>
        '''
        self.styles = self.check_styles(styles)
        self.update()

    @staticmethod
    def check_styles(styles):
        '''
            PURPOSE
            Checks that parameter 'styles' is a <str> or list thereof, whose
            elements are also members of the set of keys in ANSI.styles

            PARAMETERS
            styles          <str>

            RETURNS
            <list> of <str>
        '''
        options = list(ANSI_styles.keys())
        if styles in [[], (), None]:
            return []
        elif isinstance(styles, (list, tuple)):

            for style in styles:

                if not isinstance(style, str):
                    msg = ('\n\nParameter \'styles\' in \'Style.__init__\' must'
                           ' contain <str> elements that take one or more of '
                           'the following values:\n')
                    for o in options:
                        msg += f'\'{o}\', '
                    msg = msg[:-2]
                    raise TypeError(msg)

                elif style not in options:
                    msg = ('\n\nParameter \'styles\' in \'Style.__init__\' must'
                           ' contain <str> elements that take one or more of '
                           'the following values:\n')
                    for o in options:
                        msg += f'\'{o}\', '
                    msg = msg[:-2]
                    raise ValueError(msg)

            return list(set((styles)))

        elif isinstance(styles, str):

            if styles not in options:
                msg = ('\n\nParameter \'styles\' in \'Style.__init__\' must be '
                       'a <str> (or list thereof) that takes one (or more) '
                       'of the following values:\n')
                for o in options:
                    msg += f'\'{o}\', '
                msg = msg[:-2]
                raise ValueError(msg)

            return [styles]

        else:

            msg = ('\n\nParameter \'styles\' in \'Style.__init__\' must be '
                   'a <str> (or list thereof) that takes one (or more) '
                   'of the following values:\n')
            for o in options:
                msg += f'\'{o}\', '
            msg = msg[:-2]

            raise TypeError(msg)

    def update(self):
        '''
            PURPOSE
            Update the ANSI escape sequence that is returned from this instance
        '''
        if not self.styles:
            self.sequence = self.clear()
            self.codes = []
        else:
            codes = [ANSI_styles[style] for style in self.styles]
            fmt = ''
            for code in codes:
                fmt += f'{code};'
            fmt = fmt[:-1]
            self.sequence = esc.format(fmt)
            self.codes = [ANSI_styles[style] for style in self.styles]

    def add(self, *styles):
        '''
            PURPOSE
            Adds new styles to the current instance

            PARAMETERS
            styles          Any number of <str>
        '''
        self.styles += self.check_styles(styles)
        self.styles = list(set(styles))
        self.update()

    def remove(self, *styles):
        '''
            PURPOSE
            Removes styles in the current instance

            PARAMETERS
            styles          Any number of <str>
        '''
        styles = self.check_styles(styles)
        for style in styles:
            if style in self.styles:
                idx = self.styles.index(style)
                del self.style[idx]
        self.update()

    def __call__(self, string):
        '''
            PURPOSE
            Returns the given string with the current style configuration

            PARAMETERS
            string      <str>

            RETURNS
            out         <str>
        '''
        out = self.sequence + string + self.clear()
        return out

    @staticmethod
    def clear():
        '''
            PURPOSE
            Return an ANSI escape sequence that clears all styles

            RETURNS
            out         <str>
        '''
        fmt = ''
        for style in styles_clear.values():
            fmt += f'{style};'
        fmt = fmt[:-1]
        return esc.format(fmt)

    def __str__(self):
        '''
            PURPOSE
            Returns a human-readable description of the styles implemented
            in the instance

            RETURNS
            out         <str>
        '''
        sample_text = self.sequence + 'Aa Zz 0123' + self.clear()
        out = bold('STYLES')
        length = max(len(key) for key in ANSI_styles.keys()) + 1
        length = max(len(out), length)
        out = bold(out) + '\t'

        if not self.styles:
            out += 'None'
            return out

        for code, style in zip(self.codes, self.styles):
            space = ' '*(length-len(style))
            out += esc.format(code) + style + self.clear() + ' '

        out += f'\n{bold("SAMPLE")}\t{sample_text}'

        return out

    def __repr__(self):
        '''
            PURPOSE
            Machine readable string output with instance information

            RETURNS
            <str>
        '''
        if not self.styles:
            return f'Styles(None)'
        else:
            return f'Styles({", ".join(self.styles)})'

    def __hash__(self):
        '''
            PURPOSE
            To return a unique hash for the combined properties of a Style
            instance

            RETURNS
            <int>
        '''
        ID = ''.join(f'{code:02d}' for code in self.codes)
        return hash(ID)

    @staticmethod
    def list_styles():
        '''
            PURPOSE
            Returns a human-readable description of all available styles

            RETURNS
            out         <str>
        '''
        out = 'STYLES'
        length = max(len(key) for key in ANSI_styles.keys()) + 1
        length = max(len(out), length)
        out = bold(out) + '\n'
        for key, value in ANSI_styles.items():
            space = ' '*(length-len(key))
            out += space + esc.format(value) + key + Style.clear() + '\n'
        return out
