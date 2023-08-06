import click

from grid import Grid


@click.group(invoke_without_command=True)
@click.pass_context
def slurm(ctx) -> None:
    """Manages SLURM workflows in Grid"""
    return


def _check_is_python_script(ctx, _param, value):
    """Click callback that checks if a file is a Python script."""
    if value is not None:
        if not value.endswith('.py'):
            raise click.BadParameter('You must provide a Python script. '
                                     'No script detected.')

        ctx.params['entrypoint'] = value
        return value


@slurm.command()
@click.argument('alias', required=False, type=str)
@click.pass_context
def get_token(ctx, alias: str) -> None:
    """Get's an auth token for registering a grid-daemon in a SLURM cluster."""
    client = Grid()

    client.get_slurm_auth_token()


@slurm.command(context_settings=dict(ignore_unknown_options=True))
@click.argument('script',
                required=False,
                type=click.Path(exists=True),
                callback=_check_is_python_script)
@click.pass_context
def train(ctx, script: str) -> None:
    """Trains on a SLURM cluster"""
    click.echo("Testing new command.")
