# Imports our libraries to calculate current/future dates
import calendar
import datetime
import discord
import time
# Temp Libraries for some sort of Giphy API implementation
import json
import aiohttp
# Imports random so we can randomize responses
import random
# Imports our discord command library
from discord.ext import commands

# ------------------- Variables -------------------


# This references the client we created within our bot.py and passes it into the cog
class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client  # this allows us to access the client within our cog

    # ------------------- Commands -------------------
    @commands.command()
    async def dumb(self, ctx):
        await ctx.send("I am a dumb robot!")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.client.latency * 1000)}ms")

    # Commands that contain a list of responses
    @commands.command()
    async def roll(self, ctx):
        await ctx.send(random.randint(1, 6))

    @commands.command(aliases=["8ball"])
    async def _8ball(self, ctx, *, question):
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."]
        await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

    


    @commands.command(aliases=["user", "info"],passcontext=True)
    # @commands.has_permissions(kick_members=True)
    async def whois(self, ctx, member: discord.Member):
        channel = ctx.message.channel
        embed = discord.Embed(title=member.name, description=member.mention, color=discord.Colour.green())
        embed.add_field(name='ID', value=member.id, inline=True)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
        await ctx.send_message(channel,embed=embed)


# This function allows us to connect this cog to our bot
def setup(client):
    client.add_cog(Commands(client))