#Importing libraries
import discord
from discord.ext import commands
from sys import argv

class Lockdown:
    """
    Channel lockdown commands.
    """
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.has_permissions(manage_messages=True)
    @commands.command(pass_context=True, name="lock")
    async def lock(self, ctx):
        """Lock message sending in the channel. Staff only."""
        try:
            if ctx.message.channel in self.bot.community_channels:
                roles = (self.bot.community_role, self.bot.hacker_role)
            else:
                roles = (self.bot.everyone_role,)
            overwrites = ctx.message.channel.overwrites_for(roles[0])
            if overwrites.send_messages is False:
                await self.bot.say("🔒 Channel is already locked down. Use `.unlock [community]` to unlock.")
                return
            overwrites.send_messages = False
            overwrites.add_reactions = False
            await asyncio.gather(self.bot.edit_channel_permissions(ctx.message.channel, role, overwrites) for role in roles)
            await self.bot.say("🔒 Channel locked down. Only staff members may speak. Do not bring the topic to other channels or risk disciplinary actions.")
            msg = "🔒 **Lockdown**: {0} by {1} | {2}#{3}".format(ctx.message.channel.mention, ctx.message.author.mention, ctx.message.author.name, ctx.message.author.discriminator)
            await self.bot.send_message(self.bot.modlogs_channel, msg)

        except discord.errors.Forbidden:
            await self.bot.say("💢 I don't have permission to do this.")

    @commands.has_permissions(manage_messages=True)
    @commands.command(pass_context=True, name="softlock")
    async def softlock(self, ctx):
        """Lock message sending in the channel, without the "disciplinary action" note. Staff only."""
        try:
            if ctx.message.channel in self.bot.community_channels:
                roles = (self.bot.community_role, self.bot.hacker_role)
            else:
                roles = (self.bot.everyone_role,)
            overwrites = ctx.message.channel.overwrites_for(role)
            if overwrites.send_messages is False:
                await self.bot.say("🔒 Channel is already locked down. Use `.unlock [community]` to unlock.")
                return
            overwrites.send_messages = False
            overwrites.add_reactions = False
            await asyncio.gather(self.bot.edit_channel_permissions(ctx.message.channel, role, overwrites) for role in roles)
            await self.bot.say("🔒 Channel locked.")
            msg = "🔒 **Soft-lock**: {0} by {1} | {2}#{3}".format(ctx.message.channel.mention, ctx.message.author.mention, ctx.message.author.name, ctx.message.author.discriminator)
            await self.bot.send_message(self.bot.modlogs_channel, msg)
        except discord.errors.Forbidden:
            await self.bot.say("💢 I don't have permission to do this.")

    @commands.has_permissions(manage_messages=True)
    @commands.command(pass_context=True, name="unlock")
    async def unlock(self, ctx):
        """Unlock message sending in the channel. Staff only."""
        try:
            if ctx.message.channel in self.bot.community_channels:
                roles = (self.bot.community_role, self.bot.hacker_role)
            else:
                roles = (self.bot.everyone_role,)
            overwrites = ctx.message.channel.overwrites_for(role)
            if overwrites.send_messages is True:
                await self.bot.say("🔓 Channel is already unlocked.")
                return
            overwrites.send_messages = True
            overwrites.add_reactions = True
            await asyncio.gather(self.bot.edit_channel_permissions(ctx.message.channel, role, overwrites) for role in roles)
            await self.bot.say("🔓 Channel unlocked.")
            msg = "🔓 **Unlock**: {0} by {1} | {2}#{3}".format(ctx.message.channel.mention, ctx.message.author.mention, ctx.message.author.name, ctx.message.author.discriminator)
            await self.bot.send_message(self.bot.modlogs_channel, msg)

        except discord.errors.Forbidden:
            await self.bot.say("💢 I don't have permission to do this.")

def setup(bot):
    bot.add_cog(Lockdown(bot))
