import click

from anyscale.controllers.project_controller import ProjectController


@click.command(
    name="clone",
    short_help="Clone a project that exists on anyscale, to your local machine.",
    help="""Clone a project that exists on anyscale, to your local machine.
This command will create a new folder on your local machine inside of
the current working directory and download the most recent snapshot.

This is frequently used with anyscale push or anyscale pull to download, make
changes, then upload those changes to a currently running session.""",
)
@click.argument("project-name", required=True)
def anyscale_clone(project_name: str) -> None:
    project_controller = ProjectController()
    project_controller.clone(project_name)
