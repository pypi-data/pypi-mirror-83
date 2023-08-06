#! /usr/bin/python3

import argparse, sys, os

from ..core.repository import Repository
from ..view import *


class GitPMList:

    """
    'gitpm list' is a commandline tool to list git projects in a directory.
    """

    @staticmethod
    def error(e):
        GitPMList.parser.error(e)

    @staticmethod
    def generateParser():

        """
        Generate the ArgumentParser for 'gitpm list'.
        """

        GitPMList.parser = argparse.ArgumentParser(
            prog="gitpm list",
            description="The 'gipm-list' tool lists git repositories.",
            epilog="More details at https://github.com/finnmglas/gitPM.",
        )
        GitPMList.parser.add_argument(
            "status",
            default="all",
            choices=["all"] + Repository.status_set,
            nargs="?",
            help="The status of projects filtered for.",
        )

        return GitPMList.parser

    @staticmethod
    def main(args=None, directory=os.getcwd()):

        """
        The main program of 'gitpm list'.
        """

        if args == None:  # parse args using own parser
            GitPMList.generateParser()
            args = GitPMList.parser.parse_args(sys.argv[1:])

        print("GitPM found these repositories:\n")
        printTable(
            [Repository.id_width + 10, 32, 24, Repository.hash_abbr_len],
            [
                [
                    colors_fg.BOLD + r.getId() + colors.ENDC,
                    r.getName(),
                    status_colors[r.getStatus()] + r.getStatus() + colors.ENDC,
                    r.getMasterHash()[0 : Repository.hash_abbr_len],
                ]
                for r in Repository.list(directory)
                if (args.status == "all" or r.getStatus() == args.status)
            ],
        )


if __name__ == "__main__":
    GitPMList.main()
