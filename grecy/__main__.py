import typer
import os
from grecy.connections import access_to
from grecy.__version__ import __version__

app = typer.Typer()

@app.command()
def install(model: str):

    models = ["grc_perseus_sm","grc_perseus_lg","grc_perseus_trf","grc_proiel_sm","grc_proiel_lg","grc_proiel_trf"]

    hf_url = "https://huggingface.co/"

    if model in models:

        # Checking the access to Hugging Face
        if not access_to(hf_url):
            print(f'The access to {hf_url} is not possible.')
            print(f'Please, check the network connection.')
            exit(0)

        # The url for the model
        https = hf_url + "Jacobo/" + model + "/resolve/main/" + model + "-" + __version__ + "-py3-none-any.whl"

        # The pip command
        pip_command = "python -m pip install " + https

        try:
            os.system(pip_command)

        except Exception as e:

            print(f'There is a problem installing the model: {pip_command}')
            print(f'Below the related information:')
            print(f'{str(e)}')

    else:
        print('\n' + f'Please, check the model required. The options in greCy are:')
        print([model for model in models])


@app.command()
def uninstall(model: str):

    models = ["grc_perseus_sm","grc_perseus_lg","grc_perseus_trf","grc_proiel_sm","grc_proiel_lg","grc_proiel_trf"]

    if model in models:

        pip_command = "python -m pip uninstall --yes " + model

        try:
            os.system(pip_command)

        except Exception as e:

            print(f'There is a problem uninstalling: {model}')
            print(f'Below the related information:')
            print(f'{str(e)}')
    else:
        print('\n' + f'Please, check the model required. The options in greCy are:')
        print([model for model in models])

if __name__ == "__main__":

    app()
