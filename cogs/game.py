import discord
import random
import db
from discord.ext import commands, tasks
from utils import sleeping

# Todo Adventure Function - List whether user is new or not, and if not list scores

items = ['knife', 'sword', 'shield', 'invisibility potion']
user_items = []

class Game(commands.Cog):
    def __init__(self, client):
        self.client = client  # this allows us to access the client within our cog
        db.createDatabase()
        self.conn = db.connectToDatabase()

    @commands.command()
    async def adventure(self, ctx):
        # Defining our embedded message
        embed = discord.Embed(title=f"Greetings {ctx.author.name}...", color=discord.Colour.dark_red())

        # If player doesn't exist, create them in db
        if not (db.doesPlayerExist(self.conn, str(ctx.author.id))):
            db.insertPlayer(self.conn, str(ctx.author.id), ctx.author.name)

        # Add the players current scores to embed
        hs, ls, cs = db.selectScore(self.conn, str(ctx.author.id))
        embed.add_field(name="Scores", value=f"High Score: {str(hs)}\nLifetime Score: {str(ls)}")

        # Ask if the player is ready to begin
        embed.add_field(name="Are you brave enough for this adventure?",
                        value=f"Yes? ✅ No? ❌\n\n"
                              f"__**Hint:**__ Select the reaction that corresponds to your answer")
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
        msg = await ctx.send(embed=embed)

        # Get response and react
        for emoji in ["✅", "❌"]:
            await msg.add_reaction(emoji)
        while True:
            cache_msg = await msg.channel.fetch_message(msg.id)
            for item in cache_msg.reactions:
                if str(item) == "❌" and item.count > 1:
                    embed = discord.Embed(title=f"What a shame {ctx.author.name}...",
                                          color=discord.Colour.dark_red())
                    embed.add_field(name="I had hopes for you... It appears you are not ready for this quest...",
                                    value="So long adventurer...", inline=True)
                    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
                    return await msg.edit(embed=embed)
                elif str(item) == "✅" and item.count > 1:
                    # zero out currentscore to prevent weirdness
                    db.updateScore(self.conn, str(ctx.author.id), 0)
                    return await self.Ball_Room(ctx, msg)

    @commands.command()  # Done for now
    async def Ball_Room(self, ctx, msg):
        emojis = ['⬆', '➡', '⬅', '⬇']
        cache_msg = await msg.channel.fetch_message(msg.id)
        await cache_msg.delete()

        embed = discord.Embed(title="The Ball Room",
                              color=discord.Colour.dark_purple())
        embed.add_field(name="You enter the Ball Room... What will you do?",
                        value="• Directly ahead of you there appears to be serving window, perhaps a kitchen?\n"
                              "• To your Right there appears to be a lack luster room...\n"
                              "• On the left you have a lovely entrance with an open door.\n"
                              "• Behind you a grand double door looms over you.\n\n"
                              "__**Hint:**__ Select the reaction that corresponds to your answer", inline=True)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
        msg = await ctx.send(embed=embed)

        for emoji in emojis:
            await msg.add_reaction(emoji)

        while True:
            cache_msg = await msg.channel.fetch_message(msg.id)
            for item in cache_msg.reactions:
                if str(item) == "⬆" and item.count > 1:
                    return await self.Kitchen(ctx, msg)
                elif str(item) == "➡" and item.count > 1:
                    return await self.Closet(ctx, msg)  # Done
                elif str(item) == "⬅" and item.count > 1:
                    return await self.Living_Room(ctx, msg)  # Working on this - Baron
                elif str(item) == "⬇" and item.count > 1:
                    return await self.Main_Hall(ctx, msg)  # Done

    @commands.command()
    async def Kitchen(self, ctx, msg):  # Done for now
        cache_msg = await msg.channel.fetch_message(msg.id)
        await cache_msg.delete()
        emojis = ['1️⃣', '2️⃣', '3️⃣']

        embed = discord.Embed(title=f"The Kitchen...",
                              color=discord.Colour.dark_red())
        embed.add_field(name="... Woah... It appears someone left this place in a hurry...",
                        value="Its an awful mess here...\n\n"
                              "Weird... This room doesn't appear to have an attached room... "
                              "Something is very off about this room, I can't quite put my finger on it.", inline=False)

        embed.add_field(name="I think I am going to investigate...",
                        value="1️⃣ The Odd Utensil Rack\n2️⃣ The Bent Faucet\n3️⃣ The 70's Era Painting", inline=False)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
        msg = await ctx.send(embed=embed)

        for emoji in emojis:
            await msg.add_reaction(emoji)

        while True:
            cache_msg = await msg.channel.fetch_message(msg.id)
            for item in cache_msg.reactions:
                if str(item) == "1️⃣" and item.count > 1:
                    embed = discord.Embed(title="Investigating the Kitchen...",
                                          color=discord.Colour.dark_red())
                    embed.add_field(name='The Odd Utensil Rack...',
                                    value="When looking up close, this doesn't appear to be all that odd... The Shape "
                                          "is still strange, but useless.\n\n"
                                          "This may have been a waste of time.. I am going to dwell on this room and "
                                          "return to the Ball Room for now...")
                    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
                    await msg.edit(embed=embed)
                    sleeping(8)
                    return await self.Ball_Room(ctx, msg)

                elif str(item) == '2️⃣' and item.count > 1:
                    cache_msg = await msg.channel.fetch_message(msg.id)
                    await cache_msg.delete()
                    emojis = ["✅", "❌"]
                    embed = discord.Embed(title="Investigating the Kitchen...",
                                          color=discord.Colour.dark_red())
                    embed.add_field(name='The Bent Faucet...',
                                    value="Looking up close it appears the faucet might have been bent from over "
                                          "usage... Or...\n\n", inline=False)
                    # You get some points!
                    db.updateScore(self.conn, str(ctx.author.id), 10)
                    embed.add_field(name="Crank!!",
                                    value="Look at that!! A hidden entrance has appeared!!\n"
                                          "Should we enter?\n\n"
                                          "Yes? ✅ No? ❌", inline=True)
                    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
                    msg = await ctx.send(embed=embed)

                    for emoji in emojis:
                        await msg.add_reaction(emoji)

                    while True:
                        cache_msg = await msg.channel.fetch_message(msg.id)
                        for item in cache_msg.reactions:
                            if str(item) == "❌" and item.count > 1:
                                embed = discord.Embed(title=f"Leaving the Kitchen...",
                                                      color=discord.Colour.dark_red())
                                embed.add_field(name="I don't think I want to disturb anything in this hidden room...",
                                                value="I think I will just go back to the Ball Room...", inline=True)
                                embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
                                await msg.edit(embed=embed)
                                sleeping(5)
                                return await self.Ball_Room(ctx, msg)

                            if str(item) == "✅" and item.count > 1:
                                return await self.Pantry(ctx, msg)

                elif str(item) == '3️⃣' and item.count > 1:
                    cache_msg = await msg.channel.fetch_message(msg.id)
                    await cache_msg.delete()
                    emojis = ["✅", "❌"]
                    embed = discord.Embed(title="Investigating the Kitchen...",
                                          color=discord.Colour.dark_red())
                    embed.add_field(name="The 70's Era Painting...",
                                    value="Whoever purchased this painting has quite the exquisite taste in art, "
                                          "the details are immaculate!\n\n"
                                          "Wait... This picture, the people in it... They are all looking towards the "
                                          "faucet I noticed earlier!\n\n"
                                          "Should we investigate?\n\n"
                                          "Yes? ✅ No? ❌", inline=False)
                    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
                    msg = await ctx.send(embed=embed)

                    for emoji in emojis:
                        await msg.add_reaction(emoji)

                    while True:
                        cache_msg = await msg.channel.fetch_message(msg.id)
                        for item in cache_msg.reactions:
                            if str(item) == "❌" and item.count > 1:
                                embed = discord.Embed(title=f"Leaving the Kitchen...",
                                                      color=discord.Colour.dark_red())
                                embed.add_field(name="I don't think I want to disturb anything in this hidden room...",
                                                value="I think I will just go back to the Ball Room...", inline=True)
                                embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
                                await msg.edit(embed=embed)
                                sleeping(5)
                                return await self.Ball_Room(ctx, msg)

                            if str(item) == "✅" and item.count > 1:
                                cache_msg = await msg.channel.fetch_message(msg.id)
                                await cache_msg.delete()
                                emojis = ["✅", "❌"]
                                embed = discord.Embed(title="Investigating the Kitchen...",
                                                      color=discord.Colour.dark_red())
                                embed.add_field(name='The Bent Faucet...',
                                                value="Looking up close it appears the faucet might have been bent "
                                                      "from over usage... Or...\n\n", inline=False)
                                db.updateScore(self.conn, str(ctx.author.id), 10)                    
                                embed.add_field(name="Crank!!",
                                                value="Look at that!! A hidden entrance has appeared!!\n"
                                                      "Should we enter?\n\n"
                                                      "Yes? ✅ No? ❌", inline=True)
                                embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
                                msg = await ctx.send(embed=embed)

                                for emoji in emojis:
                                    await msg.add_reaction(emoji)

                                while True:
                                    cache_msg = await msg.channel.fetch_message(msg.id)
                                    for item in cache_msg.reactions:
                                        if str(item) == "❌" and item.count > 1:
                                            embed = discord.Embed(title=f"Leaving the Kitchen...",
                                                                  color=discord.Colour.dark_red())
                                            embed.add_field(
                                                name="I don't think I want to disturb anything in this hidden room...",
                                                value="I think I will just go back to the Ball Room...", inline=True)
                                            embed.set_footer(icon_url=ctx.author.avatar_url,
                                                             text=f"Requested by {ctx.author.name}")
                                            await msg.edit(embed=embed)
                                            sleeping(5)
                                            return await self.Ball_Room(ctx, msg)

                                        if str(item) == "✅" and item.count > 1:
                                            return await self.Pantry(ctx, msg)

    @commands.command()
    async def Pantry(self, ctx, msg):
        cache_msg = await msg.channel.fetch_message(msg.id)
        await cache_msg.delete()

        emojis = ["✅", "❌"]
        embed = discord.Embed(title=f"The Pantry...",
                              color=discord.Colour.dark_red())
        embed.add_field(name="You enter this this abandoned room, filled to the brim with spiders... ",
                        value=f"You scream as one brushes against you... You make out what looks to be a cupboard at "
                              f"the far end of the room...\n\n"
                              f"Should we check it out?\n\n"
                              f"Yes? ✅ No? ❌", inline=True)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
        msg = await ctx.send(embed=embed)

        for emoji in emojis:
            await msg.add_reaction(emoji)

        while True:
            cache_msg = await msg.channel.fetch_message(msg.id)
            for item in cache_msg.reactions:
                if str(item) == "❌" and item.count > 1:
                    cache_msg = await msg.channel.fetch_message(msg.id)
                    await cache_msg.delete()

                    emojis = ["✅", "❌"]
                    embed = discord.Embed(title=f"The Pantry...",
                                          color=discord.Colour.dark_red())
                    embed.add_field(name="You decide you believe it would be best to leave...",
                                    value=f"You start to leave, but a strange feeling washes over you... A feeling of "
                                          f"regret... I got this far through the puzzle, "
                                          f"perhaps I should look at that cupboard\n\n"
                                          f"Should we check it out?\n\n"
                                          f"Yes? ✅ No? ❌", inline=True)
                    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
                    msg = await ctx.send(embed=embed)
                    for emoji in emojis:
                        await msg.add_reaction(emoji)

                    while True:
                        cache_msg = await msg.channel.fetch_message(msg.id)
                        for item in cache_msg.reactions:
                            if str(item) == "❌" and item.count > 1:
                                embed = discord.Embed(title=f"Leaving the Pantry...",
                                                      color=discord.Colour.dark_red())
                                embed.add_field(
                                    name="Despite the effort you went through...",
                                    value="You decide to leave, believing whatever is on the other end of the doors of "
                                          "the cupboard cannot be good...\n\n"
                                          "You deicde to return to the Ball Room...", inline=True)
                                embed.set_footer(icon_url=ctx.author.avatar_url,
                                                 text=f"Requested by {ctx.author.name}")
                                await msg.edit(embed=embed)
                                sleeping(5)
                                return await self.Ball_Room(ctx, msg)
                            if str(item) == "✅" and item.count > 1:
                                cache_msg = await msg.channel.fetch_message(msg.id)
                                await cache_msg.delete()

                                embed = discord.Embed(title=f"The Pantry's Cupboard...",
                                                      color=discord.Colour.dark_red())
                                db.updateScore(self.conn, str(ctx.author.id), 10)
                                embed.add_field(name="You walk steadily towards the cupboard...",
                                                value=f"You approach the old oak doors on the cupboard and violently "
                                                      f"swing the doors open... Revealing a hidden passage way!\n\n"
                                                      f"You decide to crawl through the new found opening...",
                                                inline=True)
                                embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
                                msg = await ctx.send(embed=embed)
                                sleeping(5)
                                return await self.Treasure_Room(ctx, msg)
                if str(item) == "✅" and item.count > 1:
                    cache_msg = await msg.channel.fetch_message(msg.id)
                    await cache_msg.delete()

                    embed = discord.Embed(title=f"The Pantry's Cupboard...",
                                          color=discord.Colour.dark_red())
                    db.updateScore(self.conn, str(ctx.author.id), 10)
                    embed.add_field(name="You walk steadily towards the cupboard...",
                                    value=f"You approach the old oak doors on the cupboard and violently "
                                          f"swing the doors open... Revealing a hidden passage way!\n\n"
                                          f"You decide to crawl through the new found opening...", inline=True)
                    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
                    msg = await ctx.send(embed=embed)
                    sleeping(5)
                    return await self.Treasure_Room(ctx, msg)
    
    @commands.command()
    async def Treasure_Room(self, ctx, msg):  # Done for now
        cache_msg = await msg.channel.fetch_message(msg.id)
        await cache_msg.delete()
        emojis = ["✅", "❌"]
        embed = discord.Embed(title=f"The Treasure Room...",
                              color=discord.Colour.dark_red())
        embed.add_field(name="As you make your way through the cupboard opening...",
                        value=f"You notice something glittering, you enter the room and it reveals a massive room, "
                              f"filled to the brim with all kinds of treasure and rewards!\n\n"
                              f"There is a grand chest in the center of the room with something "
                              f"carved into the wood...", inline=False)
        embed.add_field(name="The carving reads... ",
                        value="Should you solve my riddle, you will will a chance to gain treasure!\n\n"
                              "Are you interested?\n\n"
                              "Yes? ✅ No? ❌", inline=False)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
        msg = await ctx.send(embed=embed)

        for emoji in emojis:
            await msg.add_reaction(emoji)

        while True:
            cache_msg = await msg.channel.fetch_message(msg.id)
            for item in cache_msg.reactions:
                if str(item) == "❌" and item.count > 1:
                    embed = discord.Embed(title=f"Turning around...",
                                          color=discord.Colour.dark_red())
                    embed.add_field(name="You have decided to leave all the treasure and glory behind..",
                                    value="Depsite your great efforts, you return to the Ball Room...", inline=True)
                    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
                    await msg.edit(embed=embed)
                    sleeping(5)
                    return await self.Ball_Room(ctx, msg)
                if str(item) == "✅" and item.count > 1:
                    emojis = ['1️⃣', '2️⃣']
                    cache_msg = await msg.channel.fetch_message(msg.id)
                    await cache_msg.delete()

                    embed = discord.Embed(title=f"Enticed by the great riches described...",
                                          color=discord.Colour.dark_red())
                    embed.add_field(name="You eagerly accept the challenge!",
                                    value=f"The chest reads the following riddle...\n\n"
                                          f"Who... crafted King Arthurs grand round table?\n\n"
                                          f'1️⃣ Jeffery Bezos\n2️⃣ "Sir"-Cumference!', inline=True)
                    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
                    msg = await ctx.send(embed=embed)

                    for emoji in emojis:
                        await msg.add_reaction(emoji)

                    while True:
                        cache_msg = await msg.channel.fetch_message(msg.id)
                        for item in cache_msg.reactions:
                            if str(item) == "1️⃣" and item.count > 1:
                                embed = discord.Embed(title=f"Leaving the Treasure Room...",
                                                      color=discord.Colour.dark_red())
                                embed.add_field(
                                    name="Despite the great effort you went through...",
                                    value="You unfortunately failed the chests riddle...\n\n"
                                          "You return to the Ball Room empty handed...", inline=True)
                                embed.set_footer(icon_url=ctx.author.avatar_url,
                                                 text=f"Requested by {ctx.author.name}")
                                await msg.edit(embed=embed)
                                sleeping(5)
                                return await self.Ball_Room(ctx, msg)
                            elif str(item) == '2️⃣' and item.count > 1:
                                earned_item = random.choice(items)
                                user_items.append(earned_item)
                                embed = discord.Embed(
                                    title=f"You successfully solved the riddle to open the chest!",
                                    color=discord.Colour.dark_red())
                                db.updateScore(self.conn, str(ctx.author.id), 10)
                                embed.add_field(
                                    name="There appears to be an item here!",
                                    value=f"You earned {earned_item}", inline=False)

                                embed.add_field(name="Inventory",
                                                value=f"\n".join(user_items), inline=False)
                                db.updateScore(self.conn, str(ctx.author.id), 5)
                                embed.set_footer(icon_url=ctx.author.avatar_url,
                                                 text=f"Requested by {ctx.author.name}")
                                await msg.edit(embed=embed)
                                sleeping(8)
                                embed = discord.Embed(title=f"After retreiving your item...",
                                                      color=discord.Colour.dark_red())
                                embed.add_field(
                                    name="With loot in hand, you decide to return to the Ball Room",
                                    value="Leaving...", inline=True)
                                embed.set_footer(icon_url=ctx.author.avatar_url,
                                                 text=f"Requested by {ctx.author.name}")
                                await msg.edit(embed=embed)
                                sleeping(5)
                                return await self.Ball_Room(ctx, msg)

    @commands.command()
    async def Closet(self, ctx, msg):
        cache_msg = await msg.channel.fetch_message(msg.id)
        await cache_msg.delete()

        emojis = ["✅", "❌"]
        embed = discord.Embed(title=f"The Closet...",
                              color=discord.Colour.dark_red())
        embed.add_field(name="... You arrive at an eerie door, appears to be physically deteriorating.",
                        value=f"Will you enter?\n\n"
                              f"Yes? ✅ No? ❌\n\n", inline=True)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
        msg = await ctx.send(embed=embed)

        for emoji in emojis:
            await msg.add_reaction(emoji)

        while True:
            cache_msg = await msg.channel.fetch_message(msg.id)
            for item in cache_msg.reactions:
                if str(item) == "❌" and item.count > 1:
                    embed = discord.Embed(title=f"Turning around...",
                                          color=discord.Colour.dark_red())
                    embed.add_field(name="You have decided to turn back and return to the Ball Room...",
                                    value="Leaving...", inline=True)
                    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
                    await msg.edit(embed=embed)
                    sleeping(5)
                    return await self.Ball_Room(ctx, msg)
                if str(item) == "✅" and item.count > 1:
                    emojis = ["🔍", "❌"]
                    cache_msg = await msg.channel.fetch_message(msg.id)
                    await cache_msg.delete()
                    embed = discord.Embed(title=f"The Closet...",
                                          color=discord.Colour.dark_red())
                    embed.add_field(
                        name="The door creaks open... You enter the musty broom closet, as you're entering you run into a spider "
                             "web and are briefly startled...",
                        value="What will you do next?\n\n"
                              "Search? 🔍 Leave? ❌", inline=True)
                    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
                    msg = await ctx.send(embed=embed)

                    for emoji in emojis:
                        await msg.add_reaction(emoji)

                    while True:
                        cache_msg = await msg.channel.fetch_message(msg.id)
                        for item in cache_msg.reactions:
                            if str(item) == "❌" and item.count > 1:
                                embed = discord.Embed(title=f"Leaving the Broom Closet...",
                                                      color=discord.Colour.dark_red())
                                embed.add_field(name="You have decided to turn back and return to the Ball Room...",
                                                value="Leaving...", inline=True)
                                embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
                                await msg.edit(embed=embed)
                                sleeping(5)
                                return await self.Ball_Room(ctx, msg)

                            if str(item) == "🔍" and item.count > 1:
                                emojis = ["✅", "❌"]
                                cache_msg = await msg.channel.fetch_message(msg.id)
                                await cache_msg.delete()
                                embed = discord.Embed(title=f"The Closet...",
                                                      color=discord.Colour.dark_red())
                                embed.add_field(
                                    name="You are rummaging through what seems to be piles of janitor slacks and brooms... "
                                         "At the bottom of the pile there is a chest!",
                                    value="Will you open it?\n\n"
                                          "Yes? ✅ No? ❌\n\n", inline=True)
                                embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
                                msg = await ctx.send(embed=embed)

                                for emoji in emojis:
                                    await msg.add_reaction(emoji)

                                while True:
                                    cache_msg = await msg.channel.fetch_message(msg.id)
                                    for item in cache_msg.reactions:
                                        if str(item) == "❌" and item.count > 1:
                                            embed = discord.Embed(title=f"Leaving the Broom Closet...",
                                                                  color=discord.Colour.dark_red())
                                            embed.add_field(
                                                name="You have decided to turn back and return to the Ball Room...",
                                                value="Leaving...", inline=True)
                                            embed.set_footer(icon_url=ctx.author.avatar_url,
                                                             text=f"Requested by {ctx.author.name}")
                                            await msg.edit(embed=embed)
                                            sleeping(5)
                                            return await self.Ball_Room(ctx, msg)
                                        if str(item) == "✅" and item.count > 1:
                                            earned_item = random.choice(items)
                                            user_items.append(earned_item)
                                            embed = discord.Embed(title=f"You attempted to open the chest...",
                                                                  color=discord.Colour.dark_red())
                                            embed.add_field(
                                                name="There appears to be an item here!",
                                                value=f"You earned {earned_item}", inline=False)
                                            db.updateScore(self.conn, str(ctx.author.id), 5)
                                            embed.add_field(name="Inventory",
                                                            value=f"\n".join(user_items), inline=False)
                                            embed.set_footer(icon_url=ctx.author.avatar_url,
                                                             text=f"Requested by {ctx.author.name}")
                                            await msg.edit(embed=embed)
                                            sleeping(8)
                                            embed = discord.Embed(title=f"After retreiving your item...",
                                                                  color=discord.Colour.dark_red())
                                            embed.add_field(
                                                name="With loot in hand, you decide to return to the Ball Room",
                                                value="Leaving...", inline=True)
                                            embed.set_footer(icon_url=ctx.author.avatar_url,
                                                             text=f"Requested by {ctx.author.name}")
                                            await msg.edit(embed=embed)
                                            sleeping(5)
                                            return await self.Ball_Room(ctx, msg)

    @commands.command()
    async def Living_Room(self, ctx, msg):  # Working on this - Baron
        cache_msg = await msg.channel.fetch_message(msg.id)
        await cache_msg.delete()

        emojis = ["✅", "❌"]
        embed = discord.Embed(title=f"The Living Room...",
                              color=discord.Colour.dark_red())
        embed.add_field(name="... As your approach the dark and unknown room, you realize the door is wide open and "
                             "damaged... Do you go in?",
                        value=f"Will you enter?\n\n"
                              f"Yes? ✅ No? ❌\n\n", inline=True)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
        msg = await ctx.send(embed=embed)

        for emoji in emojis:
            await msg.add_reaction(emoji)

        while True:
            cache_msg = await msg.channel.fetch_message(msg.id)
            for item in cache_msg.reactions:
                if str(item) == "❌" and item.count > 1:
                    embed = discord.Embed(title=f"Turning around...",
                                          color=discord.Colour.dark_red())
                    embed.add_field(name="You have an intense feeling drawing you to the room... You ignore this "
                                         "feeling and turn back in order to return to the Ball Room...",
                                    value="Leaving...", inline=True)
                    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
                    await msg.edit(embed=embed)
                    sleeping(5)
                    return await self.Ball_Room(ctx, msg)
                if str(item) == "✅" and item.count > 1:
                    emojis = ["⚔", "🎒"]
                    cache_msg = await msg.channel.fetch_message(msg.id)
                    await cache_msg.delete()

                    embed = discord.Embed(title=f"The Living Room...",
                                          color=discord.Colour.dark_red())
                    embed.add_field(
                        name="You proceed into the room... As you enter deeper into the room, you're shocked to run "
                             "into... A... GOBLIN!",
                        value="What will you do next?\n\n"
                              "Fight? ⚔ Use an Item? 🎒", inline=True)
                    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
                    msg = await ctx.send(embed=embed)

                    for emoji in emojis:
                        await msg.add_reaction(emoji)

                    while True:
                        cache_msg = await msg.channel.fetch_message(msg.id)
                        for item in cache_msg.reactions:
                            if str(item) == "🎒" and item.count > 1:
                                if 'invisibility potion' in user_items:
                                    cache_msg = await msg.channel.fetch_message(msg.id)
                                    await cache_msg.delete()
                                    emojis = ["✅", "❌"]
                                    embed = discord.Embed(title=f"Do you want to use this?",
                                                          color=discord.Colour.dark_red())
                                    embed.add_field(
                                        name="You reach into your backpack and pull out the invisibility potion...",
                                        value=f"Will you use this item?\n\n"
                                              f"Yes? ✅ No? ❌\n\n", inline=True)
                                    embed.set_footer(icon_url=ctx.author.avatar_url,
                                                     text=f"Requested by {ctx.author.name}")
                                    msg = await ctx.send(embed=embed)

                                    for emoji in emojis:
                                        await msg.add_reaction(emoji)

                                    while True:
                                        cache_msg = await msg.channel.fetch_message(msg.id)
                                        for item in cache_msg.reactions:
                                            if str(item) == "✅" and item.count > 1:
                                                user_items.remove('invisibility potion')
                                                embed = discord.Embed(title=f"You use your potion!",
                                                                      color=discord.Colour.dark_red())
                                                embed.add_field(
                                                    name="As you empty the contents of the potion into your belly, "
                                                         "a gut wrenching pain overwhelms you... ",
                                                    value="You realize you can no longer see your hands! You quickly "
                                                          "run past the monster and proceed to the Cellar...",
                                                    inline=True)
                                                db.updateScore(self.conn, str(ctx.author.id), 10)
                                                embed.set_footer(icon_url=ctx.author.avatar_url,
                                                                 text=f"Requested by {ctx.author.name}")
                                                await msg.edit(embed=embed)
                                                sleeping(5)
                                                return await self.Cellar(ctx, msg)
                                            elif str(item) == "❌" and item.count > 1:
                                                return await self.Living_Room_Fight(ctx, msg)
                                else:
                                    embed = discord.Embed(title=f"You frantically check your pack...",
                                                          color=discord.Colour.dark_red())
                                    embed.add_field(
                                        name="You reach into your backpack and realize you have nothing to help you!",
                                        value=f"Looks like we have no choice but to fight...\n", inline=True)
                                    embed.set_footer(icon_url=ctx.author.avatar_url,
                                                     text=f"Requested by {ctx.author.name}")
                                    await msg.edit(embed=embed)
                                    sleeping(5)
                                    return await self.Living_Room_Fight(ctx, msg)
                            elif str(item) == "⚔" and item.count > 1:
                                return await self.Living_Room_Fight(ctx, msg)
                                # Epic fight ensues

    @commands.command()
    async def Living_Room_Fight(self, ctx, msg):
        cache_msg = await msg.channel.fetch_message(msg.id)
        await cache_msg.delete()

        # Describe the opening attack with a stupid pun
        embed = discord.Embed(title="The Den", color=discord.Colour.dark_red())
        embed.add_field(name="The Goblin 👺 charges you!", value="You realize your mistake now. This was no living room, it was a den! The Goblin lets out a shriek and lunges at you!")
        msg = await ctx.send(embed=embed)
        sleeping(5)

        # If the player has a shield, they block the attack. Otherwise they get hurt.
        if "shield" in user_items:
            embed.add_field(name="You raise your shield! 🛡", value="You bring it between you and the Goblin just in the nick of time. He collides with the shield, his nasty claws leaving ragged scrapes across the dome of the shield. You stumble back from the force of the collision but maintain your 🦶🦶 footing.", inline=False)
        else:
            embed.add_field(name="The Goblin hits!", value="Caught off guard, you put your arm out in front of you and the Goblin rakes your forearm 🩸 with his claws. You feel a searing pain shoot up your arm 💔 and you stumble backwards as he collides with you.", inline=False)
            db.updateScore(self.conn, str(ctx.author.id), -10)
        await msg.edit(embed=embed)
        sleeping(5)

        # Counterattack and exit
        if "sword" in user_items:
          embed.add_field(name="You draw your sword! 🤺", value="The Goblin tries to take advantage of the momentum and continues his onslaught. As he rushes in focused on your throat, you raise your sword in front of you and he skewers himself on it. The shrieking suddenly stops 🩸🩸🩸 and the goblin falls backwards off your sword onto the floor. 💀", inline=False)
        elif "knife" in user_items:
          embed.add_field(name="You draw your knife! 🗡", value="The Goblin hesitates for a moment as you brandish the blade 🗡, but overcomes his fear and draws a sharpened rock 🔪 from a pouch at his hip. He unexpectedly hurls it at you, narrowly missing your head! Now weaponless, the creature turns to run. You take adavantage of the situation and rush up behind him dispatching him in an instant. 💀", inline=False)
        else:
          embed.add_field(name="You put up your fists!", value="The Goblin laughs at you and steps closer with a sneer. You surprise the monstrous fellow with a swift double jab 🤜🤜 followed with a wicked uppercut ✊ that lifts him several inches off the floor. He lands on his feet though his knees nearly buckle. You give him no quarter and with a vicious kick 🦵 send him sprawling. 💀", inline=False)
        db.updateScore(self.conn, str(ctx.author.id), 15)
        await msg.edit(embed=embed)
        sleeping(5)
        embed.add_field(name="You take a moment to catch your breath and recover.", value="The goblin lies still on the floor of the living room. You look around briefly but there doesn't seem to be anything intersting here besides a staircase leading down. After catching your breath, you descend the stairs.", inline=False)
        await msg.edit(embed=embed)
        sleeping(15)
        return await self.Cellar(ctx, msg)

    @commands.command()
    async def Cellar(self, ctx, msg):
        cache_msg = await msg.channel.fetch_message(msg.id)
        await cache_msg.delete()
        emojis = ["✅", "❌"]
        embed = discord.Embed(title=f"The Cellar...",
                              color=discord.Colour.dark_red())
        embed.add_field(name="You now find yourself in the Cellar...",
                        value=f"You look around and see kegs full of mysterious liquid in the far end of the room. "
                              f"After taking a moment to think about you, you think it would be best to leave them "
                              f"alone. You think there might be something useful in this room...\n\n"
                              f"Should we take a look around?\n\n"
                              f"Yes? ✅ No? ❌", inline=True)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
        msg = await ctx.send(embed=embed)

        for emoji in emojis:
            await msg.add_reaction(emoji)

        while True:
            cache_msg = await msg.channel.fetch_message(msg.id)
            for item in cache_msg.reactions:
                if str(item) == "❌" and item.count > 1:
                    cache_msg = await msg.channel.fetch_message(msg.id)
                    await cache_msg.delete()

                    emojis = ["✅", "❌"]
                    embed = discord.Embed(title=f"The Cellar...",
                                          color=discord.Colour.dark_red())
                    embed.add_field(name="You decide you believe it would be best to leave...",
                                    value=f"You start to leave, but a strange feeling washes over you... Something is "
                                          f"is pulling you to this room..."
                                          f"Maybe I should take a look around?\n\n"
                                          f"Yes? ✅ No? ❌", inline=True)
                    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
                    msg = await ctx.send(embed=embed)
                    for emoji in emojis:
                        await msg.add_reaction(emoji)

                    while True:
                        cache_msg = await msg.channel.fetch_message(msg.id)
                        for item in cache_msg.reactions:
                            if str(item) == "❌" and item.count > 1:
                                embed = discord.Embed(title=f"Leaving the Cellar...",
                                                      color=discord.Colour.dark_red())
                                embed.add_field(
                                    name="You decide it would be best to leave for now...",
                                    value="You decide to return to the Living Room...", inline=True)
                                embed.set_footer(icon_url=ctx.author.avatar_url,
                                                 text=f"Requested by {ctx.author.name}")
                                await msg.edit(embed=embed)
                                sleeping(5)
                                return await self.Living_Room(ctx, msg)
                            if str(item) == "✅" and item.count > 1:
                                user_items.append("key")
                                cache_msg = await msg.channel.fetch_message(msg.id)
                                await cache_msg.delete()

                                embed = discord.Embed(title=f"The Bowels of the Cellar...",
                                                      color=discord.Colour.dark_red())
                                embed.add_field(name="You cautiously look through out the room...",
                                                value=f"Despite there being piles of filth everywhere your eyes can "
                                                      f"see, you decide there may be something worthwhile in the "
                                                      f"filth.\n\nYou begin thrashing the piles of unknown materials "
                                                      f"ar`ound, expertly compiling all the lesser piles into one "
                                                      f"massive pile of grotesque filth...\n\n"
                                                      f"At last... The final pile... You think to yourself whether "
                                                      f"its worth trying one final pile, you decide there is nothing "
                                                      f"to lose.\n\n"
                                                      f"EUREKA! You find a key! You are unsure what the key is to "
                                                      f"but decide to hang on to it for now and return to the "
                                                      f"Living Room...",
                                                inline=True)
                                db.updateScore(self.conn, str(ctx.author.id), 5)
                                embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
                                msg = await ctx.send(embed=embed)
                                sleeping(10)
                                return await self.Ball_Room(ctx, msg)
                elif str(item) == "✅" and item.count > 1:
                    user_items.append("key")
                    cache_msg = await msg.channel.fetch_message(msg.id)
                    await cache_msg.delete()

                    embed = discord.Embed(title=f"The Bowels of the Cellar...",
                                          color=discord.Colour.dark_red())
                    embed.add_field(name="You cautiously look through out the room...",
                                    value=f"Despite there being piles of filth everywhere your eyes can "
                                          f"see, you decide there may be something worthwhile in the "
                                          f"filth.\n\nYou begin thrashing the piles of unknown materials "
                                          f"around, expertly compiling all the lesser piles into one "
                                          f"massive pile of grotesque filth...\n\n"
                                          f"At last... The final pile... You think to yourself whether "
                                          f"its worth trying one final pile, you decide there is nothing "
                                          f"to lose.\n\n"
                                          f"EUREKA! You find a key! You are unsure what the key is to "
                                          f"but decide to hang on to it for now and return to the "
                                          f"Living Room...",
                                    inline=True)
                    db.updateScore(self.conn, str(ctx.author.id), 5)
                    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
                    msg = await ctx.send(embed=embed)
                    sleeping(10)
                    return await self.Ball_Room(ctx, msg)

    #@commands.command()
    #async def Cellar_Storage(self, ctx, msg):
    #    cache_msg = await msg.channel.fetch_message(msg.id)
    #    await cache_msg.delete()

    #    await ctx.send("idk, something Cellar Storage Related soo n")

    @commands.command()
    async def Main_Hall(self, ctx, msg):
        cache_msg = await msg.channel.fetch_message(msg.id)
        await cache_msg.delete()

        # Describe room and prompt player
        embed = discord.Embed(title="The Main Hall", color=discord.Colour.dark_red())
        embed.add_field(name="You enter the Main Hall",
                        value="You see here a long, dimly lit hallway. A thick red rug covered in dust leads down the length of the room. There are several suits of armor along both walls down the hall. As you moved inside, clouds of dust kick up from the rug with each step. You think you can just make out the outline of a door at the far end of the hallway... ")
        embed.add_field(name="What do you do?", value="Approach the door? 🚪\nLeave? ️💨")
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🚪")
        await msg.add_reaction("💨")

        # Determine the players chosen action
        action = None
        while not action:
            cache_msg = await msg.channel.fetch_message(msg.id)
            for item in cache_msg.reactions:
                if str(item) == "🚪" and item.count > 1:
                    action = "approach"
                if str(item) == "💨" and item.count > 1:
                    embed.add_field(name="On second thought...", value="You turn and head back the way you came.",
                                    inline=False)
                    await cache_msg.edit(embed=embed)
                    sleeping(5)
                    return await self.Ball_Room(ctx, msg)

        # Describe what happens as they approach the door and prompt player
        embed.add_field(name="You decide to approach the door.",
                        value="As you pace down the hallway, the suits of armor on either side loom over you. Suddenly, the two figures closest to the door stand at attention and turn towards you! They draw their weapons and begin to advance...",
                        inline=False)
        embed.add_field(name="You size up your foes.",
                        value="They look tough but if you had a weapon you might be able to do some damage. On the other hand, that armor makes them ungainly and slow. Maybe you could dart past them?")
        embed.add_field(name="What do you do?", value="Fight? ⚔\nRun past? 💨")
        await cache_msg.edit(embed=embed)
        await msg.add_reaction("⚔")

        # Get players next reaction
        action = None
        while not action:
            cache_msg = await msg.channel.fetch_message(msg.id)
            for item in cache_msg.reactions:
                if str(item) == "💨" and item.count > 1:
                    embed.add_field(name="You try to duck past them.",
                                    value="They move with surprising speed and swing their weapons at you! You turn, sprinting for the door your entered through as they give chase. You rush through the door slamming it shut behind you. Phew, that was close.",
                                    inline=False)
                    db.updateScore(self.conn, str(ctx.author.id), -5)
                    await cache_msg.edit(embed=embed)
                    sleeping(5)
                    return await self.Ball_Room(ctx, msg)
                if str(item) == "⚔" and item.count > 1:
                    action = "fight"

        # Describe the fight. Varies depending on equipment. Go through the next door after.ght
        if "sword" in user_items:
            embed.add_field(name="You wield your sword.",
                            value="You swing, catching them off guard and quickly dispatching one. The other steps back, wary now and is ready when you charge in. He thrusts but you parry the clumsy attack and deal a deadly slash.",
                            inline=False)
        elif "knife" in user_items:
            embed.add_field(name="You wield your knife.",
                            value="You deftly avoid the animated armor's fell blows and one at a time jam the knife into a gap in their armor, dropping them to the ground.",
                            inline=False)
        else:
            embed.add_field(name="You put up your fists",
                            value="The enemies land several ghastly blows on you but over the course of the brawl you manage to dismantle them, piece by piece.",
                            inline=False)
        embed.add_field(name="You are victorious!",
                        value="The enemies have been vanquished, lying on the ground before you. You glance over your shoulder but none of the other suits of armor have moved. You appear to be safe for now. You proceed through the door.",
                        inline=False)
        db.updateScore(self.conn, str(ctx.author.id), 30)
        await cache_msg.edit(embed=embed)
        sleeping(10)
        return await self.Entry_Room(ctx, msg)

    @commands.command()
    async def Entry_Room(self, ctx, msg):
        emojis = ["⚔", "🎒"]
        statements = ["Its now or never!", "I can do it!", "Just keep swimming...", "Ouch..",
                      "I need to end this quick"]
        boss = True
        player = True
        boss_hp = 200
        boss_dmg = 8
        player_hp = 150
        player_dmg = 10

        if "knife" in user_items:
            player_dmg += 5
            user_items.remove("knife")
        elif "sword" in user_items:
            player_dmg += 10
            user_items.remove("sword")
        elif "shield" in user_items:
            boss_dmg -= 3
            user_items.remove("shield")

        cache_msg = await msg.channel.fetch_message(msg.id)
        await cache_msg.delete()
        embed = discord.Embed(title=f"Entry Way...",
                              color=discord.Colour.dark_red())
        embed.add_field(
            name="As you make your way through the grand entry way of this building, you are suddenly startled by "
                 "a loud crash!",
            value="You frantically look around to see what could have caused such a commotion... Suddenly you "
                  "hear annother crash, an another... Then another... \n\n"
                  "You see a beast unlike any you've ever seen emerges from underneath the grand staircase... "
                  "Directly blocking your path!\n\n"
                  "You have no choice but to fight the beast...", inline=True)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
        msg = await ctx.send(embed=embed)

        sleeping(8)

        cache_msg = await msg.channel.fetch_message(msg.id)
        await cache_msg.delete()
        embed = discord.Embed(title=f"⚔ Boss Battle ⚔",
                              color=discord.Colour.dark_red())
        embed.add_field(name=f"A wild Foozgorg appears!!!\n\n"
                             f"HP: {boss_hp}",
                        value=f"{random.choice(statements)}\n\n", inline=False)
        embed.add_field(name='Player Stats',
                        value=f'HP: {player_hp}\n\n'
                              f'Fight? ⚔ Use an Item? 🎒', inline=False)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
        msg = await ctx.send(embed=embed)
        sleeping(5)

        while boss and player:
            if boss_hp > 0:
                for emoji in emojis:
                    await msg.add_reaction(emoji)
                cache_msg = await msg.channel.fetch_message(msg.id)
                for item in cache_msg.reactions:
                    if str(item) == "🎒" and item.count > 1:
                        if "invisibility potion" in user_items:
                            user_items.remove("invisibility potion")
                            p_dmg = player_dmg + int(random.randint(0, 10))
                            boss_hp -= p_dmg
                            if boss_hp < 0:
                                boss_hp = 0
                                boss = False
                                break
                            embed = discord.Embed(title=f"⚔ Boss Battle ⚔",
                                                  color=discord.Colour.dark_red())
                            embed.add_field(name=f"Foozgorg HP: {boss_hp}",
                                            value=f"You dealt {p_dmg} this turn!\n\n", inline=False)
                            embed.add_field(name='Player Stats',
                                            value=f'HP: {player_hp}\n\n'
                                                  f'You used your invisibility potion and avoided damage!',
                                            inline=False)
                        else:
                            p_dmg = player_dmg - int(random.randint(5, 15))
                            if p_dmg < 0:
                                p_dmg = 0
                            boss_hp -= p_dmg
                            if boss_hp < 0:
                                boss_hp = 0
                                boss = False
                                break
                            b_dmg = boss_dmg + int(random.randint(5, 15))
                            player_hp -= b_dmg
                            if player_hp < 0:
                                player_hp = 0
                                player = False
                                break
                            embed = discord.Embed(title=f"⚔ Boss Battle ⚔",
                                                  color=discord.Colour.dark_red())
                            embed.add_field(name=f"Foozgorg HP: {boss_hp}",
                                            value=f"You failed to find anything useful in your bag... "
                                                  f"You attack instead!\n\n"
                                                  f"Because of your fumbling uou dealt {p_dmg} to the boss!\n\n", inline=False)
                            embed.add_field(name='Player Stats',
                                            value=f'HP: {player_hp}\n\n'
                                                  f'You were distracted and took {b_dmg} damage this turn!',
                                            inline=False)
                        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
                        await msg.edit(embed=embed)
                        sleeping(2)

                        cache_msg = await msg.channel.fetch_message(msg.id)
                        await cache_msg.delete()

                        embed = discord.Embed(title=f"⚔ Boss Battle ⚔",
                                              color=discord.Colour.dark_red())
                        embed.add_field(name=f"Foozgorg HP: {boss_hp}",
                                        value=f"{random.choice(statements)}\n\n", inline=False)
                        embed.add_field(name='Player Stats',
                                        value=f'HP: {player_hp}\n\n'
                                              f'Fight? ⚔ Use an Item? 🎒', inline=False)
                        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
                        msg = await ctx.send(embed=embed)
                        sleeping(2)

                    if str(item) == '⚔' and item.count > 1:

                        p_dmg = player_dmg + int(random.randint(0, 10))
                        boss_hp -= p_dmg
                        if boss_hp < 0:
                            boss_hp = 0
                            boss = False
                            break
                        b_dmg = boss_dmg + int(random.randint(0, 10))
                        player_hp -= b_dmg
                        if player_hp < 0:
                            player_hp = 0
                            player = False
                            break

                        embed = discord.Embed(title=f"⚔ Boss Battle ⚔",
                                              color=discord.Colour.dark_red())
                        embed.add_field(name=f"Foozgorg HP: {boss_hp}",
                                        value=f"You dealt {p_dmg} to the boss!\n\n", inline=False)
                        embed.add_field(name='Player Stats',
                                        value=f'HP: {player_hp}\n\n'
                                              f'You took {b_dmg} damage this turn!',
                                        inline=False)
                        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
                        await msg.edit(embed=embed)
                        sleeping(2)

                        cache_msg = await msg.channel.fetch_message(msg.id)
                        await cache_msg.delete()

                        embed = discord.Embed(title=f"⚔ Boss Battle ⚔",
                                              color=discord.Colour.dark_red())
                        embed.add_field(name=f"Foozgorg HP: {boss_hp}",
                                        value=f"{random.choice(statements)}\n\n", inline=False)
                        embed.add_field(name='Player Stats',
                                        value=f'HP: {player_hp}\n\n'
                                              f'Fight? ⚔ Use an Item? 🎒', inline=False)
                        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
                        msg = await ctx.send(embed=embed)
            elif boss == 0:
                boss = False
            elif player == 0:
                player = False

        if not player:
            await cache_msg.delete()
            embed = discord.Embed(title=f"And so ends the tale of the glorious {ctx.author.name}",
                                  color=discord.Colour.dark_red())
            embed.add_field(name='Player Stats',
                            value=f'Score: SCORE_INT', inline=False)  # Todo put player score
            embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
            return await ctx.send(embed=embed)
        elif not boss:
            await cache_msg.delete()
            embed = discord.Embed(title=f"And so the beast falls!",
                                  color=discord.Colour.dark_red())
            embed.add_field(name='After a mighty battle you emerged victorious!',
                            value='After taking a short break you decide to quickly head into the next '
                                 'room...', inline=False)
            embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
            msg = await ctx.send(embed=embed)
            sleeping(5)
            return await self.Exit(ctx, msg)
                    

    @commands.command()
    async def Exit(self, ctx, msg):
        cache_msg = await msg.channel.fetch_message(msg.id)
        await cache_msg.delete()

        # Describe the room and prompt for action
        embed = discord.Embed(title="The Foyer", color=discord.Colour.dark_red())
        embed.add_field(name="You enter the Foyer.", value="You can hardly believe you've made it here! The front door is within your reach, its magnificently carved wood lightly gleaming in the soft light filtering through the windows. The air smells a bit musty, but you can catch a whiff of fresh outdoor air! Notably, there is a large gap in the floorboards here. Better be careful...", inline=False)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
        msg = await ctx.send(embed=embed)
        sleeping(5)

        # If the player doesn't have the key, prompt for action then dump 'em into the cellar :)
        if "key" not in user_items:
            cache_msg = await msg.channel.fetch_message(msg.id)
            embed.add_field(name="You step toward the door.", value="As you draw closer, your eye is drawn to a massive keyhole in the center of the door. A small message is carved in a circle around it.\n*never try to ope without the key! thou hast been warned!*")
            embed.add_field(name="What would you like to do?", value="Open the door? 🚪\nTurn back? 🔙")
            await msg.edit(embed=embed)
            await msg.add_reaction("🚪")
            await msg.add_reaction("🔙")

            action = None
            while not action:
                cache_msg = await msg.channel.fetch_message(msg.id)
                for item in cache_msg.reactions:
                    if str(item) == "🚪" and item.count > 1:
                        action = "open"
                    if str(item) == "🔙" and item.count > 1:
                          action = "turn"
            if action == "open":
                embed.add_field(name="You try to push the door open.", value="You try to shove the door open with all your might. As soon as you put force on the door though, you realize to your dismay that the rug under your feet concealed a trap door!", inline=False)
            if action == "turn":
                embed.add_field(name="You turn away from the door.", value="You turn from the door, deciding to heed the warning. As you walk back the way you came from, you stumble on an uneven floor board and find yourself falling through the hole in the floor!", inline=False)
            db.updateScore(self.conn, str(ctx.author.id), -15)
            await cache_msg.edit(embed=embed)
            sleeping(5)
            
            embed.add_field(name="You are falling!", value="You plunge down into inky darkness and land with a thud on a cold stone floor. You are dazed and it takes several seconds for you to collect yourself.", inline=False)
            await cache_msg.edit(embed=embed)
            sleeping(10)
            return await self.Cellar(ctx, msg)
        
        # You have escaped and won the game!
        await msg.delete()
        embed = discord.Embed(title="You won!", color=discord.Colour.dark_blue())
        embed.add_field(name="You insert the key into the lock.", value="The door effortlessly swings open and you step out into the fresh air. You take a moment to feel the warmth of the sun on your skin and are grateful to have made your escape from that place.")
        hs, ls, cs = db.selectScore(self.conn, str(ctx.author.id))
        embed.add_field(name='Player Stats',
                            value=f'Score: {cs}\nPrevious High Score: {hs}\nPrevious Lifetime Score: {ls}', inline=False)

        await ctx.send(embed=embed)

        db.finishGame(self.conn, str(ctx.author.id))

# Used to connect this cog to the bot
def setup(client):
    client.add_cog(Game(client))
