# Discord EC2 Bot

Small script I made in order to allow users on my Discord server to start/stop my [Valheim server](https://github.com/codeeno/valheim-terraform) in order to reduce costs.

## Usage

The bot, once running, can be interacted with via the `!server` command. Possible commands:

* start - Starts the EC2 instance
* stop - Stops the EC2 instance
* status - Prints whether or not the instance is currently `running` or `stopped`.

## Setup

Install the dependencies:

```bash
$ pip3 install -r requirements.txt
```


Copy `.env` file:

```bash
$ mv .env.sample .env
```

Adjust the values in the `.env` file. 
* The `TOKEN` value is the access token of your Discord bot.
* The `SERVER_NAME` value needs to correspond this the value of the `Name` tag of the EC2-Instance that is to be started/stopped.
* The `AWS` values are your usual AWS credentials and region.

Run the script:

```bash
$ python3 main.py
```
