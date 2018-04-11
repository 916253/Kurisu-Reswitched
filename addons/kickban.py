import datetime
import discord
import json
import re
import time
from discord.ext import commands
from sys import argv

class KickBan:
    """
    Kicking and banning users.
    """
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.has_permissions(manage_nicknames=True)
    @commands.command(pass_context=True, name="kick")
    async def kick_member(self, ctx, user, *, reason=""):
        """Kicks a user from the server. Staff only."""
        try:
            try:
                member = ctx.message.mentions[0]
            except IndexError:
                await self.bot.say("Please mention a user.")
                return
            msg = "You were kicked from {}.".format(self.bot.server.name)
            if reason != "":
                msg += " The given reason is: " + reason
            msg += "\n\nYou are able to rejoin the server, but please be sure to behave when participating again."
            try:
                await self.bot.send_message(member, msg)
            except discord.errors.Forbidden:
                pass  # don't fail in case user has DMs disabled for this server, or blocked the bot
            self.bot.actions.append("uk:"+member.id)
            await self.bot.kick(member)
            msg = "👢 **Kick**: {} kicked {} | {}#{}\n🏷 __User ID__: {}".format(ctx.message.author.mention, member.mention, self.bot.escape_name(member.name), member.discriminator, member.id)
            if reason != "":
                msg += "\n✏️ __Reason__: " + reason
            await self.bot.send_message(self.bot.modlogs_channel, msg + ("\nPlease add an explanation below. In the future, it is recommended to use `.kick <user> [reason]` as the reason is automatically sent to the user." if reason == "" else ""))
        except discord.errors.Forbidden:
            await self.bot.say("💢 I don't have permission to do this.")

    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True, name="ban")
    async def ban_member(self, ctx, user, *, reason=""):
        """Bans a user from the server. Staff only."""
        issuer = ctx.message.author
        try:
            try:
                member = ctx.message.mentions[0]
            except IndexError:
                await self.bot.say("Please mention a user.")
                return
            if self.bot.halfop_role in issuer.roles:
                if self.bot.unprobated_role in member.roles:
                    await self.bot.say("{} You can only use this on members in probation.".format(issuer.mention))
                    return
            msg = "You were banned from {}.".format(self.bot.server.name)
            if reason != "":
                msg += " The given reason is: " + reason
            msg += "\n\nThis ban does not expire."
            try:
                await self.bot.send_message(member, msg)
            except discord.errors.Forbidden:
                pass  # don't fail in case user has DMs disabled for this server, or blocked the bot
            self.bot.actions.append("ub:"+member.id)
            await self.bot.ban(member, 0)
            await self.bot.say("{} is now b&. 👍".format(self.bot.escape_name(member)))
            msg = "⛔ **Ban**: {} banned {} | {}#{}\n🏷 __User ID__: {}".format(issuer.mention, member.mention, self.bot.escape_name(member.name), member.discriminator, member.id)
            if reason != "":
                msg += "\n✏️ __Reason__: " + reason
            await self.bot.send_message(self.bot.modlogs_channel, msg + ("\nPlease add an explanation below. In the future, it is recommended to use `.ban <user> [reason]` as the reason is automatically sent to the user." if reason == "" else ""))
        except discord.errors.Forbidden:
            await self.bot.say("💢 I don't have permission to do this.")

    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True, name="silentban", hidden=True)
    async def silentban_member(self, ctx, user, *, reason=""):
        """Bans a user from the server, without a notification. OP+ only."""
        try:
            try:
                member = ctx.message.mentions[0]
            except IndexError:
                await self.bot.say("Please mention a user.")
                return
            self.bot.actions.append("ub:"+member.id)
            await self.bot.ban(member, 0)
            await self.bot.say("{} is now b&. 👍".format(self.bot.escape_name(member)))
            msg = "⛔ **Silent ban**: {} banned {} | {}#{}\n🏷 __User ID__: {}".format(ctx.message.author.mention, member.mention, self.bot.escape_name(member.name), member.discriminator, member.id)
            if reason != "":
                msg += "\n✏️ __Reason__: " + reason
            await self.bot.send_message(self.bot.serverlogs_channel, msg)
            await self.bot.send_message(self.bot.modlogs_channel, msg + ("\nPlease add an explanation below. In the future, it is recommended to use `.silentban <user> [reason]`." if reason == "" else ""))
        except discord.errors.Forbidden:
            await self.bot.say("💢 I don't have permission to do this.")


def setup(bot):
    bot.add_cog(KickBan(bot))
