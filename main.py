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

# القائمة (تظهر في رسالة الشرح فقط)
COLORS = {
    i: f"لون {i}" for i in range(1, 51)
}

async def set_role(interaction, i):
    name = COLORS[i]
    role = discord.utils.get(interaction.guild.roles, name=name)
    if not role: role = await interaction.guild.create_role(name=name)
    for n in COLORS.values():
        old = discord.utils.get(interaction.guild.roles, name=n)
        if old in interaction.user.roles: await interaction.user.remove_roles(old)
    await interaction.user.add_roles(role)
    await interaction.response.send_message(f"✅ {name}", ephemeral=True, delete_after=3)

class ColorView(discord.ui.View):
    def __init__(self, start, end, is_last=False):
        super().__init__(timeout=None)
        for i in range(start, end + 1):
            btn = discord.ui.Button(label=str(i), style=discord.ButtonStyle.secondary, custom_id=f"c{i}")
            btn.callback = lambda inter, i=i: set_role(inter, i)
            self.add_item(btn)
        if is_last:
            rem = discord.ui.Button(label="❌ إزالة", style=discord.ButtonStyle.danger, custom_id="rem")
            rem.callback = self.remove_all
            self.add_item(rem)

    async def remove_all(self, inter):
        for name in COLORS.values():
            r = discord.utils.get(inter.guild.roles, name=name)
            if r in inter.user.roles: await inter.user.remove_roles(r)
        await inter.response.send_message("❌", ephemeral=True, delete_after=3)

@bot.command()
async def ارسال_اللوحة(ctx):
    class Open(discord.ui.View):
        @discord.ui.button(label="👑 افتح اللوحة", style=discord.ButtonStyle.green)
        async def click(self, inter, btn):
            await inter.response.send_message(view=ColorView(1, 25), ephemeral=False)
            await inter.followup.send(view=ColorView(26, 50, is_last=True), ephemeral=False)
    await ctx.send("نظام الألوان:", view=Open())

bot.run(TOKEN)
