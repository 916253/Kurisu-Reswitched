import asyncio
import copy
import discord
import sys
import time
import datetime
import traceback
from discord.ext import commands
from sys import argv

class Loop:
    """
    Loop events.
    """
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    def __unload(self):
        self.is_active = False

    is_active = True

    last_hour = datetime.datetime.now().hour




def setup(bot):
    bot.add_cog(Loop(bot))
