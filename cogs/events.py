import discord
import random
from discord.ext import commands, tasks

# ------------------- Variables -------------------
# Variables for the bot status


# This references the client we created within our bot.py and passes it into the cog
class Events(commands.Cog):
    def __init__(self, client):
        self.client = client  # this allows us to access the client within our cog

    # ------------------- Events and Tasks -------------------
    # Loads bot, and lets us know when its ready
    @commands.Cog.listener()
    async def on_ready(self):
        print("Logged in as " + self.client.user.name)
        print(self.client.user.id)
        print("-------")


    # When a known command fails, throws error
    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     await ctx.send(ctx.command.name + " didn't work! Give it another try.")
    #     print(error)

    # Event for monitoring command usage
    @commands.Cog.listener()
    async def on_command(self, ctx):
        print(ctx.command.name + " was invoked.")

    # Event for monitoring successful command usage
    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        print(ctx.command.name + " was invoked sucessfully.")
    
    # @commands.Cog.listener()
    # async def on_reaction_add(self,reaction,user):
    #   channel = reaction.message.channel
    #   await channel.send('{} has added {} to the message: {} '.format(user.name,reaction.emoji,reaction.message.content)) 

    # @commands.Cog.listener()  # Not sure this is needed right now. 
    # async def on_reaction_remove(self,reaction,user):
    #   channel = reaction.message.channel
    #   await channel.send('{} has removed {} from the message: {} '.format(user.name,user.emoji,reaction.message.content)) 


# This function allows us to connect this cog to our bot
def setup(client):
    client.add_cog(Events(client))
