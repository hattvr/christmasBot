import traceback, discord
from discord.ui import *
from discord import app_commands
from discord.ext import commands
from aio_pika import Message, connect

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name = "ping"
    )
    async def ping(self, ctx: commands.Context):
        return await ctx.send(
            f"Pong! {round(self.bot.latency * 1000)}ms"
        )
        
    @commands.hybrid_command(
        name = "prepare-gift",
        description = "Prepare a gift for users to open!"
    )
    async def preparegift(self, ctx: commands.Context):
        await ctx.typing()
        
        embed = discord.Embed(
            title = "Christmas Gift Giving!",
            description = f"""
**Hide gifts in both Genshin Wizard and Celestia for members to find!**

You'll be able to use the </open-gift:{self.bot.application_commands['ping']}> command in both servers to search for presents.

Collect presents to exchange for prizes at our **Christmas Shop**!
            """,
            color = discord.Color.brand_green()
        )
        
        return await ctx.reply(
            embed = embed,
            view = PreparationView(ctx)
        )

class PreparationView(View):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.bot = ctx.bot

    @button(label = "Prepare a Gift", style = discord.ButtonStyle.blurple)
    async def prepare(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(PreperationModal())
        
    @button(label = "How to Participate", style = discord.ButtonStyle.gray)
    async def instructions(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()
        
        embed = discord.Embed(
            description = "Instructions on how to participate in the event!",
            color = discord.Color.brand_green()
        )
        
        return await interaction.followup.send(
            embed = embed,
            ephemeral = True
        )
        
class PreperationModal(Modal, title = "Prepare a Gift"):
    channel = TextInput(
        label = "Channel ID", 
        style = discord.TextStyle.short,
        placeholder = "Enter the channel ID to send the gift to",
        required = True,
        min_length = 18, 
        max_length = 19
    )
    
    code_word = TextInput(
        label = "Code Word",
        placeholder = "Enter a code word for the gift",
        required = True,
        style = discord.TextStyle.short
    )
    
    channel_hint = TextInput(
        label = "Channel Hint",
        style = discord.TextStyle.short,
        required = True,
        placeholder = "Enter a hint for the channel"
    )
    
    code_word_hint = TextInput(
        label = "Code Word Hint",
        style = discord.TextStyle.short,
        required = True,
        placeholder = "Enter a hint for the code word"
    )
    
    image_url = TextInput(
        label = "Image URL",
        placeholder = "Enter the image URL for the gift",
        required = False,
        style = discord.TextStyle.short,
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        embed = discord.Embed(
            title = "Present Prepared Request!",
            color = discord.Color.gold()
        )
        
        embed.add_field(name = "Channel ID", value = f"<#{self.channel.value}>", inline = False)
        embed.add_field(name = "Code Word", value = self.code_word.value, inline = False)
        embed.add_field(name = "Channel Hint", value = self.channel_hint.value, inline = False)
        embed.add_field(name = "Code Word Hint", value = self.code_word_hint.value, inline = False)
        embed.add_field(name = "Image URL", value = self.image_url.value, inline = False)
        
        try:
            embed.set_thumbnail(url = self.image_url.value)
        
            await interaction.followup.send(
                embed = embed
            )
        except:
            await interaction.followup.send(
                embed = discord.Embed(
                    description = f"```{traceback.format_exc()}```", 
                    color = discord.Color.brand_red()
                    )
                )
            
        return



async def setup(bot):
    await bot.add_cog(Commands(bot))
