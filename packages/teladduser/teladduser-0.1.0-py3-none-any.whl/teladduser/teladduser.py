import time
import traceback
from collections import OrderedDict
from datetime import datetime

import click
import rows
from decouple import config, UndefinedValueError
from telethon.errors import (
    FloodWaitError,
    PeerFloodError,
    UserChannelsTooMuchError,
    UserPrivacyRestrictedError,
)
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerChannel, InputPeerEmpty


@click.command()
@click.option('--file', '-f', default=None,
              help='A SpreadSheet with User names to add into a Telegram Supergroup. This parameter is mandatory.')
@click.option('--time_sleep', '-t', default=900,
              help='Time to sleep for each 20 insertions, the default is 900 seconds. '
                   'It is needed to avoid Flood Error and account to be banned.')
def teladduser(file, time_sleep):
    """
    Log in on a Telegram account and add a users in a Supergroup from a SpreadSheet
    which the account logged in is admin.
    """

    # Verify if the Excel SpreadSheet was give!
    if not file:
        print('Need to pass the Excel SpreadSheet Filename!\n')
        click.Context(teladduser).exit(code=1)

    # Login on a Telegram account
    try:
        api_id = config('API_ID')
        api_hash = config('API_HASH')
        phone = config('PHONE')
        client = TelegramClient(phone, api_id, api_hash)
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(phone)
            login_code = click.prompt('Enter the Login Code that was send to yor Telegram app', type=int)
            client.sign_in(phone, login_code)
    except UndefinedValueError:
        print(
            'The environment variables API_ID, API_HASH or PHONE were not defined. '
            'Please create a .env file with they!\n'
        )
        click.Context(teladduser).exit(code=1)

    # Get all Groups of the logged user
    chats = []
    last_date = None
    chunk_size = 100
    groups = []
    result = client(
        GetDialogsRequest(
            offset_date=last_date,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=chunk_size,
            hash=0
        )
    )

    # Get only the super group of the logged user
    chats.extend(result.chats)
    for chat in chats:
        try:
            if chat.megagroup:
                groups.append(chat)
        except:
            continue

    # Select a group to add users
    for i, g in enumerate(groups):
        print(f"{i + 1} - {g.title}")
    g_index = click.prompt("\nEnter Number of Group you want add users", type=int)
    try:
        target_group = groups[int(g_index) - 1]
    except IndexError:
        print('\nThe number selected was not of a valid Group number! Please try again!\n')
        click.Context(teladduser).exit(code=1)

    target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

    print(f'\nReading the file {file}, this will take a while ...\n')
    users_to_add = rows.import_from_xlsx(file)

    # Create a new Rows Table to save processed data
    fields = OrderedDict(
        [
            ('username_normal', rows.fields.TextField),
            ('nome', rows.fields.TextField),
            ('grupocanal', rows.fields.TextField),
            ('conta_de_envio', rows.fields.IntegerField),
            ('log', rows.fields.TextField)
        ]
    )
    users_added = rows.Table(fields=fields)

    n = 0
    for i, user in enumerate(users_to_add):
        if user.log:
            users_added.append(
                {
                    'username_normal': user.username_normal,
                    'nome': user.nome,
                    'grupocanal': user.grupocanal,
                    'cont_a_de_envio': user.conta_de_envio,
                    'log': user.log,
                }
            )
        elif i >= 45:
            try:
                print(f'Adicionando usuário: {i} - {user.nome}')
                user_to_add = client.get_input_entity(user.username_normal)
                client(InviteToChannelRequest(target_group_entity, [user_to_add]))
                log = f"Usuário inserido em: {datetime.strftime(datetime.today(), '%Y-%m-%d às %H:%M:%S')}"
                users_added.append(
                    {
                        'username_normal': user.username_normal,
                        'nome': user.nome,
                        'grupocanal': target_group.title,
                        'cont_a_de_envio': user.conta_de_envio,
                        'log': log,
                    }
                )
                n += 1
                if n % 20 == 0:
                    print(f'\nWaiting {time_sleep / 60} minutes to avoid Flood Error.\n')
                    time.sleep(time_sleep)
                else:
                    time.sleep(time_sleep / 15)
            except PeerFloodError:
                print(
                    "\nGetting Flood Error from telegram. Script is stopping now. Please try again after some time.\n"
                )
                try:
                    rows.export_to_xlsx(users_added, "usersAddedBeforeFloodError.xlsx")
                except:
                    print('\nCould not write to the file provided!\n')
                click.Context(teladduser).exit(code=1)
            except UserPrivacyRestrictedError:
                print("\nThe user's privacy settings do not allow you to do this. Skipping.\n")
            except ValueError as err:
                print(f'\n{err} - Skipping.\n')
            except UserChannelsTooMuchError:
                print(
                    f'\nThe user {user.username_normal} you tried to add is already in too many channels/supergroups\n')
            except FloodWaitError as err:
                print('\nHave to sleep', err.seconds, 'seconds\n')
                time.sleep(err.seconds)
            except KeyboardInterrupt:
                print('\nExecution was interrupted by user.\n')
                click.Context(teladduser).exit(code=1)
            except:
                traceback.print_exc()
                print("\nUnexpected Error\n")
                continue
        else:
            users_added.append(
                {
                    'username_normal': user.username_normal,
                    'nome': user.nome,
                    'grupocanal': user.grupocanal,
                    'cont_a_de_envio': user.conta_de_envio,
                    'log': user.log,
                }
            )
    try:
        rows.export_to_xlsx(users_added, file)
    except:
        traceback.print_exc()
        print('\nCould not write to the file provided!\n')
