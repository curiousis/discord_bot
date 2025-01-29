import sys
import random

# To use this package, install: pip3 install discord.py

import discord

# This is mainly taken from https://discordpy.readthedocs.io/en/stable/quickstart.html
# To make the file watch for changes (the script is restarted each time you save the file),
# npm package nodemon can be used:
# 1: Install npm if you do not have it yet:
#    sudo apt update
#    sudo apt install npm
# 2. To install nodemon: sudo npm i -g nodemon
# 3: To run the file: nodemon --exec python3 bottemplate.py

discordToken = ""  # Your bot token here (https://discord.com/developers/applications/ and tab Bot -> Token -> Reset Token -> Copy the token here)
name = "csm101_israel_biringanine"  # Your bot name here


if discordToken == "":
    sys.exit("ERROR: Please set the discord token.")
if name == "":
    sys.exit("ERROR: Please set the name of the bot.")


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    """'gives feedback when bot is ready"""
    print(f"We have logged in as {client.user}")


my_dictionary = {}
todos = {}


def add_to_dictionary(dictionary, term, value):
    """
    gets dictionary, term and value.
    Then adds the value to the dictionary.
    """
    dictionary[term] = value


def remove_from_dictionary(dictionary, term):
    """
    Gets dictionay and term, then deletes the value
    """
    if term in dictionary:
        del dictionary[term]
    else:
        return "I do not know that"


def get_from_dictionary(dictionary, term):
    """gets a term and then gives the value

        Args:
            dictionary (_type_): dict
            term (_type_): string

        Returns:
    string"""

    if term in dictionary:
        return dictionary[term]
    else:
        return "I do not know this"


def add_todo(dictionary, item_key, item_value):
    if len(dictionary) < 5:
        if item_value in dictionary.values():
            return "item aready exists in the dictionary"
        else:
            dictionary[item_key] = item_value
            return dictionary
    else:
        return "Too many items!"


@client.event
async def on_message(message):
    global my_dictionary
    global todos
    if message.author == client.user:
        return  # We don't want to reply to ourselves

    # RULE: To not flood the channel with responses from multiple bots,
    # we only respond to messages that start with our name

    if message.content.startswith(name):
        print(f"{message.author} says: {message.content}")
        msg = message.content[len(name) :].strip()
        list_message = msg.split(" ")
        # 1.1: random
        if list_message[0] == "random":

            if len(list_message) < 3:
                await message.channel.send("Exterminate! Too few parameters.")
            elif len(list_message) > 4:
                await message.channel.send("Exterminate! Too many parameters.")
            if len(list_message) == 3:
                try:
                    first = int(list_message[1])
                    last = int(list_message[2])

                    if first > last:
                        await message.channel.send(
                            "Exterminate! The first number should be lower than the last number."
                        )
                    else:
                        random_number = random.randint(first, last)
                        await message.channel.send(f"Random number: {random_number}")
                except ValueError:
                    await message.channel.send("Exterminate! Only digits allowed.")
            elif len(list_message) == 4:
                try:
                    first = int(list_message[1])
                    second = int(list_message[2])
                    third = int(list_message[3])
                    if first > second:
                        await message.channel.send(
                            "Exterminate! The first number should be lower than the second number."
                        )
                    else:
                        random_numbers = [
                            random.randint(first, second) for _ in range(third)
                        ]
                        await message.channel.send(f"Random numbers: {random_numbers}")
                except ValueError:
                    await message.channel.send("Exterminate! Only digits allowed.")
        if list_message[0] == "set":
            if len(list_message) == 2:
                await message.channel.send(
                    remove_from_dictionary(my_dictionary, list_message[1])
                )
            elif len(list_message) == 3:
                add_to_dictionary(my_dictionary, list_message[1], list_message[2])

            else:
                await message.channel.send("Too little/many parameters")

        if list_message[0] == "get":
            if len(list_message) < 2:
                await message.channel.send("Exterminate! Too few parameters")
            elif len(list_message) > 2:
                await message.channel.send("Exterminate! Too many parameters")
            else:
                await message.channel.send(
                    get_from_dictionary(my_dictionary, list_message[1])
                )

        if list_message[0] == "sum":
            if len(list_message) < 3:
                await message.channel.send("Exterminate! Too few parameters.")
            elif len(list_message) > 3:
                await message.channel.send("Exterminate! Too many parameters.")
            elif len(list_message) == 3:
                try:
                    first = int(list_message[1])
                    second = int(list_message[2])
                    total = first + second
                    await message.channel.send(f"The Sum is: {total}")
                except ValueError:
                    await message.channel.send("Exterminate! Only digits allowed.")

        if list_message[0] == "todo":
            if len(list_message) == 1:
                if len(todos) == 0:
                    await message.channel.send("the todo list is empty")
                else:
                    for key, value in todos.items():
                        await message.channel.send(f"{key}: {value}")

            elif len(list_message) > 1:
                length = len(todos) + 1
                response = add_todo(todos, length, " ".join(list_message[1:]))
                await message.channel.send(response)
        if list_message[0] == "help":
            commands = [
                "here are the commands:",
                "random <first> <last> - generates a random number between the first and last number",
                "random <first> <second> <third> - generates a list of random numbers between the first and second number based on the side of the third number",
                "sum <first> <second> - sums the first and second number",
            ]

            [await message.channel.send(f"{command} ") for command in commands]

        if message.content.startswith(f"{name} hello"):

            await message.channel.send("Hello! Am I lost?")


client.run(discordToken)
