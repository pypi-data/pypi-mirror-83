import click
from glob import glob
import os

from .__about__ import __version__
from grvlms.commands import cli, compose, context, local
from grvlms.commands.compose import ScriptRunner
from grvlms.commands import config as config_cli
from grvlms.commands.context import Context
from grvlms import config as grvlms_config
from grvlms import env
from grvlms import interactive
from grvlms import scripts
from grvlms import utils

BASE_OPENEDX_COMMAND = """
export DJANGO_SETTINGS_MODULE=$SERVICE_VARIANT.envs.$SETTINGS
echo "Loading settings $DJANGO_SETTINGS_MODULE"
"""

HERE = os.path.abspath(os.path.dirname(__file__))

templates = os.path.join(HERE, "templates")

config = {
    "add": {
        "ACTIVATE_AZURE": True,
        "AZURE_CLIENT_ID": "",
        "AZURE_SECRET_KEY": "",

        "ACTIVATE_GOOGLE": False,
        "GOOGLE_CLIENT_ID": "",
        "GOOGLE_SECRET_KEY": "",
    }
}

hooks = {
    "init": ["lms"],
}


def patches():
    all_patches = {}
    for path in glob(os.path.join(HERE, "patches", "*")):
        with open(path) as patch_file:
            name = os.path.basename(path)
            content = patch_file.read()
            all_patches[name] = content
    return all_patches


class LocalContext(Context):
    @staticmethod
    def docker_compose(root, config, *command):
        args = []
        override_path = env.pathjoin(
            root, "local", "docker-compose.override.yml"
        )
        if os.path.exists(override_path):
            args += ["-f", override_path]
        return utils.docker_compose(
            "-f",
            env.pathjoin(root, "local", "docker-compose.yml"),
            *args,
            "--project-name",
            config["LOCAL_PROJECT_NAME"],
            *command
        )


class DevContext(Context):
    @staticmethod
    def docker_compose(root, config, *command):
        args = [
            "-f",
            env.pathjoin(root, "local", "docker-compose.yml"),
        ]
        override_path = env.pathjoin(
            root, "local", "docker-compose.override.yml"
        )
        if os.path.exists(override_path):
            args += ["-f", override_path]
        args += [
            "-f",
            env.pathjoin(root, "dev", "docker-compose.yml"),
        ]
        override_path = env.pathjoin(root, "dev", "docker-compose.override.yml")
        if os.path.exists(override_path):
            args += ["-f", override_path]
        return utils.docker_compose(
            *args, "--project-name", config["DEV_PROJECT_NAME"], *command,
        )


@click.group(help="Extra Command for Social Oauth")
@click.option("--dev", is_flag=True, help="Start in Dev")
@click.pass_context
def command(context, dev):
    if dev:
        context.obj = DevContext(
            context.obj.root, context.obj.user, context.obj.remote_config
        )
    else:
        context.obj = LocalContext(
            context.obj.root, context.obj.user, context.obj.remote_config
        )


def ask_questions_socialoauth(config, defaults):
    # Azure SSO
    interactive.ask_bool(
        "Could you want to enable azure image feature:",
        "SOCIALOAUTH_ACTIVATE_AZURE",
        config,
        {"SOCIALOAUTH_ACTIVATE_AZURE": False})
    interactive.ask(
        "Your Azure Client ID:",
        "SOCIALOAUTH_AZURE_CLIENT_ID",
        config,
        {"SOCIALOAUTH_AZURE_CLIENT_ID": ""})
    interactive.ask(
        "Your Azure Secret key:",
        "SOCIALOAUTH_AZURE_SECRET_KEY",
        config,
        {"SOCIALOAUTH_AZURE_SECRET_KEY": ""})
    # Google SSO
    interactive.ask_bool(
        "Could you want to enable google image feature:",
        "SOCIALOAUTH_ACTIVATE_GOOGLE",
        config,
        {"SOCIALOAUTH_ACTIVATE_GOOGLE": False})
    interactive.ask(
        "Your Google Client ID:",
        "SOCIALOAUTH_GOOGLE_CLIENT_ID",
        config,
        {"SOCIALOAUTH_GOOGLE_CLIENT_ID": ""})
    interactive.ask(
        "Your Google Secret key:",
        "SOCIALOAUTH_GOOGLE_SECRET_KEY",
        config,
        {"SOCIALOAUTH_GOOGLE_SECRET_KEY": ""})


def load_config_socialoauth(root, interactive=True):
    defaults = grvlms_config.load_defaults()
    config = grvlms_config.load_current(root, defaults)
    if interactive:
        ask_questions_socialoauth(config, defaults)
    return config, defaults


@click.command(help="Print socialoauth version", name="version")
def print_version():
    click.secho("The version is: {}".format(__version__), fg="blue")


@click.command(help="Update Provider Config", name="update")
@click.pass_obj
def update(context):
    config = grvlms_config.load(context.root)
    runner = ScriptRunner(context.root, config, context.docker_compose)
    command = BASE_OPENEDX_COMMAND
    if config.get("SOCIALOAUTH_ACTIVATE_GOOGLE"):
        command += """
        ./manage.py lms update_googlesso
        """
    if config.get("SOCIALOAUTH_ACTIVATE_AZURE"):
        command += """
        ./manage.py lms update_azuresso
        """
    runner.exec("lms", command)


@click.command(help="Init plugin", name="init")
@click.pass_obj
def init(context):
    local.local.callback()
    compose.initialise_plugin("init")


@click.command(help="Config socialoauth variables", name="config")
@click.option("-i", "--interactive", is_flag=True, help="Run interactively")
@click.option("-s", "--set", "set_",
              type=config_cli.YamlParamType(),
              multiple=True,
              metavar="KEY=VAL",
              help="Set a configuration value")
@click.pass_obj
def config_social(context, interactive, set_):
    config, defaults = load_config_socialoauth(
        context.root, interactive=interactive
    )
    if set_:
        grvlms_config.merge(config, dict(set_), force=True)
    grvlms_config.save_config_file(context.root, config)
    grvlms_config.merge(config, defaults)
    env.save(context.root, config)


command.add_command(print_version)
command.add_command(init)
command.add_command(update)
command.add_command(config_social)
