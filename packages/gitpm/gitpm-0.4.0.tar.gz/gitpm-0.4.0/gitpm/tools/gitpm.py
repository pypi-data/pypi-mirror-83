#! /usr/bin/python3

import argparse, sys, os

from ..core.repository import Repository

from .gp_list import GitPMList
from .gp_create import GitPMCreate
from .gp_loop import GitPMLoop
from .gp_project import GitPMProject


class GitPM:

    """
    The 'gitpm' cli simplifies repository management.
    """

    tools = {
        "list": GitPMList,
        "create": GitPMCreate,
        "loop": GitPMLoop,
        "project": GitPMProject,
    }

    @staticmethod
    def error(e):
        GitPM.parser.error(e)

    @staticmethod
    def generateParser():

        """
        Generate the ArgumentParser for 'gitpm'.
        """

        GitPM.parser = argparse.ArgumentParser(
            description="Manage multiple bare git-repositories.",
            epilog="More details at https://github.com/finnmglas/gitpm.",
        )

        subparsers = GitPM.parser.add_subparsers(dest="tool", help="GitPM tools")
        subparsers.required = True

        for name in GitPM.tools:
            tool = GitPM.tools[name]
            # Import Parser --- ledgerman [name]
            toolParser = subparsers.add_parser(name)
            toolParser.__dict__ = tool.generateParser().__dict__

        return GitPM.parser

    @staticmethod
    def main(directory=os.getcwd()):
        # generate parser
        GitPM.generateParser()

        # --- if argv[0] is project id: run a project op
        argv = sys.argv[1:]
        if (
            len(argv)
            and Repository.isId(argv[0])
            and Repository.formatId(argv[0]) in Repository.listIds(directory)
        ):
            argv = ["project"] + argv
        if len(argv) > 2 and argv[0] == "project":
            if argv[2] == "execute":
                argv = argv[:3]
            elif argv[2] in Repository.git_argument_set:
                argv = argv[:2] + ["execute"]

        # parse args
        args = GitPM.parser.parse_args(argv)

        # forward args to a tool
        GitPM.tools[args.tool].main(args)


if __name__ == "__main__":
    GitPM.main()
