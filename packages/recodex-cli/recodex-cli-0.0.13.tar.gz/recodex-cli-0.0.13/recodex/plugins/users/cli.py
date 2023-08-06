import click
import csv
import sys

from recodex.api import ApiClient
from recodex.config import UserContext
from recodex.decorators import pass_user_context, pass_api_client


@click.group()
def cli():
    """
    Tools for user manipulation
    """


def format_user_csv(user):
    return {
        'id': user['id'],
        'title_before': user['name']['degreesBeforeName'],
        'first_name': user['name']['firstName'],
        'last_name': user['name']['lastName'],
        'title_after': user['name']['degreesAfterName'],
        'avatar_url': user['avatarUrl'],
    }


@cli.command()
@click.argument("search_string")
@click.option('--csv', 'as_csv', is_flag=True, help='Return full records formated into CSV.')
@pass_user_context
@pass_api_client
def search(api: ApiClient, context: UserContext, search_string, as_csv):
    """
    Search for a user
    """

    if as_csv:
        fieldnames = ['id', 'title_before', 'first_name', 'last_name', 'title_after', 'avatar_url']
        csv_writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        csv_writer.writeheader()

    instances_ids = api.get_user(context.user_id)["privateData"]["instancesIds"]
    for instance_id in instances_ids:
        for user in api.search_users(instance_id, search_string):
            if as_csv:
                csv_writer.writerow(format_user_csv(user))
            else:
                click.echo("{} {}".format(user["fullName"], user["id"]))


@cli.command()
@click.argument("email")
@click.argument("first_name")
@click.argument("last_name")
@click.option('--password', help='Password. If no password is given, it is prompted.',
              prompt=True, hide_input=True, confirmation_prompt=True)
@click.option('--instance_id', help='Instance where the new user belongs to. If no instance is provided, instance of logged user is taken.')
@click.option('--join_group', multiple=True, help='Id of a group which is immediately joined by the registered user. This option may be repeated.')
@pass_user_context
@pass_api_client
def register(api: ApiClient, context: UserContext, email, first_name, last_name, password, instance_id, join_group):
    """
    Register new user with local account
    """
    if instance_id is None:
        instances_ids = api.get_user(context.user_id)["privateData"]["instancesIds"]
        if len(instances_ids) != 1:
            click.echo("Instance ID is ambiguous. Provide explicit ID via --instance_id option.")
            return
        instance_id = instances_ids[0]

    res = api.register_user(instance_id, email, first_name, last_name, password)
    user_id = res['user']['id']
    click.echo("User {id} ({first_name} {last_name}, {email}) registered in instance {instance_id}".format(
        id=user_id, first_name=first_name, last_name=last_name, email=email, instance_id=instance_id))

    for group_id in join_group:
        api.group_add_student(group_id, user_id)
        click.echo("User {} joined group {}".format(user_id, group_id))


@cli.command()
@click.argument("id")
@click.option("--name", nargs=2, help="New name as two arguments (first_name last_name).")
@click.option("--gravatar/--no-gravatar")
@pass_api_client
def edit(api: ApiClient, id, name, gravatar):
    """
    Edit profile of a user
    """

    user = api.get_user(id)
    data = {
        "degreesAfterName": user['name']['degreesBeforeName'],
        "degreesBeforeName": user['name']['degreesAfterName'],
        "email": user["privateData"]["email"],
        "gravatarUrlEnabled": user['avatarUrl'] is not None,
    }

    if name is not None:
        data["firstName"] = name[0]
        data["lastName"] = name[1]

    if gravatar is not None:
        data["gravatarUrlEnabled"] = gravatar
    api.update_user(id, data)


@cli.command()
@click.argument("id")
@pass_api_client
def enable(api: ApiClient, id):
    """
    Enable user (who was previously disabled)
    """

    api.set_allow_user(id, True)


@cli.command()
@click.argument("id")
@pass_api_client
def disable(api: ApiClient, id):
    """
    Disable user (the user will no longer be allowed to log in or perform any other API calls)
    """

    api.set_allow_user(id, False)


@cli.command()
@click.argument("id")
@pass_api_client
def delete(api: ApiClient, id):
    """
    Delete user (users are only soft-deleted)
    """

    api.delete_user(id)
