# -*- coding: utf-8 -*-
"""alfredyang@pharbers.com.

This module document the usage of class phCommand,
which help users to create, update, and publish the jobs they created.
"""
import click
from ph_max_auto.phcontext.phcontextfacade import PhContextFacade


@click.command()
@click.option("-r", "--runtime", prompt="Your programming language is", help="You use programming language.",
              type=click.Choice(["python3", "r"]), default="python3")
@click.option("--cmd", prompt="Your command is", help="The command that you want to process.",
              type=click.Choice(["create", "combine", "dag", "publish", "run", "submit", "status"]))
@click.option("-p", "--path", prompt="Your config and python job file directory",
              help="The concert job you want the process.")
@click.option("-n", "--namespace", help="submit namespace", default="")
@click.option("-c", "--context", help="submit context", default="{}")
@click.argument('args', nargs=1, default="{}")
def maxauto(runtime, cmd, path, namespace, context, args):
    """The Pharbers Max Job Command Line Interface (CLI)
        --runtime Args: \n
            python: This is to see \n
            R: This is to see \n

        --cmd Args: \n
            create: to generate a job template \n
            combine: to combine job into a job sequence \n
            publish: to publish job to pharbers IPaaS \n

        --path Args: \n
            the dictionary that specify the py and yaml file
    """
    facade = PhContextFacade(runtime, cmd, path, namespace, context, args)
    click.get_current_context().exit(facade.execute())
