import json
import asyncio
import discord
from discord.ext import commands
from discord import ButtonStyle, Embed
from discord.ui import Button, View, Modal, TextInput
import google.generativeai as genai

def load_db():
    try:
        with open("db/Ai.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_db(db):
    with open("db/Ai.json", "w") as f:
        json.dump(db, f, indent=4)


class AISetupModal(Modal):
    def __init__(self, cog):
        super().__init__(title="Ai Setup")
        self.cog = cog
        self.add_item(TextInput(label="Channel ID", placeholder="Enter channel ID"))

    async def on_submit(self, interaction: discord.Interaction):
        channel_id = int(self.children[0].value)
        guild_id = str(interaction.guild.id)
        self.cog.ai_channels[guild_id] = channel_id
        save_db(self.cog.ai_channels)
        channel = interaction.guild.get_channel(channel_id)
        await interaction.response.send_message(f"✅ Ai has been set up in {channel.mention}")

class SetupView(View):
    def __init__(self, cog):
        super().__init__()
        self.cog = cog

    @discord.ui.button(label="Ai Setup", style=ButtonStyle.green)
    async def ai_setup(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(AISetupModal(self.cog))

    @discord.ui.button(label="Ai Delete", style=ButtonStyle.red)
    async def ai_delete(self, interaction: discord.Interaction, button: Button):
        guild_id = str(interaction.guild.id)
        if guild_id in self.cog.ai_channels:
            del self.cog.ai_channels[guild_id]
            save_db(self.cog.ai_channels)
            await interaction.response.send_message("✅ Disabled Ai for this server.")
        else:
            await interaction.response.send_message("❌ Ai is not setup in this server.")

    @discord.ui.button(label="Ai Config", style=ButtonStyle.blurple)
    async def ai_config(self, interaction: discord.Interaction, button: Button):
        guild_id = str(interaction.guild.id)
        if guild_id in self.cog.ai_channels:
            channel = interaction.guild.get_channel(self.cog.ai_channels[guild_id])
            await interaction.response.send_message(f"Ai chat is enabled in {channel.mention}")
        else:
            await interaction.response.send_message("❌ Ai is not setup in this server.")

class GeminiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ai_channels = load_db()
        self.setup_gemini()

    def setup_gemini(self):
        genai.configure(api_key="API_KEY")
        self.model = genai.GenerativeModel('gemini-pro')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        guild_id = str(message.guild.id)
        if guild_id in self.ai_channels and message.channel.id == self.ai_channels[guild_id]:
            async with message.channel.typing():
                try:
                    response = await asyncio.to_thread(self.model.generate_content, message.content)
                    await message.reply(response.text)
                except Exception as e:
                    await message.channel.send(f"**An error occurred:** {str(e)}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ai(self, ctx):
        await ctx.send(f"Setup Ai Chat for this server!", view=SetupView(self))

async def setup(bot):
    await bot.add_cog(GeminiCog(bot))
