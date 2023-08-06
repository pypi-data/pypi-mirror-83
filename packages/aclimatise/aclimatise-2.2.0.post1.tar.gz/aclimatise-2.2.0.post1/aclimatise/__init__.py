import logging
import pty
import subprocess
import typing

import dataclasses
import psutil
from pyparsing import ParseBaseException

from aclimatise.converter import WrapperGenerator
from aclimatise.converter.cwl import CwlGenerator
from aclimatise.converter.wdl import WdlGenerator
from aclimatise.converter.yml import YmlGenerator
from aclimatise.execution import Executor
from aclimatise.execution.local import LocalExecutor
from aclimatise.flag_parser.parser import CliParser
from aclimatise.model import Command, Flag
from aclimatise.usage_parser.parser import UsageParser

logger = logging.getLogger("aclimatise")

default_executor = LocalExecutor()


def _combine_flags(
    flag_lists: typing.Iterable[typing.Iterable[Flag]],
) -> typing.Iterable[Flag]:
    """
    Combines the flags from several sources, choosing the first one preferentially
    """
    lookup = {}

    # Build a list of flags, but only ever choose the first instance of a synonym
    for flags in flag_lists:
        for flag in flags:
            for synonym in flag.synonyms:
                stripped = synonym.lstrip("-")
                if stripped not in lookup:
                    lookup[stripped] = flag

    # Now, make them unique by description
    unique = {flag.longest_synonym: flag for flag in lookup.values()}

    return list(unique.values())


def parse_help(cmd: typing.Collection[str], text: str, max_length=1000) -> Command:
    """
    Parse a string of help text into a Command. Use this if you already have run the executable and extracted the
    help text yourself

    :param cmd: List of arguments used to generate this help text, e.g. ['bwa', 'mem']
    :param text: The help text to parse
    :param max_length: If the input text has more than this many lines, no attempt will be made to parse the file (as
        it's too large, will likely take a long time, and there's probably an underlying problem if this has happened).
        In this case, an empty Command will be returned
    """
    if len(text.splitlines()) > max_length:
        return Command(list(cmd))

    help_command = CliParser().parse_command(name=cmd, cmd=text)
    usage_command = UsageParser().parse_usage(list(cmd), text)

    # Combine the two commands by picking from the help_command where possible, otherwise falling back on the usage
    fields = dict(
        help_text=text,
        # Use the help command's positionals preferentially, but fall back to usage
        positional=help_command.positional or usage_command.positional,
        # Combine the flags from both help and usage
        named=list(_combine_flags([help_command.named, usage_command.named])),
    )
    for field in dataclasses.fields(Command):
        fields[field.name] = (
            fields.get(field.name)
            or getattr(help_command, field.name)
            or getattr(usage_command, field.name)
        )

    return Command(**fields)


def best_cmd(
    cmd: typing.List[str],
    flags: typing.Iterable[str] = (["--help"], ["-h"], [], ["--usage"]),
    executor: Executor = default_executor,
) -> Command:
    """
    Determine the best Command instance for a given command line tool, by trying many
    different help flags, such as --help and -h, then return the Command. Use this if you know the command you want to
    parse, but you don't know which flags it responds to with help text. Unlike :py:func:`aclimatise.explore_command`,
    this doesn't even attempt to parse subcommands.

    :param cmd: The command to analyse, e.g. ['wc'] or ['bwa', 'mem']
    :param flags: A list of help flags to try, e.g. ['--help', '-h'], in order how which one you would prefer to use.
    Generally [] aka no flags should be last
    :param executor: A class that provides the means to run a command. You can use the pre-made classes or write your own.
    """
    # For each help flag, run the command and then try to parse it
    logger.info("Trying flags for {}".format(" ".join(cmd)))
    commands = []
    for flag in flags:
        help_cmd = cmd + flag
        logger.info("Trying {}".format(" ".join(help_cmd)))
        try:
            final = executor.execute(help_cmd)
            result = parse_help(cmd, final)
            result.generated_using = flag
            commands.append(result)
        except (ParseBaseException, UnicodeDecodeError) as e:
            # If parsing fails, this wasn't the right flag to use
            continue

    # Sort by flags primarily, and if they're equal, return the command with the longest help text, and if they're equal
    # return the command with the most help flags. This helps ensure we get ["bedtools", "--help"] instead of
    # ["bedtools"]
    best = max(
        commands,
        key=lambda com: (
            len(com.named) + len(com.positional),
            # len(com.help_text) if com.help_text else 0,
        ),
    )
    logger.info(
        "The best help flag seems to be {}".format(
            " ".join(best.command + best.generated_using)
        )
    )
    return best


def is_subcommand(command: Command, parent: Command) -> bool:
    """
    Returns true if command is a valid subcommand, relative to its parent
    """
    # Recursively call this on all ancestors
    if parent.parent is not None and not is_subcommand(command, parent.parent):
        return False

    # This isn't a subcommand if it has the same input text as the parent
    if command.help_text and command.help_text == parent.help_text:
        return False

    # This isn't a subcommand if it has no flags
    if len(command.positional) + len(command.named) == 0:
        return False

    # This isn't a subcommand if it shares any positional with the parent command
    for pos_a, pos_b in zip(parent.positional, command.positional):
        if pos_a == pos_b:
            return False

    # This isn't a subcommand if it shares any flags with the parent command
    for flag_a, flag_b in zip(parent.named, command.named):
        if flag_a == flag_b:
            return False

    return True


def explore_command(
    cmd: typing.List[str],
    flags: typing.Iterable[str] = (["--help"], ["-h"], [], ["--usage"]),
    parent: typing.Optional[Command] = None,
    max_depth: int = 2,
    try_subcommand_flags=True,
    executor: Executor = default_executor,
) -> typing.Optional[Command]:
    """
    Given a command to start with, builds a model of this command and all its subcommands (if they exist).
    Use this if you know the command you want to parse, you don't know which flags it responds to with help text, and
    you want to include subcommands.

    :param cmd: Command line executable and arguments to explore
    :param flags: A list of help flags to try, e.g. ['--help', '-h'], in order how which one you would prefer to use.
    Generally [] aka no flags should be last
    :param parent: A parent Command to add this command to as a subcommand, if this command actually exists
    :param executor: A class that provides the means to run a command. You can use the pre-made classes or write your own.
    :param try_subcommand_flags: If true, try all the ``flags`` on each subcommand. If False, we choose
    the best help flag on the parent command and then use that same one on each child. Generally True is recommended
    since some tools (such as bedtools) use different help flags for subcommands
    """
    logger.info("Exploring {}".format(" ".join(cmd)))
    command = best_cmd(cmd, flags, executor=executor)

    # Check if this is a valid subcommand
    if parent:
        if is_subcommand(command, parent):
            logger.info("{} seems to be a valid subcommand".format(" ".join(cmd)))
            command.parent = parent
        else:
            logger.info(
                "{} does not seem to be a valid subcommand".format(" ".join(cmd))
            )
            return None

    # Recursively call this function on positionals, but only do this if we aren't at max depth
    if command.depth < max_depth:
        # By default we use the best parent help-flag
        child_flags = flags if try_subcommand_flags else [command.generated_using]

        # Try each *unique* positional
        for positional in {positional.name for positional in command.positional}:
            subcommand = explore_command(
                cmd=cmd + [positional],
                flags=child_flags,
                parent=command,
                max_depth=max_depth,
                executor=executor,
                try_subcommand_flags=try_subcommand_flags,
            )
            if subcommand is not None:
                command.subcommands.append(subcommand)
                # If we had any subcommands then we probably don't have any positionals, or at least don't care about them
                command.positional = []

    return command
