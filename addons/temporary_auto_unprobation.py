import discord
from discord.ext import commands
import sys
import asyncio
import traceback
from contextlib import suppress

class Periodic:
    def __init__(self, time, func):
        self.func = func
        self.time = time
        self.is_started = False
        self._task = None

    async def start(self):
        if not self.is_started:
            self.is_started = True
            # Start task to call func periodically:
            self._task = asyncio.ensure_future(self._run())

    async def stop(self):
        if self.is_started:
            self.is_started = False
            # Stop task and await it stopped:
            self._task.cancel()
            with suppress(asyncio.CancelledError):
                await self._task

    async def _run(self):
        while True:
            try:
                await self.func()
            except:
                ty, error, trace = sys.exc_info()
                traceback.print_exception(ty, error, trace, file=sys.stderr)
            await asyncio.sleep(self.time)

class TemporaryAutoUnprobation:
    def __init__(self, bot):
        self.bot = bot
        self.timer = None
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    async def on_ready(self):
        if self.timer == None:
            # Add group to 5 member every minute
            self.timer = Periodic(60, self._add_some_members)
            await self.timer.start()

    async def _add_some_members(self):
        # We assume that 5 user every minute is fine

        users_to_fix = 5
        msg = "Fixing the roles for {} more users".format(users_to_fix)
        await self.bot.send_message(self.bot.serverlogs_channel, msg)
        i = 0
        to_process = 0
        for member in self.bot.get_all_members():
            if not self.bot.probation_role in member.roles and not self.bot.unprobated_role in member.roles:
                if i < users_to_fix:
                    await self.bot.add_roles(member, self.bot.unprobated_role)
                    i += 1
                else:
                    to_process += 1

        if to_process == 0:
            msg = "✅ All users have been processed, we are ready to move on to phase 2"
            await self.bot.send_message(self.bot.serverlogs_channel, msg)
            await self.timer.stop()
        else:
            msg = "ℹ️ We have {} users left to handle".format(to_process)
            await self.bot.send_message(self.bot.serverlogs_channel, msg)


def setup(bot):
    bot.add_cog(TemporaryAutoUnprobation(bot))
