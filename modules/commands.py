import asyncio, discord, pickle
from discord.ext import commands
from aio_pika import Message, connect

class mod_cmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name = "ping")
    async def ping(self, ctx: commands.Context):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")
        
async def setup(bot):
    await bot.add_cog(mod_cmds(bot))
