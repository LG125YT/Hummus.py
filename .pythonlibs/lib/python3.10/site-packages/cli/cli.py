import click
from startjob import command as startjob
from startandmonitor import command as startandmonitor
from queue import command as queue


class Jenkins(object):
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password


@click.group()
@click.option('--url',help='Protocol+Url+Port of the Jenkins server. [required]')
@click.option('--username', default=None, help='Username. [required]')
@click.option('--password',default=None, help='Password. [required]')
@click.pass_context
def entry_point(ctx,url,username, password):
    ctx.obj = Jenkins(url,username,password)

entry_point.add_command(startjob.startjob)
entry_point.add_command(startandmonitor.startandmonitor)
entry_point.add_command(queue.queue)


if __name__ == '__main__':
    entry_point()
