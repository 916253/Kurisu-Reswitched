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

    async def process_message(self, message):
        if message.channel == self.bot.welcome_channel:
            member = message.author
            full_name = str(member)
            allowed_names = ['@' + full_name, full_name, member.id,
                    '@' + full_name + '\n', full_name + '\n', member.id + '\n']

            hashed_names = [hashlib.sha1(name.encode('utf-8')).hexdigest() for name in allowed_names]
            hashed_names = hashed_names + [h.upper() for h in hashed_names]

            if any(hashed_name in message.content for hashed_name in hashed_names):
                await self.bot.add_roles(message.author, self.bot.unprobated_role)
                await self.bot.purge_from(self.bot.welcome_channel, limit=100, check=lambda m: m.author == message.author or (m.author == self.bot.user and message.author.mention in m.content))
            elif full_name in message.content:
                await self.bot.send_message(message.channel, message.author.mention + " :no_entry: Incorrect, do not just post your name and discriminator. Please reread the rules carefully")

    async def on_message(self, message):
        try:
            await self.process_message(message)
        except discord.errors.Forbidden:
            await self.bot.say("💢 I don't have permission to do this.")

    async def on_message_edit(self, before, after):
        try:
            await self.process_message(after)
        except discord.errors.Forbidden:
            await self.bot.say("💢 I don't have permission to do this.")

def setup(bot):
    bot.add_cog(ProbationBot(bot))
