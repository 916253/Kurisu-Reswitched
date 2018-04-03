import datetime
import discord
import os
import random
import re
import string
from discord.ext import commands
from sys import argv

class Extras:
    """
    Extra things.
    """
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    prune_key = "nokey"

    @commands.command()
    async def robocop(self):
        """About the bot"""
        embed = discord.Embed(title="Robocop", color=discord.Color.green())
        embed.set_author(name="")
        embed.set_thumbnail(url="http://i.imgur.com/0iDmGQa.png")
        embed.description = "Based off of Kurisu by 916253 and ihaveamac"
        await self.bot.say("", embed=embed)

    @commands.command()
    async def membercount(self):
        """Prints the member count of the server."""
        await self.bot.say("{} has {:,} members!".format(self.bot.server.name, self.bot.server.member_count))

    @commands.has_permissions(ban_members=True)
    @commands.command(hidden=True)
    async def embedtext(self, *, text):
        """Embed content."""
        await self.bot.say(embed=discord.Embed(description=text))

    @commands.command(hidden=True)
    async def timedelta(self, length):
        # thanks Luc#5653
        units = {
            "d": 86400,
            "h": 3600,
            "m": 60,
            "s": 1
        }
        seconds = 0
        match = re.findall("([0-9]+[smhd])", length)  # Thanks to 3dshax server's former bot
        if match is None:
            return None
        for item in match:
            seconds += int(item[:-1]) * units[item[-1]]
        curr = datetime.datetime.now()
        diff = datetime.timedelta(seconds=seconds)
        # http://stackoverflow.com/questions/2119472/convert-a-timedelta-to-days-hours-and-minutes
        # days, hours, minutes = td.days, td.seconds//3600, (td.seconds//60)%60
        msg = "```\ncurr: {}\nnew:  {}\ndiff: {}\n```".format(
            curr,
            curr + diff,
            diff
        )
        await self.bot.say(msg)






def setup(bot):
    bot.add_cog(Extras(bot))
