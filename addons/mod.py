import discord
import json
import re
from discord.ext import commands
from subprocess import call
from sys import argv

class Mod:
    """
    Staff commands.
    """
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    async def add_restriction(self, member, rst):
        with open("data/restrictions.json", "r") as f:
            rsts = json.load(f)
        if member.id not in rsts:
            rsts[member.id] = []
        if rst not in rsts[member.id]:
            rsts[member.id].append(rst)
        with open("data/restrictions.json", "w") as f:
            json.dump(rsts, f)

    async def remove_restriction(self, member, rst):
        with open("data/restrictions.json", "r") as f:
            rsts = json.load(f)
        if member.id not in rsts:
            rsts[member.id] = []
        if rst in rsts[member.id]:
            rsts[member.id].remove(rst)
        with open("data/restrictions.json", "w") as f:
            json.dump(rsts, f)

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def quit(self, *gamename):
        """Stops the bot."""
        await self.bot.say("👋 Bye bye!")
        await self.bot.close()

    @commands.has_permissions(manage_server=True)
    @commands.command(pass_context=True, hidden=True)
    async def userinfo(self, ctx, user):
        """Gets user info. SuperOP+."""
        u = ctx.message.mentions[0]
        role = u.top_role.name
        if role == "@everyone":
            role = "@ everyone"
        await self.bot.say("name = {}\nid = {}\ndiscriminator = {}\navatar = {}\nbot = {}\navatar_url = {}\ndefault_avatar = {}\ndefault_avatar_url = <{}>\ncreated_at = {}\ndisplay_name = {}\njoined_at = {}\nstatus = {}\ngame = {}\ncolour = {}\ntop_role = {}\n".format(u.name, u.id, u.discriminator, u.avatar, u.bot, u.avatar_url, u.default_avatar, u.default_avatar_url, u.created_at, u.display_name, u.joined_at, u.status, u.game, u.colour, role))


    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True, name="clear")
    async def purge(self, ctx, limit: int):
       """Clears a given number of messages. Staff only."""
       try:
           await self.bot.purge_from(ctx.message.channel, limit=limit)
           msg = "🗑 **Cleared**: {} cleared {} messages in {}".format(ctx.message.author.mention, limit, ctx.message.channel.mention)
           await self.bot.send_message(self.bot.modlogs_channel, msg)
       except discord.errors.Forbidden:
           await self.bot.say("💢 I don't have permission to do this.")
           
    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True, name="reset")
    async def reset(self, ctx, limit: int):
       """Wipes messages in #newcomers and pastes the welcome message again. Staff only."""
       try:
           await self.bot.purge_from(ctx.message.channel, limit=limit)
           msg = "🗑 **Reset**: {} cleared {} messages in {}".format(ctx.message.author.mention, limit, ctx.message.channel.mention)
           await self.bot.send_message(self.bot.modlogs_channel, msg)
           await self.bot.say("<:ReSwitched:326421448543567872> __**Welcome to ReSwitched!**__\n ​ \nBe sure you read the following rules and information before participating:\n ​ \n​:bookmark_tabs:__Rules:__ \n**1**. Read all the rules before participating in chat. Not reading the rules is *not* an excuse for breaking them.\n • It's suggested that you read channel topics and pins before asking questions as well, as some questions may have already been answered in those. \n ​ \n**2**. Be nice to each other. It's fine to disagree, it's not fine to insult or attack other people. \n • You may disagree with anyone or anything you like, but you should try to keep it to opinions, and not people. Avoid vitriol. \n • Constant antagonistic behavior is considered uncivil and appropriate action will be taken. \n ​ \n**3**. If you have concerns about another user, please take up your concerns with a staff member (myself or someone with the \"moderator\" role in the sidebar) in private. Don't publicly call other users out. \n ​ \n**4**. Don't spam. \n • For excessively long text, use a service like https://0bin.net/. \n ​• When you are asking us to give you access to the other channels, please include \"readthefuckingmanual\" in your message. Failure to do so may result in being kicked out. \n ​ \n**5**. Don't brigade, raid, or otherwise attack other people or communities. Don't discuss participation in these attacks. This may warrant an immediate permanent ban. \n ​ \n**6**. Off-topic content goes to #off-topic. Keep low-quality content like memes out. \n ​ \n**7**. Trying to evade, look for loopholes, or stay borderline within the rules will be treated as breaking them. \n ​ \n​**8**. Absolutely no piracy. There is a zero-tolerance policy and we will enforce this strictly and swiftly. \n ​ \n")
           await self.bot.say(":hash: __Channel Breakdown:__ \n#news - Used exclusively for updates on ReSwitched progress and community information. Most major announcements are passed through this channel and whenever something is posted there it's usually something you'll want to look at.\n ​ \n#general -  All things switch-hacking related. We try to keep this channel on-topic in that respect as much as possible, though it does drift a bit. If you have any questions about the state of switch hacking, how to get set up, etc, #general is the place to ask.\n ​ \n#off-topic - Channel for discussion of anything that doesn't belong in #general. Anything goes, so long as you make sure to follow the rules and be on your best behavior.")
           await self.bot.say("**When you have read everything, send a message in this channel to ask us to give you access to the other channels. Have a nice day!**")
       except discord.errors.Forbidden:
           await self.bot.say("💢 I don't have permission to do this.")

    @commands.has_permissions(manage_nicknames=True)
    @commands.command(pass_context=True, name="mute")
    async def mute(self, ctx, user, *, reason=""):
        """Mutes a user so they can't speak. Staff only."""
        try:
            member = ctx.message.mentions[0]
            await self.add_restriction(member, "Muted")
            await self.bot.add_roles(member, self.bot.muted_role)
            msg_user = "You were muted!"
            if reason != "":
                msg_user += " The given reason is: " + reason
            try:
                await self.bot.send_message(member, msg_user)
            except discord.errors.Forbidden:
                pass  # don't fail in case user has DMs disabled for this server, or blocked the bot
            await self.bot.say("{} can no longer speak.".format(member.mention))
            msg = "🔇 **Muted**: {} muted {} | {}#{}".format(ctx.message.author.mention, member.mention, self.bot.escape_name(member.name), self.bot.escape_name(member.discriminator))
            if reason != "":
                msg += "\n✏️ __Reason__: " + reason
            else:
                msg += "\nPlease add an explanation below. In the future, it is recommended to use `.mute <user> [reason]` as the reason is automatically sent to the user."
            await self.bot.send_message(self.bot.modlogs_channel, msg)
        except discord.errors.Forbidden:
            await self.bot.say("💢 I don't have permission to do this.")

    @commands.has_permissions(manage_nicknames=True)
    @commands.command(pass_context=True, name="unmute")
    async def unmute(self, ctx, user):
        """Unmutes a user so they can speak. Staff only."""
        try:
            member = ctx.message.mentions[0]
            await self.remove_restriction(member, "Muted")
            await self.bot.remove_roles(member, self.bot.muted_role)
            await self.bot.say("{} can now speak again.".format(member.mention))
            msg = "🔈 **Unmuted**: {} unmuted {} | {}#{}".format(ctx.message.author.mention, member.mention, self.bot.escape_name(member.name), self.bot.escape_name(member.discriminator))
            await self.bot.send_message(self.bot.modlogs_channel, msg)
        except discord.errors.Forbidden:
            await self.bot.say("💢 I don't have permission to do this.")


    @commands.command(pass_context=True, name="secure")
    async def secure(self, ctx, user, *, reason=""):
        """Give access to the hacker role"""
        author = ctx.message.author
        if (self.bot.owner_role not in author.roles):
            msg = "{} You cannot used this command.".format(author.mention)
            await self.bot.say(msg)
            return
        try:
            member = ctx.message.mentions[0]
            await self.bot.add_roles(member, self.bot.nohelp_role)
            msg = "⭕️ **Secure channel access**: {} gave access to secure channels to {} | {}#{}".format(ctx.message.author.mention, member.mention, self.bot.escape_name(member.name), self.bot.escape_name(member.discriminator))
            await self.bot.send_message(self.bot.modlogs_channel, msg)
        except discord.errors.Forbidden:
            await self.bot.say("💢 I don't have permission to do this.")

    @commands.command(pass_context=True, name="insecure")
    async def insecure(self, ctx, user):
        """take away the probation role"""
        author = ctx.message.author
        if (self.bot.owner_role not in author.roles):
            msg = "{} You cannot used this command.".format(author.mention)
            await self.bot.say(msg)
            return
        try:
            member = ctx.message.mentions[0]
            await self.bot.remove_roles(member, self.bot.probation_role)
            msg = "🚫 **Unprobated**: {} unprobated {} | {}#{}".format(ctx.message.author.mention, member.mention, self.bot.escape_name(member.name), self.bot.escape_name(member.discriminator))
            await self.bot.send_message(self.bot.modlogs_channel, msg)
        except discord.errors.Forbidden:
            await self.bot.say("💢 I don't have permission to do this.")
            
    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True, name="probate")
    async def probate(self, ctx, user, *, reason=""):
        """Probate a user. Staff only."""
        try:
            member = ctx.message.mentions[0]
            await self.add_restriction(member, "Probation")
            await self.bot.add_roles(member, self.bot.probation_role)
            msg_user = "You are under probation!"
            if reason != "":
                msg_user += " The given reason is: " + reason
            try:
                await self.bot.send_message(member, msg_user)
            except discord.errors.Forbidden:
                pass  # don't fail in case user has DMs disabled for this server, or blocked the bot
            await self.bot.say("{} is now in probation.".format(member.mention))
            msg = "🚫 **Probated**: {} probated {} | {}#{}".format(ctx.message.author.mention, member.mention, self.bot.escape_name(member.name), self.bot.escape_name(member.discriminator))
            if reason != "":
                msg += "\n✏️ __Reason__: " + reason
            else:
                msg += "\nPlease add an explanation below. In the future, it is recommended to use `.probate <user> [reason]` as the reason is automatically sent to the user."
            await self.bot.send_message(self.bot.modlogs_channel, msg)
        except discord.errors.Forbidden:
            await self.bot.say("💢 I don't have permission to do this.")

    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True, name="unprobate")
    async def unprobate(self, ctx, user):
        """Unprobate a user. Staff only."""
        try:
            member = ctx.message.mentions[0]
            await self.remove_restriction(member, "Probation")
            await self.bot.remove_roles(member, self.bot.probation_role)
            await self.bot.say("{} is out of probation.".format(member.mention))
            msg = "⭕️ **Un-probated**: {} un-probated {} | {}#{}".format(ctx.message.author.mention, member.mention, self.bot.escape_name(member.name), self.bot.escape_name(member.discriminator))
            await self.bot.send_message(self.bot.modlogs_channel, msg)
        except discord.errors.Forbidden:
            await self.bot.say("💢 I don't have permission to do this.")



    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True)
    async def playing(self, ctx, *gamename):
        """Sets playing message. Staff only."""
        try:
            await self.bot.change_presence(game=discord.Game(name='{}'.format(" ".join(gamename))))
        except discord.errors.Forbidden:
            await self.bot.say("💢 I don't have permission to do this.")

    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True)
    async def status(self, ctx, status):
        """Sets status. Staff only."""
        try:
            if status == "online":
                await self.bot.change_presence(status=discord.Status.online)
            elif status == "offline":
                await self.bot.change_presence(status=discord.Status.offline)
            elif status == "idle":
                await self.bot.change_presence(status=discord.Status.idle)
            elif status == "dnd":
                await self.bot.change_presence(status=discord.Status.dnd)
            elif status == "invisible":
                await self.bot.change_presence(status=discord.Status.invisible)
        except discord.errors.Forbidden:
            await self.bot.say("💢 I don't have permission to do this.")

    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True, hidden=True)
    async def username(self, ctx, *, username):
        """Sets bot name. Staff only."""
        try:
            await self.bot.edit_profile(username=('{}'.format(username)))
        except discord.errors.Forbidden:
            await self.bot.say("💢 I don't have permission to do this.")

def setup(bot):
    bot.add_cog(Mod(bot))
