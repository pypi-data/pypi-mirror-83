import sys

import click
from gkeepapi.exception import LabelException

from google_keep_tasks.cli import GkeepGroup
from google_keep_tasks.utils import pretty_date


def format_label(label):
    return u'━ {}'.format(label)


def format_label_with_timestaps(label):
    return u'{} (created {}, updated {})'.format(
        format_label(label),
        pretty_date(label.timestamps.created),
        pretty_date(label.timestamps.updated),
    )


@click.group(cls=GkeepGroup)
def labels():
    """List, create, rename or delete labels using ``labels`` command.
    This command has subcommands for adding, searching, editing, or
    deleting labels. To see all subcommands of ``labels`` use ``--help``::

        gkeep labels --help

    An example of a subcommand is ``add``. To see help use
    ``gkeep labels add --help``.
    """
    pass


@labels.command('list', options_metavar='[options]')
@click.option('--timestamps', is_flag=True, help='Include timestaps per each label.')
@click.pass_context
def list_labels(ctx, timestamps):
    """List labels on Google Keep. For example:

    .. code-block:: shell

        gkeep labels list

    The syntax is:
    """
    keep = ctx.obj['keep']
    fmt = format_label_with_timestaps if timestamps else format_label
    click.echo(u'\n'.join([
         fmt(label) for label in keep.labels()]
    ))


@labels.command('add', options_metavar='[options]')
@click.argument('title', metavar='<title>')
@click.pass_context
def add_label(ctx, title):
    """Create a label on Google Keep. For example:

    .. code-block:: shell

        gkeep labels create "Label name"

    The syntax is:
    """
    keep = ctx.obj['keep']
    try:
        keep.createLabel(title)
    except LabelException as e:
        click.echo(u'Error creating label: {}'.format(e), err=True)
        sys.exit(3)
    keep.sync()
    click.echo(f'Created label {title}')


@labels.command('edit', options_metavar='[options]')
@click.argument('old_title', metavar='<old_title>')
@click.argument('title', metavar='<new_title>')
@click.pass_context
def edit_label(ctx, old_title, title):
    """Rename a label title. For example:

    .. code-block:: shell

        gkeep labels edit "Old title" "New title"

    The syntax is:
    """
    keep = ctx.obj['keep']
    label = keep.findLabel(old_title)
    if not label:
        click.echo(u'The label was not found', err=True)
        sys.exit(2)
    new_label = keep.findLabel(title)
    if new_label:
        click.echo(u'The label {} already exists'.format(title), err=True)
        sys.exit(2)
    label.name = title
    keep.sync()
    click.echo(f'Renamed label {old_title} to {title}')


@labels.command('delete', options_metavar='[options]')
@click.argument('title', metavar='<title>')
@click.pass_context
def edit_label(ctx, title):
    """Delete a label. For example:

    .. code-block:: shell

        gkeep labels delete "Label name"

    The syntax is:
    """
    keep = ctx.obj['keep']
    label = keep.findLabel(title)
    if label and (label.deleted or label.trashed):
        click.echo(u'The label "{}" had already been deleted.'.format(title), err=True)
        sys.exit(2)
    elif label:
        keep.deleteLabel(label)
        keep.sync()
        click.echo('Label "{}" deleted.'.format(title))
    else:
        click.echo('The label was not found', err=True)
        sys.exit(2)
