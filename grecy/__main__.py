import subprocess
import sys

import typer

from grecy.connections import (
    LATEST_RELEASE_URL,
    ModelNotFoundError,
    ReleaseLookupError,
    find_wheel_url,
)

MODELS = [
    "grc_perseus_sm",
    "grc_perseus_lg",
    "grc_perseus_trf",
    "grc_proiel_sm",
    "grc_proiel_lg",
    "grc_proiel_trf",
    "grc_ner_trf",
]

app = typer.Typer()


def _fail(message: str) -> typer.Exit:
    typer.echo(message, err=True)
    return typer.Exit(code=1)


def _check_model(model: str) -> None:
    if model not in MODELS:
        raise _fail(
            f"Unknown model: {model}\n"
            f"The options in greCy are: {', '.join(MODELS)}"
        )


def _run_pip(*args: str) -> int:
    # sys.executable keeps pip in the environment that is running greCy.
    return subprocess.run([sys.executable, "-m", "pip", *args]).returncode


@app.command()
def install(model: str):
    _check_model(model)

    try:
        wheel_url = find_wheel_url(model)
    except ReleaseLookupError as error:
        raise _fail(
            f"Could not look up the greCy releases at {LATEST_RELEASE_URL}: {error}\n"
            "Please check the network connection."
        )
    except ModelNotFoundError:
        raise _fail(f"No greCy release contains the model {model}.")

    if _run_pip("install", wheel_url) != 0:
        raise _fail(f"There was a problem installing {model} from {wheel_url}")


@app.command()
def uninstall(model: str):
    _check_model(model)

    if _run_pip("uninstall", "--yes", model) != 0:
        raise _fail(f"There was a problem uninstalling {model}")


if __name__ == "__main__":
    app()
