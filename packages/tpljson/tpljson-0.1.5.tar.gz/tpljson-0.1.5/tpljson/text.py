import textwrap
import math

from colorama import Fore, Back, Style


def surround_text(text, left='>>', right='<<', pad=2, preserve_whitespace=True):
    """
    Surround ``text`` string with the characters from `left` and `right` - if color is not enabled this is
    a good way to draw attention to a particular block of text.

    :param text: the text to surround
    :type text: str
    :param left: text that goes to the left of ``text``
    :type left: str
    :param right: text that goes to the right of ``text``
    :type right: str
    :param pad: whitespace padding to place between ``left``, ``right`` and ``text``
    :type pad: int
    :param preserve_whitespace: preserve existing whitespace before and after text, such that indenting would
           remain unchanged.
    :type preserve_whitespace: bool
    :return: formatted string
    :rtype: str
    """
    ltext = left + (' ' * pad)
    rtext = (' ' * pad) + right
    if preserve_whitespace:
        lspace = len(text) - len(text.lstrip())  # 10
        rspace = len(text) - len(text.rstrip())
        lpad = max((lspace - len(ltext), 0))  # 6
        rpad = max((rspace - len(rtext), 0))
        ltext = (' ' * lpad) + ltext
        rtext = rtext + (' ' * rpad)
        return '{}{}{}'.format(ltext, text.strip(), rtext)
    else:
        return '{}{}{}'.format(ltext, text.strip(), rtext)


def highlight_text(text, fg=Fore.BLACK, bg=Back.LIGHTYELLOW_EX):
    """
    Highlight text if terminal coloring is supported on the current platform.

    :param text: text to highlight
    :type text: str
    :param fg: foreground color `colorama.Fore.<color>`
    :type fg: colorama.Fore
    :param bg: background color `colorama.Back.<color>`
    :type bg: colorama.Back
    :return: colorized string
    :rtype: str
    """
    return fg + bg + text + Style.RESET_ALL


def preview_text(text,
                 max_lines=5,
                 center_line=None,
                 newline='\n',
                 max_chars=0,
                 indent=4,
                 dedent=False,
                 prefix=None,
                 suffix=None,
                 highlight=None,
                 colored=None):
    """
    Preview a blob of text limiting the number of lines, and/or characters.

    Setting any value to `0` will disable that option.

    This function assumes 1 is the first line, because that's what the JSON module uses.

    Note that all arguments and operations are applied to ``text``, ``prefix`` and ``suffix`` if given
    are added after all other operators.

    :param text: a `str` to preview
    :type text: str
    :param max_lines: maximum number of lines from `text` to preview
    :type max_lines: int
    :param center_line: center the preview around this line, 1-based (first line is 1)
    :type center_line: int
    :param newline: character to use for newlines
    :type newline: str
    :param max_chars: maximum number of characters from `text` to preview
    :type max_chars: int
    :param indent: number of characters to indent with, `0` disables this option
    :type indent: int
    :param dedent: `True/False` removes common indentation from the text. (applied before `indent`)
    :type dedent: bool
    :param prefix: Add this text to the beginning of the output string
    :type prefix: str
    :param suffix: add this text to the end of the output string
    :type suffix: str
    :param highlight: colorize the given line, 1-based (first line is 1)
    :param colored: if false, no color will be added to output (default=True)
    :type colored: bool
    :type highlight: int
    :return: formatted string
    :rtype: str
    """

    if dedent:
        text = textwrap.dedent(text)

    if indent is not None and indent > 0:
        text = textwrap.indent(text, ' '*indent)

    if highlight is not None and highlight > 0:
        highlight = highlight - 1  # compensate for 1 based index
        lines = text.split(newline)
        if len(lines) > highlight:
            if colored is None or colored:
                lines[highlight] = highlight_text(lines[highlight])
            else:
                lines[highlight] = surround_text(lines[highlight])
            text = newline.join(lines)

    if max_lines is not None and max_lines > 0:
        lines = text.split(newline)
        # calculate how many lines of context to show around `center_line` based on `max_lines`
        if center_line and len(lines) >= center_line:
            before = math.floor(max_lines / 2.0)
            after = math.ceil(max_lines / 2.0)
            center_line = center_line - 1  # compensate for 1 based index
            start_line = max((center_line - before, 0))
            end_line = min((center_line + after, len(lines)))
            lines = lines[start_line:end_line]
        else:
            lines = lines[:max_lines]
        text = newline.join(lines)

    if max_chars is not None and (len(text) > max_chars > 0):
        # summarize long lines
        lines = text.split(newline)
        max_line_len = math.floor(max((len(text) / len(lines), 5)))  # show at least 5 chars
        lines_limit = []
        for line in lines:
            if len(line) > max_line_len:
                line = '{}...'.format(line[0:max_line_len])
                lines_limit.append(line)
            else:
                lines_limit.append(line)
        text = newline.join(lines_limit)

    if prefix:
        text = prefix + text

    if suffix:
        text = text + suffix

    return text
