import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home(): return "البوت يعمل!"
Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()

TOKEN = os.environ.get("TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="#", intents=intents)

COLORS = {i: f"Color {i}" for i in range(1, 51)}

async def set_role(interaction, i):
    name = COLORS[i]
    role = discord.utils.get(interaction.guild.roles, name=name)
    if not role: role = await interaction.guild.create_role(name=name)
    for n in COLORS.values():
        old = discord.utils.get(interaction.guild.roles, name=n)
        if old and old in interaction.user.roles: await interaction.user.remove_roles(old)
    await interaction.user.add_roles(role)
    await interaction.response.send_message(f"✅ تم تفعيل اللون {i}", ephemeral=True, delete_after=2)

class ColorView(discord.ui.View):
    def __init__(self, start, end):
        super().__init__(timeout=None)
        for i in range(start, end + 1):
            btn = discord.ui.Button(label=str(i), style=discord.ButtonStyle.secondary, custom_id=f"color_{i}")
            btn.callback = lambda inter, i=i: set_role(inter, i)
            self.add_item(btn)
        rem = discord.ui.Button(label="❌ إزالة", style=discord.ButtonStyle.danger, custom_id=f"remove_{start}")
        rem.callback = self.remove_all
        self.add_item(rem)

    async def remove_all(self, inter):
        for name in COLORS.values():
            r = discord.utils.get(inter.guild.roles, name=name)
            if r and r in inter.user.roles: await inter.user.remove_roles(r)
        await inter.response.send_message("❌ تمت إزالة اللون", ephemeral=True, delete_after=2)

@bot.command()
async def ارسال_اللوحة(ctx):
    await ctx.send("👑 **لوحة الألوان (1-25):**", view=ColorView(1, 25))

@bot.command()
async def لوحة(ctx):
    await ctx.send("👑 **لوحة الألوان (26-50):**", view=ColorView(26, 50))

bot.run(TOKEN)

