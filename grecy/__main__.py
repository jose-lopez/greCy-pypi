from platform import release

import typer
import os
from grecy.connections import access_to, get_release


app = typer.Typer()

@app.command()
def install(model: str):

    models = ["grc_perseus_sm","grc_perseus_lg","grc_perseus_trf","grc_proiel_sm","grc_proiel_lg","grc_proiel_trf", "grc_ner_trf"]

    git_url = "https://github.com/jmyerston/greCy/releases/download/"
    git_release_url_to_check = "https://github.com/jmyerston/greCy/releases/tag/v3.7.5"
    git_release = "https://github.com/jmyerston/greCy/releases/latest"

    if model in models:

        # Checking the access to Hugging Face
        if not access_to(git_release_url_to_check):
            print(f'The access to {git_release_url_to_check} is not possible.')
            print(f'Please, check the network connection.')
            exit(0)

        latest_release = get_release(git_release)

        # The url for the model
        https = git_url + "v" + latest_release + "/" + model + "-" + latest_release + "-" + "py3-none-any.whl"

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

    models = ["grc_perseus_sm","grc_perseus_lg","grc_perseus_trf","grc_proiel_sm","grc_proiel_lg","grc_proiel_trf", "grc_ner_trf"]

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