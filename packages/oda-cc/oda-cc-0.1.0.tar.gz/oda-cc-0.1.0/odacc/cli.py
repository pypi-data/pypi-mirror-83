import click
import logging
import yaml
import json
from collections import defaultdict
from functools import reduce
import os
from nb2workflow.nbadapter import notebook_short_name, NotebookAdapter


class UnsetDict:
    def __init__(self, data):
        self._data = data

    def get(self, k, default):
        return self.__getitem__(k)

    def __getitem__(self, k):
        return self.__class__(
                    self._data.get(
                            k,
                            self.__class__({}),
                        )
                )

    def __str__(self):
        if self._data == {}:
            return "unset"
        return str(self._data)


@click.group()
@click.option("-d", "--debug", is_flag=True, default=False)
@click.option("-C", "--change-dir")
@click.pass_context
def cli(ctx, debug, change_dir=None):
    ctx.obj = {}
    obj = ctx.obj

    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)

    if change_dir is None:
        change_dir = os.getcwd()

    obj["change_dir"] = change_dir

    obj["oda_yaml"] = yaml.load(open(os.path.join(change_dir, "oda.yaml")), Loader=yaml.SafeLoader)

    logging.debug("loaded: %s", obj['oda_yaml'])


@cli.command()
@click.pass_obj
def inspect(obj):
    pass

@cli.command()
@click.argument("path")
@click.argument("default")
@click.pass_obj
def get(obj, path, default):
    try:
        click.echo(reduce(
                lambda x, y: x[y],
                [obj['oda_yaml']] + path.split(".")))
    except (KeyError, TypeError) as e:
        click.echo(default)


@cli.command()
@click.argument("template")
@click.option("-n", "--notebook", default=None)
@click.pass_obj
def format(obj, template, notebook):
    if notebook:
        n = notebook_short_name(notebook)
        nba = NotebookAdapter(notebook)
        pars = nba.extract_parameters()
    else:
        pars=json.load(open(os.path.join(obj["change_dir"], "pars.json")))

    click.echo(
        template.format(
            pars=UnsetDict(pars)
        )
    )

if __name__ == "__main__":
    cli()
