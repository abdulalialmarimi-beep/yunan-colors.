import os
import discord
from discord.ext import commands

# ضع التوكن الخاص بك هنا إذا لم تكن تستخدم Environment Variables
TOKEN = "ضع_التوكن_هنا" 
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="#", intents=intents)

COLORS = {i: f"Color {i}" for i in range(1, 51)}

async def set_role(interaction, i):
    role = discord.utils.get(interaction.guild.roles, name=COLORS[i])
    if not role: role = await interaction.guild.create_role(name=COLORS[i])
    for n in COLORS.values():
        old = discord.utils.get(interaction.guild.roles, name=n)
        if old in interaction.user.roles: await interaction.user.remove_roles(old)
    await interaction.user.add_roles(role)
    await interaction.response.send_message(f"✅ تم تفعيل اللون {i}", ephemeral=True)

class ColorView(discord.ui.View):
    def __init__(self, start, end):
        super().__init__(timeout=None)
        for i in range(start, end + 1):
            btn = discord.ui.Button(label=str(i), style=discord.ButtonStyle.secondary, custom_id=f"color_{i}")
            btn.callback = lambda inter, i=i: set_role(inter, i)
            self.add_item(btn)
        rem = discord.ui.Button(label="❌ إزالة", style=discord.ButtonStyle.danger, custom_id=f"rem_{start}")
        rem.callback = self.remove_all
        self.add_item(rem)

    async def remove_all(self, inter):
        for name in COLORS.values():
            r = discord.utils.get(inter.guild.roles, name=name)
            if r in inter.user.roles: await inter.user.remove_roles(r)
        await inter.response.send_message("❌ تمت الإزالة", ephemeral=True)

@bot.event
async def on_ready():
    print(f'البوت جاهز: {bot.user}')

@bot.command()
async def send_colors(ctx):
    # هذا الأمر سيرسل اللوحتين دفعة واحدة
    await ctx.send("👑 **لوحة (1-25):**", view=ColorView(1, 25))
    await ctx.send("👑 **لوحة (26-50):**", view=ColorView(26, 50))

bot.run(TOKEN)
