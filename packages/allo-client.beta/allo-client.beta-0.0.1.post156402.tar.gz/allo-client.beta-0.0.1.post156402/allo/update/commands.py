import os
import click
from allo.model.colors import BColors
from allo.model.config import AlloConfig
from allo.telem.telem import TelemUtil
from allo.utils.api import API


def exit_if_no_conf():
    if not hasattr(AlloConfig.load(), "repo_path"):
        BColors.error("Produit non installé ou non détecté.")
        exit(1)


@click.group(invoke_without_command=True)
@click.argument('version', required=False)
def update(version=""):
    """
    Liste les versions disponibles à la mise à jour.

    Si VERSION est renseigné, une mise à jour vers VERSION est déclenchée.

    \b
    VERSION est le numéro de version vers laquelle mettre à jour.
    Si VERSION = "latest", la dernière version disponible sera déployée.
    """
    exit_if_no_conf()
    if version is None:
        from allo.utils.api import API
        print("Versions disponibles :")
        result = API.get_versions()
        for version in result:
            print("- {}".format(version["name"].split(" ")[1]))
    else:
        TelemUtil.telem_start()
        update_to_version(version)


def update_to_version(version):
    result = API.get_versions()
    if len(result) == 0:
        BColors.success("Vous êtes déjà dans la version version disponible")
    else:
        toupdate = None
        if version == "latest":
            toupdate = result[0]
        else:
            for ver in result:
                if ver["name"].split(" ")[1] == version:
                    toupdate = ver

        if toupdate is not None:
            update_request(toupdate)
        else:
            BColors.error("Version indisponible")


def update_request(version):
    BColors.warning("Une mise à jour en version {} va être déclenchée. "
                    "Confirmer ? [o/N] ".format(version["name"].split(" ")[1]))
    confirm = input()
    if confirm.lower() == "o":
        if API.update_to_version(version["id"]):
            BColors.info("Mise à jour en version {}...".format(version["name"].split(" ")[1]))

            progress_file = "/tmp/progress.log"
            if os.path.exists(progress_file):
                os.remove(progress_file)

            from allo.utils.logreader import LogReader
            logreader = LogReader(1, progress_file, True)
            logreader.start()
            logreader.join()

        else:
            BColors.error("Erreur lors de la demande de mise à jour")
