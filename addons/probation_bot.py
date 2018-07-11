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

    async def on_message(self, message):
        try:
            if message.channel == self.bot.welcome_channel:
                member = message.author
                full_name = str(member)
                allowed_names = ['@' + full_name, full_name, member.id,
                        '@' + full_name + '\n', full_name + '\n', member.id + '\n']

                hashed_names = [hashlib.sha1(name.encode('utf-8')).hexdigest() for name in allowed_names]
                hashed_names = hashed_names + [h.upper() for h in hashed_names]

                if any(hashed_name in message.content for hashed_name in hashed_names):
                    # Auto unprobate
                    await self.bot.add_roles(member, self.bot.unprobated_role)
                    await self.bot.delete_message(message)
        except discord.errors.Forbidden:
            await self.bot.say("💢 I don't have permission to do this.")

def setup(bot):
    bot.add_cog(ProbationBot(bot))
