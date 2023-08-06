#! /usr/bin/python3

import argparse, sys, os

from ..core.repository import Repository


class GitPMCreate:

    """
    'gitpm create' is a commandline tool to create new git projects.
    """

    @staticmethod
    def error(e):
        GitPMCreate.parser.error(e)

    @staticmethod
    def generateParser():

        """
        Generate the ArgumentParser for 'gitpm create'.
        """

        GitPMCreate.parser = argparse.ArgumentParser(
            prog="gitpm create",
            description="The 'gipm-create' tool create git repositories.",
            epilog="More details at https://github.com/finnmglas/gitPM.",
        )
        GitPMCreate.parser.add_argument("name", help="The name of the new project.")

        return GitPMCreate.parser

    @staticmethod
    def main(args=None, directory=os.getcwd()):

        """
        The main program of 'gitpm create'.
        """

        if args == None:  # parse args using own parser
            GitPMCreate.generateParser()
            args = GitPMCreate.parser.parse_args(sys.argv[1:])

        r = Repository.create(directory, args.name)
        print("\nNew project id: " + r.getId() + ".\n")


if __name__ == "__main__":
    GitPMCreate.main()
