import click
from tabulate import tabulate

from flipflop import flipflop


@click.command()
@click.option("--inline-input", "-i", help="Singular inline expression to execute")
@click.option(
    "--simple",
    "-s",
    help="Only include variables and final expression",
    is_flag=True,
    default=False,
)
@click.option(
    "--table-format",
    "-t",
    help="Chosen table format (see python-tabulate for more details)",
    default="simple_grid",
)
def main(inline_input: str | None, simple: bool, table_format: str) -> int:
    try:
        results = flipflop(inline_input, full=not simple)
    except Exception as e:
        click.secho(e, fg="red")
        return 1

    click.echo(
        tabulate(results["values"], headers=results["header"], tablefmt=table_format)
    )

    if results["is_tautology"]:
        click.secho("Expression IS a tautology", fg="green")
    else:
        click.secho("Expression IS NOT a tautology", fg="red")

    return 0


if __name__ == "__main__":
    main()
