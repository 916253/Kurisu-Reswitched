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

    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True, name="bam")
    async def bam_member(self, ctx, user: discord.Member, *, reason=""):
        """Bams a user. Staff only."""
        await self.bot.say("{} is ̶n͢ow b̕&̡.̷ 👍̡".format(self.bot.escape_name(user)))

    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True, name="warm")
    async def warm_member(self, ctx, user: discord.Member, *, reason=""):
        """Warms a user :3. Staff only."""
        await self.bot.say("{} warmed. User is now {}°C.".format(user.mention, str(random.randint(0, 100))))


def setup(bot):
    bot.add_cog(Meme(bot))
