import click
from library.functions import startjob_lib



@click.command()
@click.option('--job',required=True,help='Name of the job to start.')
@click.option('--parameters',required=False, help='Job\s parameters.')
@click.option('--token',default=None, help='Token to access the job.')
@click.pass_obj
def startjob(jenkins,job, parameters, token):
    """Starts a Jenkins job."""
    startjob_lib(jenkins.url, jenkins.username, jenkins.password, job, parameters, token)

