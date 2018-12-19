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
            discrim = member.discriminator
            allowed_names = ['@' + full_name, full_name, member.id,
                    '@' + full_name + '\n', full_name + '\n', member.id + '\n']
            close_names = ['@' + member.name, member.name, discrim, '#' + discrim,
                           '@' + member.name + '\n', member.name + '\n', discrim + '\n', '#' + discrim + '\n']

            hashed_names = [hashlib.sha1(name.encode('utf-8')).hexdigest() for name in allowed_names]
            md5_hashed_names = [hashlib.md5(name.encode('utf-8')).hexdigest() for name in allowed_names]
            hashed_close_names = [hashlib.sha1(name.encode('utf-8')).hexdigest() for name in close_names]

            if any(hashed_name in message.content.lower() for hashed_name in hashed_names):
                await self.bot.add_roles(message.author, self.bot.unprobated_role)
                await self.bot.purge_from(self.bot.welcome_channel, limit=100, check=lambda m: m.author == message.author or (m.author == self.bot.user and message.author.mention in m.content))
            elif any(close_name in message.content.lower() for close_name in hashed_close_names):
                await self.bot.send_message(message.channel, message.author.mention + " :no_entry: Close, but incorrect. You got the process right, but you're not doing it on your name and discriminator properly. Please re-read the rules carefully and look up any terms you are not familiar with.")
            elif any(md5_name in message.content.lower() for md5_name in md5_hashed_names):
                await self.bot.send_message(message.channel, message.author.mention + " :no_entry: Close, but incorrect. You're processing your name and discriminator properly, but you're not using the right process. Please re-read the rules carefully and look up any terms you are not familiar with.")
            elif full_name in message.content or member.id in message.content or member.name in message.content or discrim in message.content:
                await self.bot.send_message(message.channel, message.author.mention + " :no_entry: Incorrect. You need to do something with your name and discriminator instead of just posting it. Please re-read the rules carefully and look up any terms you are not familiar with.")

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
