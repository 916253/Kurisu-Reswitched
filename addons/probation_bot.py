from discord.ext import commands
import hashlib
from itertools import chain

class ProbationBot:
    """
    Kicking and banning users.
    """
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    def contains(self, message):
        if message.channel == self.bot.welcome_channel:
            member = message.author
            full_name = str(member)
            allowed_names = ['@' + full_name, full_name, member.id,
                    '@' + full_name + '\n', full_name + '\n', member.id + '\n']

            hashed_names = [hashlib.sha1(name.encode('utf-8')).hexdigest() for name in allowed_names]
            hashed_names = hashed_names + [h.upper() for h in hashed_names]

            return any(hashed_name in message.content for hashed_name in hashed_names)
        else:
            return False

    async def on_message(self, message):
        try:
            if self.contains(message):
                    await self.bot.add_roles(message.author, self.bot.unprobated_role)
                    await self.bot.purge_from(self.bot.welcome_channel, limit=100, check=lambda m: m.author == message.author)
        except discord.errors.Forbidden:
            await self.bot.say("💢 I don't have permission to do this.")

    async def on_message_edit(self, before, after):
        try:
            if self.contains(after):
                    await self.bot.add_roles(after.author, self.bot.unprobated_role)
                    await self.bot.purge_from(self.bot.welcome_channel, limit=100, check=lambda m: m.author == after.author)
        except discord.errors.Forbidden:
            await self.bot.say("💢 I don't have permission to do this.")

def setup(bot):
    bot.add_cog(ProbationBot(bot))
