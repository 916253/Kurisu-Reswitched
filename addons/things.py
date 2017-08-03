import discord
from discord.ext import commands
from sys import argv

class Things:
    """
    Random things.
    """
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.command()
    async def frolics(self):
        """test"""
        await self.bot.say("https://www.youtube.com/watch?v=VmarNEsjpDI")



def setup(bot):
    bot.add_cog(Things(bot))
