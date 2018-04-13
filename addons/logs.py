import discord
import json
from discord.ext import commands
from sys import argv
from datetime import datetime, timedelta

class Logs:
    """
    Logs join and leave messages, bans and unbans, and member changes.
    """
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    async def on_member_join(self, member):
        await self.bot.wait_until_all_ready()
        age = member.joined_at - member.created_at
        if age < timedelta(minutes=15):
            try:
                await self.bot.send_message(member, "Your account is too new to join ReSwitched. Please try again later.")
                sent = True
            except discord.errors.Forbidden:
                sent = False
            self.bot.actions.append("uk:"+member.id)
            await self.bot.kick(member)
            msg = "🚨 **Account too new**: {} | {}#{}\n🗓 __Creation__: {}\n🕓 Account age: {}\n🏷 __User ID__: {}".format(
                member.mention, self.bot.escape_name(member.name), member.discriminator, member.created_at, age, member.id
            )
            if not sent:
                msg += "\nThe user has disabled direct messages, so the reason was not sent."
            await self.bot.send_message(self.bot.serverlogs_channel, msg)
            return
        msg = "✅ **Join**: {} | {}#{}\n🗓 __Creation__: {}\n🕓 Account age: {}\n🏷 __User ID__: {}".format(
            member.mention, self.bot.escape_name(member.name), member.discriminator, member.created_at, age, member.id
        )
        with open("data/restrictions.json", "r") as f:
            rsts = json.load(f)
        if member.id in rsts:
            roles = []
            for rst in rsts[member.id]:
                roles.append(discord.utils.get(self.bot.server.roles, name=rst))
            await self.bot.add_roles(member, *roles)
        with open("data/warnsv2.json", "r") as f:
            warns = json.load(f)
        try:
            if len(warns[member.id]["warns"]) == 0:
                await self.bot.send_message(self.bot.serverlogs_channel, msg)
            else:
                embed = discord.Embed(color=discord.Color.dark_red())
                embed.set_author(name="Warns for {}#{}".format(self.bot.escape_name(member.name), member.discriminator), icon_url=member.avatar_url)
                for idx, warn in enumerate(warns[member.id]["warns"]):
                    embed.add_field(name="{}: {}".format(idx + 1, warn["timestamp"]), value="Issuer: {}\nReason: {}".format(warn["issuer_name"], warn["reason"]))
                await self.bot.send_message(self.bot.serverlogs_channel, msg, embed=embed)
        except KeyError:  # if the user is not in the file
            await self.bot.send_message(self.bot.serverlogs_channel, msg)

    async def on_member_remove(self, member):
        await self.bot.wait_until_all_ready()
        if "uk:"+member.id in self.bot.actions:
            self.bot.actions.remove("uk:"+member.id)
            return
        if "sbk:"+member.id in self.bot.actions:
            self.bot.actions.remove("sbk:"+member.id)
            return
        if self.bot.pruning != 0 and "wk:"+member.id not in self.bot.actions:
            self.bot.pruning -= 1
            if self.bot.pruning == 0:
                await self.bot.send_message(self.bot.mods_channel, "Pruning finished!")
            return
        msg = "{}: {} | {}#{}\n🏷 __User ID__: {}".format("👢 **Auto-kick**" if "wk:"+member.id in self.bot.actions else "⬅️ **Leave**", member.mention, self.bot.escape_name(member.name), member.discriminator, member.id)
        await self.bot.send_message(self.bot.serverlogs_channel, msg)
        if "wk:"+member.id in self.bot.actions:
            self.bot.actions.remove("wk:"+member.id)
            await self.bot.send_message(self.bot.modlogs_channel, msg)

    async def on_member_ban(self, member):
        await self.bot.wait_until_all_ready()
        if "ub:"+member.id in self.bot.actions:
            self.bot.actions.remove("ub:"+member.id)
            return
        msg = "⛔ **{}**: {} | {}#{}\n🏷 __User ID__: {}".format("Auto-ban" if "wb:"+member.id in self.bot.actions else "Ban", member.mention, self.bot.escape_name(member.name), member.discriminator, member.id)
        await self.bot.send_message(self.bot.serverlogs_channel, msg)
        if "wb:"+member.id in self.bot.actions:
            self.bot.actions.remove("wb:"+member.id)
        else:
            msg += "\nThe responsible staff member should add an explanation below."
        await self.bot.send_message(self.bot.modlogs_channel, msg)

    async def on_member_unban(self, server, user):
        await self.bot.wait_until_all_ready()
        if "tbr:"+user.id in self.bot.actions:
            self.bot.actions.remove("tbr:"+user.id)
            return
        msg = "⚠️ **Unban**: {} | {}#{}".format(user.mention, self.bot.escape_name(user.name), user.discriminator)
        if user.id in self.bot.timebans:
            msg += "\nTimeban removed."
            self.bot.timebans.pop(user.id)
            with open("data/timebans.json", "r") as f:
                timebans = json.load(f)
            if user.id in timebans:
                timebans.pop(user.id)
                with open("data/timebans.json", "w") as f:
                    json.dump(timebans, f)
        await self.bot.send_message(self.bot.modlogs_channel, msg)

    async def on_member_update(self, member_before, member_after):
        await self.bot.wait_until_all_ready()
        do_log = False  # only nickname and roles should be logged
        dest = self.bot.modlogs_channel
        if member_before.roles != member_after.roles:
            do_log = True
            dest = self.bot.serverlogs_channel
            # role removal
            role_removal = []
            for index, role in enumerate(member_before.roles):
                if role not in member_after.roles:
                    role_removal.append(role)
            # role addition
            role_addition = []
            for index, role in enumerate(member_after.roles):
                if role not in member_before.roles:
                    role_addition.append(role)

            if len(role_addition) != 0 or len(role_removal) != 0:
                msg = "\n👑 __Role change__: "
                roles = []
                for role in role_removal:
                    roles.append("_~~" + role.name + "~~_")
                for role in role_addition:
                    roles.append("__**" + role.name + "**__")
                for index, role in enumerate(member_after.roles):
                    if role.name == "@everyone":
                        continue
                    if role not in role_removal and role not in role_addition:
                        roles.append(role.name)
                msg += ", ".join(roles)

        if self.bot.escape_name(member_before.name) != self.bot.escape_name(member_after.name):
            do_log = True
            dest = self.bot.serverlogs_channel
            msg = "\n📝 __Username change__: {} → {}".format(self.bot.escape_name(member_before.name), self.bot.escape_name(member_after.name))
        if member_before.nick != member_after.nick:
            do_log = True
            if member_before.nick == None:
                msg = "\n🏷 __Nickname addition__"
            elif member_after.nick == None:
                msg = "\n🏷 __Nickname removal__"
            else:
                msg = "\n🏷 __Nickname change__"
            msg += ": {0} → {1}".format(self.bot.escape_name(member_before.nick), self.bot.escape_name(member_after.nick))
        if do_log:
            msg = "ℹ️ **Member update**: {} | {}#{}".format(member_after.mention, self.bot.escape_name(member_after.name), member_after.discriminator) + msg
            await self.bot.send_message(dest, msg)

def setup(bot):
    bot.add_cog(Logs(bot))
