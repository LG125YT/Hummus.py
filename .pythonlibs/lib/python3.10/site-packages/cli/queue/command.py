import click
from library.functions import queue_lib


@click.command()
@click.pass_obj
def queue(jenkins):
    """Looks up Jenkins' queue."""
    queue_lib(jenkins.url,jenkins.username,jenkins.password)

