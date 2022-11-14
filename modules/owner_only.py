import discord, os
from discord.ext import commands
from aio_pika import Message, connect

class mod_cmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name = "reload"
    )
    async def reload(self, ctx, cmd):
        if ctx.author.id not in self.bot.owner_ids:
            return await ctx.reply(
                embed = discord.Embed(
                    description=":no_entry: You do not have permission to use this command!", 
                    color=discord.Color.brand_red()
                ))
            
        found = False
        for path, subdirs, files in os.walk("modules"):
            for name in files:
                if name.endswith(".py") and name[:-3] == cmd:
                    name = os.path.join(name)[:-3]
                    path = (os.path.join(path).replace("/", ".")).replace("\\", ".")
                    filepath = path + "." + name
                    try:
                        await self.bot.reload_extension(filepath)
                        await ctx.send("Reloaded: `" + filepath + "`")
                        found = True
                    except:
                        await self.bot.load_extension(filepath)
                        await ctx.send("Loaded: `" + filepath + "`")
                        found = True
                else:
                    continue

        if not found:
            return await ctx.send(
                "Extension `" + cmd + "` was not found!"
            )
        
        
async def setup(bot):
    await bot.add_cog(mod_cmds(bot))