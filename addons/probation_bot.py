from discord.ext import commands
import hashlib

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
                full_name = member.name + '#' + member.discriminator
                full_name_hex = hashlib.sha1(full_name.encode('utf-8')).hexdigest()
                # For those people using a shell and forgetting to use echo -n
                full_name_endl_hex = hashlib.sha1((full_name + '\n').encode('utf-8')).hexdigest()
                if full_name_hex in message.content or full_name_endl_hex in message.content:
                    # Auto unprobate
                    await self.bot.add_roles(member, self.bot.unprobated_role)
                    await self.bot.delete_message(message)
        except discord.errors.Forbidden:
            await self.bot.say("💢 I don't have permission to do this.")

def setup(bot):
    bot.add_cog(ProbationBot(bot))
