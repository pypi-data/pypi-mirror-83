import re
from collections import namedtuple
from copy import copy
from dataclasses import dataclass
from pathlib import Path
from textwrap import wrap
from tokenize import COMMENT, NEWLINE, TokenInfo, tokenize, untokenize
from typing import List, Sequence, Union

import black
import click


@click.command()
@click.argument("python_file")
@click.option("-l", "--line-length", default=88, type=int)
def cli(python_file: str, line_length):
    """
    Format the given Python file in-place.

    Fills out multiline comments, and then passes the result through `black`.
    """
    try:
        format_file(Path(python_file), line_length)
        click.echo("File formatted.")
    except ValueError as err:
        raise click.BadArgumentUsage(err)


def format_file(python_file: Union[Path, str], line_length: int = 88):

    python_file = Path(python_file)
    if not python_file.exists() or python_file.suffix not in (".py", ".pyi"):
        raise ValueError(
            f'File "{python_file}" does not exist or is not a Python file.'
        )

    with open(python_file, "rb") as f:
        # Note: do not use `tokenize.open` (even though the docs seem to recommend that).
        # https://bugs.python.org/issue23297#msg341028

        original_tokens = list(tokenize(f.readline))

    new_tokens = copy(original_tokens)  # Keep the original tokens around for debugging

    for comment_group in group_comments(original_tokens):
        original_cg_tokens = comment_group.tokens
        formatted_cg_tokens = format(comment_group, line_length)
        insert_index = new_tokens.index(original_cg_tokens[0])
        for token in original_cg_tokens:
            new_tokens.remove(token)
        for token in formatted_cg_tokens:
            new_tokens.insert(insert_index, token)
            insert_index += 1

    # Hack to make `untokenize` work. (This makes `tokenize.Untokenizer` use its
    # `compat()` method from the beginning -- instead of halfway through, when it
    # encounters our first `SimpleTokenInfo` (which then results in the `indents` list
    # being incomplete, yielding an IndexError)).
    new_tokens[0] = SimpleTokenInfo(*new_tokens[0][:2])

    raw_output: bytes = untokenize(new_tokens)
    new_file_content = black.format_str(
        raw_output.decode(), mode=black.Mode(line_length=line_length)
    )
    original_newline = next(
        (token.string for token in original_tokens if token.type == NEWLINE),
        "\n",  # default newline if no newlines found in the file.
    )
    with python_file.open(mode="w", newline=original_newline) as f:
        f.write(new_file_content)


format_file.__doc__ = cli.__doc__


def group_comments(tokens: List[TokenInfo]) -> List["CommentGroup"]:
    comment_groups = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.type == COMMENT:
            comment_group_tokens = [token]
            while True:
                i += 1
                token = tokens[i]
                if token.type in (NEWLINE, COMMENT):
                    comment_group_tokens.append(token)
                else:
                    break
            comment_groups.append(CommentGroup(comment_group_tokens))
        else:
            i += 1

    return comment_groups


@dataclass
class CommentGroup:

    tokens: Sequence[TokenInfo]  # A sequence of `COMMENT` tokens, with `NEWLINE` tokens
    #                            # in between.

    @property
    def comment_tokens(self) -> List[TokenInfo]:
        return [token for token in self.tokens if token.type == COMMENT]

    @property
    def full_comment_text(self) -> str:
        """ The text of all comments in this group, stitched together. """

        def get_text(comment_token: TokenInfo) -> str:
            stripped_chars = (" ", "#")
            return comment_token.string.strip("".join(stripped_chars))

        return " ".join(map(get_text, self.comment_tokens))

    @property
    def initial_start_column(self) -> int:
        """ Column where the first comment of the gorup starts. """
        return self.tokens[0].start[1]

    @property
    def code_block_indent(self) -> str:
        """
        Amount of whitespace at the beginning of the first line (before both code and
        comments). This is the syntactic indent level of the whole Python block in which
        the comment group lives.
        """
        first_line = self.tokens[0].line
        return re.match(r"^\ *", first_line).group()

    @property
    def starts_on_its_own_line(self) -> bool:
        """
        Whether the first comment of the group starts directly on the same line after
        real code (`False`), or if it starts on its own line (`True`).
        """
        return self.initial_start_column == len(self.code_block_indent)


def format(comment_group: CommentGroup, line_length: int) -> List["SimpleTokenInfo"]:

    # Construct prefix for all lines except the first.
    # Example of such a line:
    # "    #      # Start of comment..."
    # Or:
    # "    # ..this is a simple multiline comment continuation.
    if comment_group.starts_on_its_own_line:
        subsequent_prefix = comment_group.code_block_indent
    else:
        if comment_group.initial_start_column < round(line_length * 2 / 3):
            subsequent_start_column = comment_group.initial_start_column
        else:
            # The text would be too cramped if every subsequent line had this high
            # initial start column. Ergo, make all subsequent lines start a bit earlier.
            subsequent_start_column = line_length // 2
        start = comment_group.code_block_indent + "#"
        whitespace = " " * (subsequent_start_column - len(start))
        subsequent_prefix = start + whitespace

    # Wrap text
    first_line_placeholder = "_" * comment_group.initial_start_column
    comment_prefix = "# "
    wrapped_lines: List[str] = wrap(
        comment_group.full_comment_text,
        width=line_length,
        initial_indent=first_line_placeholder + comment_prefix,
        subsequent_indent=subsequent_prefix + comment_prefix,
    )
    wrapped_lines[0] = wrapped_lines[0].lstrip(first_line_placeholder)

    # Construct output tokens
    output_tokens = []
    for line in wrapped_lines:
        output_tokens.append(SimpleTokenInfo(COMMENT, line))
        output_tokens.append(SimpleTokenInfo(NEWLINE, "\n"))

    # Remove last newline if original group didn't have one.
    if comment_group.tokens[-1].type != NEWLINE:
        output_tokens.pop()

    return output_tokens


SimpleTokenInfo = namedtuple("SimpleTokenInfo", ["type", "string"])
#     Like `tokenize.TokenInfo`, but with only the first two fields. (Namely the only
#     fields required by `untokenize`).
