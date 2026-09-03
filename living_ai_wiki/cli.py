from pathlib import Path

import typer

from living_ai_wiki.config import ConfigError, validate_experiment_config

app = typer.Typer(help="Living AI Wiki experiment utilities.", no_args_is_help=True)


@app.callback()
def main() -> None:
    """Run repository and experiment utilities."""


@app.command("validate-config")
def validate_config(path: Path) -> None:
    """Validate an experiment YAML without running an experiment."""
    try:
        config = validate_experiment_config(path)
    except ConfigError as exc:
        typer.echo(f"invalid: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(f"valid: {config['experiment_id']}")


if __name__ == "__main__":
    app()
