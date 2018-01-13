import asyncio
import discord
import json
import re
from discord.ext import commands
from subprocess import call
from string import printable
from sys import argv

class Events:
    """
    Special event handling.
    """
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    # I hate naming variables sometimes
    user_antispam = {}
    channel_antispam = {}

    async def add_restriction(self, member, rst):
        with open("data/restrictions.json", "r") as f:
            rsts = json.load(f)
        if member.id not in rsts:
            rsts[member.id] = []
        if rst not in rsts[member.id]:
            rsts[member.id].append(rst)
        with open("data/restrictions.json", "w") as f:
            json.dump(rsts, f)

    async def scan_message(self, message):
        embed = discord.Embed()
        embed.description = message.content

    async def on_message(self, message):
        if message.mention_everyone:
            channel = message.channel
            overwrites = channel.overwrites_for(self.bot.everyone_role)
            ow_old_value1 = overwrites.send_messages
            ow_old_value2 = overwrites.add_reactions
            if ow_old_value1 is False:
                return
            overwrites.send_messages = False
            overwrites.add_reactions = False
            await self.bot.edit_channel_permissions(channel, self.bot.everyone_role, overwrites)
            await self.bot.send_message(self.bot.modlogs_channel, "🔒 **Auto-Lockdown**: {} auto-locked due to mention of everyone".format(channel.mention))
            await asyncio.sleep(60 * 2)
            overwrites.send_messages = ow_old_value1
            overwrites.add_reactions = ow_old_value2
            await self.bot.edit_channel_permissions(channel, self.bot.everyone_role, overwrites)
            await self.bot.send_message(self.bot.modlogs_channel, "🔒 **Auto-Unlock**: {}".format(channel.mention))


def setup(bot):
    bot.add_cog(Events(bot))
