import discord
import json
import re
from inspect import cleandoc
from random import randint, choice
from discord.ext import commands
from subprocess import call
from sys import argv
import time

welcome_header = """
<:ReSwitched:326421448543567872> __**Welcome to ReSwitched!**__

__**Be sure you read the following rules and information before participating. If you came here to ask about "backups", this is NOT the place.**__:

​:bookmark_tabs:__Rules:__
"""

welcome_rules = (
    # 1
    """
    Read all the rules before participating in chat. Not reading the rules is *not* an excuse for breaking them.
     • It's suggested that you read channel topics and pins before asking questions as well, as some questions may have already been answered in those.
    """,

    # 2
    """
    Be nice to each other. It's fine to disagree, it's not fine to insult or attack other people.
     • You may disagree with anyone or anything you like, but you should try to keep it to opinions, and not people. Avoid vitriol.
     • Constant antagonistic behavior is considered uncivil and appropriate action will be taken.
     • The use of derogatory slurs -- sexist, racist, homophobic, or otherwise -- is unacceptable and may be grounds for an immediate ban.
    """,

    # 3
    'If you have concerns about another user, please take up your concerns with a staff member (myself or someone with the "moderator" role in the sidebar) in private. Don\'t publicly call other users out.',

    # 4
    """
    From time to time, we may mention everyone in the server. We do this when we feel something important is going on that requires attention. Complaining about these pings may result in a ban.
     • To disable notifications for these pings, suppress them in "ReSwitched → Notification Settings".
    """,

    # 5
    """
    "Don't spam.
     • For excessively long text, use a service like <https://0bin.net/>.
    """,

    # 6
    "Don't brigade, raid, or otherwise attack other people or communities. Don't discuss participation in these attacks. This may warrant an immediate permanent ban.",

    # 7
    'Off-topic content goes to #off-topic. Keep low-quality content like memes out.',

    # 8
    'Trying to evade, look for loopholes, or stay borderline within the rules will be treated as breaking them.',

    # 9
    'Absolutely no piracy. There is a zero-tolerance policy and we will enforce this strictly and swiftly.',

    # 10
    'The first character of your server nickname should be alphanumeric if you wish to talk in chat.'
)

welcome_footer = (
    """
    :hash: __Channel Breakdown:__
    #news - Used exclusively for updates on ReSwitched progress and community information. Most major announcements are passed through this channel and whenever something is posted there it's usually something you'll want to look at.

    #vvv-faq - Answers to most frequently asked questions on this server. You'll probably want to read through this.

    #switch-hacking-meta - For "meta-discussion" related to hacking the switch. This is where we talk *about* the switch hacking that's going on, and where you can get clarification about the hacks that exist and the work that's being done.

    #user-support - End-user focused support, mainly between users. Ask your questions about using switch homebrew here.

    #tool-support - Developer focused support. Ask your questions about using PegaSwitch, libtransistor, Mephisto, and other tools here.

    #hack-n-all - General hacking, hardware and software development channel for hacking on things *other* than the switch. This is a great place to ask about hacking other systems-- and for the community to have technical discussions.

    #exchange - For hunting switches. People selling switches on low firmwares, and discussion about where to find homebrewable switches should go there.
    """,

    """
    #switch-hacking-general - Channel for everyone working on hacking the switch-- both in an exploit and a low-level hardware sense. This is where a lot of our in-the-open development goes on. Note that this isn't the place for developing homebrew-- we have #homebrew-development for that!

    #homebrew-development - Discussion about the development of homebrew goes there. Feel free to show off your latest creation here.

    #off-topic - Channel for discussion of anything that doesn't belong in #general. Anything goes, so long as you make sure to follow the rules and be on your best behavior.

    #toolchain-development - Discussion about the development of libtransistor itself goes there.

    #cfw-development - Development discussion regarding custom firmware (CFW) projects, such as Atmosphère. This channel is meant for the discussion accompanying active development.

    **If you are still not sure how to get access to the other channels, please read the rules again.**
    **If you have questions about the rules, feel free to ask here!**

    **Note: We know if you have read the rules or not. If you falsely claim to read the rules, we will kick the first time and ban the second.**
    """,
)

hidden_term_line = ' • When you have finished reading all of the rules, send a message in this channel that includes the phrase "{}", and we\'ll grant you access to the other channels. Failure to do so may result in being kicked out.'


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

    @commands.command(pass_context=True, hidden=True)
    async def pull(self, ctx):
        """Pull new changes from GitHub and restart."""
        issuer = ctx.message.author
        if (self.bot.owner_role not in issuer.roles):
            msg = "{} This command is limited to wizards.".format(issuer.mention)
            await self.bot.say(msg)
            return
        await self.bot.say("Pulling changes...")
        call(['git', 'pull'])
        await self.bot.say("👋 Restarting bot!")
        await self.bot.close()

    @commands.has_permissions(kick_members=True)
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

    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True, name="reset")
    async def reset(self, ctx, limit: int = 100, force: str = ""):
        """Wipes messages in #newcomers and pastes the welcome message again. Staff only."""
        if ctx.message.channel != self.bot.welcome_channel and force != "force":
            await self.bot.say("This command is limited to <#{}>".format(self.bot.welcome_channel.id))
            return

        try:
            await self.bot.purge_from(ctx.message.channel, limit=limit)

            probate_phrases = self.bot.config['Probate']['Phrases'].split(',')
            phrase = choice(probate_phrases).strip()

            await self.bot.say(welcome_header)
            rules = ['**{}**. {}'.format(i, cleandoc(r)) for i, r in enumerate(welcome_rules, 1)]
            rule_choice = randint(1, len(rules))
            rules[rule_choice - 1] += '\n' + hidden_term_line.format(phrase)
            msg = "🗑 **Reset**: {} cleared {} messages in {}".format(ctx.message.author.mention, limit, ctx.message.channel.mention)
            msg += "\n💬 __Current phrase__: **{}**, under rule {}".format(phrase, rule_choice)
            await self.bot.send_message(self.bot.modlogs_channel, msg)

            # find rule that puts us over 2,000 characters, if any
            total = 0
            messages = []
            current_message = ""
            for item in rules:
                total += len(item) + 2 # \n\n
                if total < 2000:
                    current_message += item + "\n\n"
                else:
                    # we've hit the limit; split!
                    messages += [current_message]
                    current_message = "\n\u200B\n" + item + "\n\u200B\n"
                    total = 0
            messages += [current_message]

            for item in messages:
                await self.bot.say(item)

            for x in welcome_footer:
                await self.bot.say(cleandoc(x))
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
            await self.bot.add_roles(member, self.bot.unprobated_role)
            msg = "🚫 **Unprobated**: {} unprobated {} | {}#{}".format(ctx.message.author.mention, member.mention, self.bot.escape_name(member.name), self.bot.escape_name(member.discriminator))
            await self.bot.send_message(self.bot.modlogs_channel, msg)
        except discord.errors.Forbidden:
            await self.bot.say("💢 I don't have permission to do this.")

    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True, name="approve")
    async def approve(self, ctx, *users):
        """Approve a user, giving them the community role."""
        members = []
        for member in ctx.message.mentions:
            await self.bot.add_roles(member, self.bot.community_role)
            members.append(member.mention)
        await self.bot.say("Approved {} member(s).".format(len(members)))
        msg = "✅ **Approved**: {} approved {} members\n".format(ctx.message.author.mention, len(members))
        msg += ', '.join(members)
        await self.bot.send_message(self.bot.modlogs_channel, msg)

    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True, name="revoke")
    async def revoke(self, ctx, *users):
        """Un-approve a user, removing the community role."""
        members = []
        for member in ctx.message.mentions:
            await self.bot.remove_roles(member, self.bot.community_role)
            members.append(member.mention)
        await self.bot.say("Un-approved {} member(s).".format(len(members)))
        msg = "❌ **Un-approved**: {} approved {} members\n".format(ctx.message.author.mention, len(members))
        msg += ', '.join(members)
        await self.bot.send_message(self.bot.modlogs_channel, msg)

    @commands.command(pass_context=True, name="addhacker")
    async def addhacker(self, ctx, user):
        """Add the hacker role to a user."""
        issuer = ctx.message.author
        if (self.bot.private_role not in issuer.roles) and (self.bot.staff_role not in issuer.roles):
            await self.bot.say("{} This command is limited to private and mod.".format(issuer.mention))
            return
        try:
            member = ctx.message.mentions[0]
        except IndexError:
            await self.bot.say("Please mention a user.")
            return
        await self.bot.add_roles(member, self.bot.hacker_role)
        await self.bot.say("{} is now a hacker.".format(member.mention))
        msg = "💻 **Hacker**: {} added hacker to {} | {}#{}".format(issuer.mention, member.mention, self.bot.escape_name(member.name), self.bot.escape_name(member.discriminator))
        await self.bot.send_message(self.bot.modlogs_channel, msg)

    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True, name="probate")
    async def probate(self, ctx, user, *, reason=""):
        """Probate a user. Staff only."""
        try:
            member = ctx.message.mentions[0]
            await self.bot.remove_roles(member, self.bot.unprobated_role)
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

    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True, name="unprobate")
    async def unprobate(self, ctx, user):
        """Unprobate a user. Staff only."""
        try:
            for member in ctx.message.mentions:
                await self.bot.add_roles(member, self.bot.unprobated_role)
            await self.bot.say("Un-probated {}".format(", ".join(member.mention for member in ctx.message.mentions)))
            unprobated_list = ", ".join("{} | {}#{}".format(member.mention, self.bot.escape_name(member.name), self.bot.escape_name(member.discriminator)) for member in ctx.message.mentions)
            msg = "⭕️ **Un-probated**: {} un-probated {}".format(ctx.message.author.mention, unprobated_list)
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
