import discord
import os
import boto3

from dotenv import load_dotenv
load_dotenv()

ec2 = boto3.client('ec2')
client = discord.Client()

TOKEN = os.getenv('TOKEN')
SERVER_NAME = os.getenv('SERVER_NAME')


class ServerAlreadyRunning(Exception):
    '''Raised when Instance is already running'''
    pass


class ServerAlreadyStopped(Exception):
    '''Raised when Instance has already stopped'''
    pass


def describe_instance():
    instance = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': [
                    'Valheim Server'
                ]
            }
        ]
    )
    return {
        "state": instance['Reservations'][0]['Instances'][0]['State']['Name'],
        "id": instance['Reservations'][0]['Instances'][0]['InstanceId']
    }


def stop_instance():
    instance = describe_instance()
    if instance['state'] == 'stopped':
        raise ServerAlreadyStopped('Instance is already stopped.')
    else:
        return ec2.stop_instances(InstanceIds=[instance['id']])


def start_instance():
    instance = describe_instance()
    if instance['state'] == 'running':
        raise ServerAlreadyRunning('Instance is already running.')
    else:
        return ec2.start_instances(InstanceIds=[instance['id']])


def get_status():
    instance = describe_instance()
    return instance['state']


@ client.event
async def on_ready():
    print(print('We have logged in as {0.user}'.format(client)))


@ client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!server'):
        command = message.content.split(' ')
        if len(command) < 2:
            await message.channel.send("Available commands:\n\nstart - Starts the server.\nstop - Stops the server.\nstatus - Displays the current server status.")

        elif command[1] == "start":
            try:
                start_instance()
            except ServerAlreadyRunning:
                await message.channel.send("The server is already running!")
            else:
                await message.channel.send("Starting Valheim server...")

        elif command[1] == "stop":
            try:
                stop_instance()
            except ServerAlreadyStopped:
                await message.channel.send("The server is already stopped!")
            else:
                await message.channel.send("Stopping Valheim server...")
        elif command[1] == "status":
            await message.channel.send(F"The server is currently: {get_status()}")
        else:
            await message.channel.send("Unrecognized command.")

client.run(os.getenv('TOKEN'))
