import asyncio
import importlib
import datetime
import os
import operator
import json
from subprocess import Popen
import subprocess
import datetime

from discord.ext import commands
from discord import utils
from utils import Util, Configuration

class EventControl:
    def __init__(self, bot):
        self.bot:commands.Bot = bot

    @commands.command(hidden=True)
    async def start(self, ctx: commands.Context):
        """Starts the event!"""
        if os.path.exists(f'submissions/{ctx.guild.id}.json') is True:
            return await ctx.send("There is a event already running! Use the event end command before starting a new one.")

        heads = [187606096418963456, 298618155281154058, 169197827002466304, 263495765270200320, 117101067136794628, 164475721173958657, 191793155685744640]
        channel = ctx.bot.get_channel(int(Configuration.getConfigVar(ctx.guild.id, "SUBMISSION_CHANNEL")))
        everyone = None

        data = {}
        with open(f'submissions/{ctx.guild.id}.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

        if ctx.author.id not in heads:
            return

        for role in channel.guild.roles:
            if role.id == channel.guild.id:
                everyone = role
                await channel.set_permissions(everyone, read_messages=True, send_messages=False, add_reactions=False)
        await ctx.send("Event has started!")

    @commands.command(hidden=True)
    async def end(self, ctx:commands.Context):
        """Ends the event!"""
        if os.path.exists(f'submissions/{ctx.guild.id}.json') is False:
            return await ctx.send("There is currently no event running.")   

        heads = [187606096418963456, 298618155281154058, 169197827002466304, 263495765270200320, 117101067136794628, 164475721173958657, 191793155685744640]
        channel = ctx.bot.get_channel(int(Configuration.getConfigVar(ctx.guild.id, "SUBMISSION_CHANNEL")))
        everyone = None

        if ctx.author.id not in heads:
            return

        for role in channel.guild.roles:
            if role.id == channel.guild.id:
                everyone = role
                await channel.set_permissions(everyone, read_messages=False)
        await ctx.send("Event has ended! Results below.")
        
        message_votes = {}
        with open(f'submissions/{ctx.guild.id}.json', 'r') as infile:
            data = json.load(infile)
            print(data)
        for submitter in data:
            print(submitter)
            msg = await channel.get_message(int(submitter['MESSAGE_ID']))
            votecount = msg.reactions[0].count
            message_votes[str(submitter)] = votecount
        message_votes_sorted = sort(message_votes.items(), key=operator.itemgetter(1))

        first_points = list(message_votes_sorted.items())[0]
        first_author = await ctx.bot.get_user_info(int(list(message_votes_sorted)[0]))
        second_points = list(message_votes_sorted.items())[1]
        second_author = await ctx.bot.get_user_info(int(list(message_votes_sorted)[1]))
        third_points = list(message_votes_sorted.items())[2]
        third_author = await ctx.bot.get_user_info(int(list(message_votes_sorted)[2]))                                                
        e = discord.Embed(color=0x7289DA, timestamp=datetime.utcnow())
        e.add_field(name="1st Place", value=f'Submitted by {first_author.name} : {str(first_points)} Upvotes', inline=True)
        e.add_field(name="2nd Place", value=f'Submitted by {second_author.name} : {str(second_points)} Upvotes', inline=True)
        e.add_field(name="3rd Place", value=f'Submitted by {third_author.name} : {str(third_points)} Upvotes', inline=True)
        await ctx.send(embed=e)

        os.remove(f'submissions/{ctx.guild.id}.json')

def setup(bot):
    bot.add_cog(EventControl(bot))
