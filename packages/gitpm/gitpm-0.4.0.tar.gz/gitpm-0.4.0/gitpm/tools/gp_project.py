#! /usr/bin/python3

import argparse, sys

from ..core.repository import Repository
from ..view import *


class GitPMProject:

    """
    'gitpm project' is a tool to modify git projects.
    """

    @staticmethod
    def error(e):
        GitPMProject.parser.error(e)

    @staticmethod
    def generateParser():

        """
        Generate the ArgumentParser for 'gitpm project'.
        """

        GitPMProject.parser = argparse.ArgumentParser(
            prog="gitpm project",
            description="The 'gipm-loop' tool can modify git projects.",
            epilog="More details at https://github.com/finnmglas/gitPM.",
        )

        GitPMProject.parser.add_argument("id", help="The project id to work with.")

        projectSubparsers = GitPMProject.parser.add_subparsers(
            dest="op", help="GitPM project operations."
        )
        projectSubparsers.required = True

        # --- --- gipm [project] details
        projectSubparsersDetails = projectSubparsers.add_parser(
            "details", help="View project details."
        )

        # --- --- gipm [project] rename
        projectSubparsersRename = projectSubparsers.add_parser(
            "rename", help="Rename a project."
        )
        projectSubparsersRename.add_argument("name", help="The project's new name.")

        # --- --- gipm [project] status
        projectSubparsersStatus = projectSubparsers.add_parser(
            "setstatus", help="Change a projects maintainance status."
        )
        projectSubparsersStatus.add_argument(
            "status", choices=Repository.status_set, help="The project's new status."
        )

        # --- --- gipm [project] describe
        projectSubparsersDescribe = projectSubparsers.add_parser(
            "describe", help="Edit a project's description."
        )
        projectSubparsersDescribe.add_argument(
            "description", help="The project's new desription."
        )

        # --- --- gipm [project] retag
        projectSubparsersRetag = projectSubparsers.add_parser(
            "retag", help="Edit a project's tags."
        )
        projectSubparsersRetag.add_argument(
            "tags", help="The project's new tags (comma-separated)."
        )

        # --- --- gipm [project] remove
        projectSubparsersRemove = projectSubparsers.add_parser(
            "remove", help="Remove a project (irreversibly)."
        )

        # --- --- gipm [project] execute
        projectSubparsersExecute = projectSubparsers.add_parser(
            "execute", help="Execute a git command."
        )

        return GitPMProject.parser

    @staticmethod
    def main(args=None):

        """
        The main program of 'gitpm project'.
        """

        if args == None:  # parse args using own parser
            GitPMProject.generateParser()
            args = GitPMProject.parser.parse_args(sys.argv[1:])

        project = Repository(Repository.formatId(int(args.id, 16)))

        if args.op == "details":
            print(
                colors_fg.BOLD
                + "Project\t"
                + colors_fg.WHITE
                + project.getName()
                + colors.ENDC
                + colors_fg.BOLD
                + " pid-"
                + project.getId()
                + " "
                + status_colors[project.getStatus()]
                + project.getStatus()
                + colors.ENDC
                + "\n"
            )
            print("About:\t" + project.getDescription() + "")
            print("Tags:\t" + project.getTags() + "\n")
            print("Master:\t" + project.getMasterHash())
        elif args.op == "rename":
            project.setName(args.name)
        elif args.op == "setstatus":
            project.setStatus(args.status)
        elif args.op == "describe":
            project.setDescription(args.description)
        elif args.op == "retag":
            project.setTags(args.tags)
        elif args.op == "remove":
            try:
                if input("Delete repository? (y / n) ") == "y":
                    project.remove()
                    print('Deleted repository "' + project.getName() + '".\n')
                else:
                    raise KeyboardInterrupt
            except KeyboardInterrupt:
                print("Canceled deletion.\n")
        elif args.op == "execute":
            if arguments[1] == "execute":
                project.execute("git " + " ".join(arguments[2:]))
            else:
                project.execute("git " + " ".join(arguments[1:]))


if __name__ == "__main__":
    GitPMProject.main()
