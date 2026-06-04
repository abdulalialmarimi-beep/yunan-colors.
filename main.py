import os
import discord
import asyncio
from discord.ext import commands
from flask import Flask
from threading import Thread

# تشغيل البوت 24/7
app = Flask('')
@app.route('/')
def home(): return "البوت يعمل!"
Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()

TOKEN = os.environ.get("TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="#", intents=intents)

# قاموس الألوان (تأكد أن أسماء الرتب في سيرفرك تطابق هذه تماماً)
# إذا أردت تسميتهم "لون 1", "لون 2" بدل الأسماء الطويلة، عدلها هنا
COLOR_DATA = {i: (f"لون {i}", 0x000000) for i in range(1, 51)}

class ColorView(discord.ui.View):
    def __init__(self, page=0):
        super().__init__(timeout=None)
        self.page = page
        self.update_buttons()

    def update_buttons(self):
        self.clear_items()
        start = (self.page * 10) + 1
        for i in range(start, start + 10):
            btn = discord.ui.Button(label=str(i), style=discord.ButtonStyle.secondary, custom_id=f"color_{i}")
            btn.callback = self.make_callback(i)
            self.add_item(btn)
        self.add_item(discord.ui.Button(label="⬅️", style=discord.ButtonStyle.primary, custom_id="prev", row=4))
        self.add_item(discord.ui.Button(label="❌ إزالة", style=discord.ButtonStyle.danger, custom_id="remove", row=4))
        self.add_item(discord.ui.Button(label="➡️", style=discord.ButtonStyle.primary, custom_id="next", row=4))

    def make_callback(self, i):
        async def callback(interaction: discord.Interaction):
            role_name = COLOR_DATA[i][0]
            role = discord.utils.get(interaction.guild.roles, name=role_name)
            if not role:
                await interaction.response.send_message(f"❌ الرتبة '{role_name}' غير موجودة، قم بإنشائها أولاً!", ephemeral=True)
                return
            
            # إزالة الألوان القديمة للعضو
            for n in range(1, 51):
                old_role = discord.utils.get(interaction.guild.roles, name=COLOR_DATA[n][0])
                if old_role in interaction.user.roles:
                    await interaction.user.remove_roles(old_role)
            
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"✅ تم تفعيل اللون: {role_name}", ephemeral=True)
        return callback

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        cid = interaction.data.get("custom_id")
        if cid == "prev": self.page = max(0, self.page - 1)
        elif cid == "next": self.page = min(4, self.page + 1)
        elif cid == "remove":
            for n in range(1, 51):
                old_role = discord.utils.get(interaction.guild.roles, name=COLOR_DATA[n][0])
                if old_role in interaction.user.roles: await interaction.user.remove_roles(old_role)
            await interaction.response.send_message("❌ تمت إزالة جميع الألوان", ephemeral=True)
            return True
        self.update_buttons()
        await interaction.response.edit_message(view=self)
        return True

@bot.command()
@commands.has_permissions(administrator=True)
async def ارسال_اللوحة(ctx):
    embed = discord.Embed(title="👑 نظام ألوان YONAN", description="اضغط على الرقم لاختيار لونك!")
    await ctx.send(embed=embed, view=ColorView())

bot.run(TOKEN)
