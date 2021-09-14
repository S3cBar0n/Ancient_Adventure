# Library for OS file control
import os
# Imports file that contains our bots token
from discord.ext import commands
#import db
from threading import Thread

# Todo Treasure Chest generates random item, stored for the user in db. Durability? Item Rarity? 
# Todo Randomly generated enemies, percentage chance of encounters, random chance to get an item
# Todo Map procedurely generated??? If we have time
# Todo Create DB > Linux server in Linode. - NoUsernames working on this
# Todo come up with sick domain name for hosting the db
# Todo Text adventure - Everyone as time permits
# Todo Items will be persistent for user trading and crafting


# def main():
#     try:
#         # Connect to the database
#         conn = db.connectToDatabase()
#     #    db.updatePlayer(conn, "test123", 70, 421)
#     #    name, hs, ls = db.selectPlayer(conn, "test123")
#     #    print(name + " has a highscore of " + str(hs) + " and a lifetime score of " + str(ls))

#     except Exception as e:
#         print(e)
#         print("Skipping DB, starting bot.")


def bot():
    # Prefix for my commands
    client = commands.Bot(command_prefix="@", help_command=None)


    # Loads our cogs library
    @client.command()
    @commands.has_permissions(administrator=True)
    async def load(ctx, extension):
        client.load_extension(f"cogs.{extension}")


    # Unloads our cogs library
    @client.command()
    @commands.has_permissions(administrator=True)
    async def unload(ctx, extension):
        client.unload_extension(f"cogs.{extension}")

    @client.command()
    @commands.has_permissions(administrator=True)
    async def reload(ctx, extension):
        client.unload_extension(f"cogs.{extension}")
        client.load_extension(f"cogs.{extension}")


    # Searches for .py files within the cogs directory on the OS and removes .py so it can be loaded
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")

    # Read in the bot token from the file secret.txt and then run it
    with open('secret.txt', 'r') as file:
        bot_token = file.read()
    client.run(bot_token)

if __name__ == '__main__':
    # Thread(target=main()).start()
    # Thread(target=bot()).start()
    bot()

