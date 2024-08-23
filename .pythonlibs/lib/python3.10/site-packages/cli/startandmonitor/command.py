import click
import sys
import ast
import pprint
import jenkins as jenkinsapi
from time import sleep
from library.functions import startandmonitor_lib


@click.command()
@click.option('--job',required=True, help='Name of the job to start and monitor.')
@click.option('--token',default=None, help='Token to access the job.')
@click.option('--wait',required=True, help='Time to wait between each request to check the build\'s status.',type=int)
@click.option('--parameters',required=False, help='Job\'s parameters.')
@click.pass_obj
def startandmonitor(jenkins,job, parameters, wait, token):
    """Starts and monitors a Jenkins job until it is finished."""
    return startandmonitor_lib(jenkins.url,jenkins.username,jenkins.password, job, parameters, wait, token)