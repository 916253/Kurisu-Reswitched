import discord
import random
from discord.ext import commands


class Meme:
    """
    Meme commands.
    """

    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    def check_if_ot(self, ctx):
        is_ot = (ctx.channel.name == "off-topic")
        return is_ot

    @commands.command(pass_context=True, hidden=True, name="bam")
    async def bam_member(self, ctx, user: discord.Member, *, reason=""):
        """Bams a user owo"""
        if self.check_if_ot(ctx):
            await self.bot.say("{} is ̶n͢ow b̕&̡.̷ 👍̡".format(self.bot.escape_name(user)))

    @commands.command(pass_context=True, hidden=True, name="warm")
    async def warm_member(self, ctx, user: discord.Member, *, reason=""):
        """Warms a user :3"""
        if self.check_if_ot(ctx):
            await self.bot.say("{} warmed. User is now {}°C.".format(user.mention, str(random.randint(0, 100))))

    @commands.command(hidden=True)
    async def frolics(self):
        """test"""
        await self.bot.say("https://www.youtube.com/watch?v=VmarNEsjpDI")


def setup(bot):
    bot.add_cog(Meme(bot))
