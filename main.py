import os
import discord
from discord.ext import commands
import json

from myserver import server_on

# โหลด config
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# คำสั่งให้บอทโพสต์ Embed + ปุ่ม
@bot.command()
@commands.has_permissions(administrator=True)
async def postrole(ctx):
    embed = discord.Embed(
        title="💥 90s Fivem 🔥",
        description=(
            "✨ กดปุ่มด้านล่างเพื่อรับยศกันเลย! ✨\n\n"
            "🔸 อย่าลืมอ่านกฎก่อนเล่นกันด้วยนะ\n"
            "🔸 อย่าทำผิดกฎเชิฟเวอร์นะคั้บ"
        ),
        color=0xFF0000
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/1123278234067419206/1422090033430663190/LOGO_90s.png?ex=68e2a84d&is=68e156cd&hm=ce4d8886632c2d4b693eb482a610e361b2c34c85f0694ac14408b41863df802a&")
    embed.set_footer(text="กดปุ่มด้านล่างเพื่อรับยศกันเลย! 🔥")

    view = discord.ui.View()
    button = discord.ui.Button(
        label="💚 กดปุ่มนี้เพื่อรับยศ",
        style=discord.ButtonStyle.success,
        custom_id="get_role"
    )
    view.add_item(button)

    await ctx.send(embed=embed, view=view)

# Event เมื่อกดปุ่ม
@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.data.get("custom_id") == "get_role":
        guild = interaction.guild
        member = interaction.user
        role = guild.get_role(int(config["role_id"]))

        if not role:
            return await interaction.response.send_message("❌ ไม่พบบทบาทที่ตั้งค่าไว้", ephemeral=True)

        if role in member.roles:
            return await interaction.response.send_message("⚠️ คุณมีบทบาทนี้อยู่แล้ว!", ephemeral=True)

        await member.add_roles(role)
        await interaction.response.send_message(f"✅ ให้บทบาท **{role.name}** เรียบร้อยแล้ว!", ephemeral=True)


server_on()       

# bot.run(config["token"])
bot.run(os.gtenv(config["token"]))
