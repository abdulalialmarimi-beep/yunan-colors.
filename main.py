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

# القائمة الاحترافية
COLOR_DATA = {
    1: ("أحمر صارخ", 0xFF0000), 2: ("أحمر برتقالي", 0xFF4500), 3: ("برتقالي أحمر", 0xFF6347), 4: ("برتقالي", 0xFFA500), 5: ("برتقالي ذهبي", 0xFF8C00),
    6: ("ذهبي", 0xFFD700), 7: ("أصفر ذهبي", 0xFFD700), 8: ("أصفر", 0xFFFF00), 9: ("أصفر مخضر", 0xADFF2F), 10: ("أخضر مصفر", 0xBDFF00),
    11: ("أخضر فاتح", 0x7FFF00), 12: ("أخضر عشبي", 0x32CD32), 13: ("أخضر", 0x228B22), 14: ("أخضر غامق", 0x006400), 15: ("أخضر زمردي", 0x50C878),
    16: ("أخضر بحري", 0x2E8B57), 17: ("أخضر مائي", 0x48D1CC), 18: ("سماوي", 0x00CED1), 19: ("سماوي فاتح", 0x87CEEB), 20: ("أزرق سماوي", 0x87CEFA),
    21: ("أزرق فاتح", 0xADD8E6), 22: ("أزرق", 0x0000FF), 23: ("أزرق ملكي", 0x4169E1), 24: ("أزرق نيلي", 0x4B0082), 25: ("نيلي", 0x6A5ACD),
    26: ("أزرق بنفسجي", 0x8A2BE2), 27: ("بنفسجي مزرق", 0x9370DB), 28: ("بنفسجي فاتح", 0xDA70D6), 29: ("بنفسجي", 0x800080), 30: ("بنفسجي غامق", 0x4B0082),
    31: ("أرجواني", 0x9932CC), 32: ("أرجواني فاتح", 0xBA55D3), 33: ("وردي بنفسجي", 0xFF00FF), 34: ("وردي غامق", 0xC71585), 35: ("وردي", 0xFFC0CB),
    36: ("وردي فاتح", 0xFFB6C1), 37: ("وردي زاهي", 0xFF69B4), 38: ("وردي مائل للأحمر", 0xDB7093), 39: ("أحمر وردي", 0xE91E63), 40: ("أحمر فاتح", 0xFF5C5C),
    41: ("مرجاني", 0xFF7F50), 42: ("خوخي", 0xFFDAB9), 43: ("رملي", 0xDEB887), 44: ("كريمي", 0xFFFDD0), 45: ("بيج", 0xF5F5DC),
    46: ("رمادي فاتح", 0xD3D3D3), 47: ("رمادي مزرق", 0x708090), 48: ("رمادي أرجواني", 0x9370DB), 49: ("رمادي غامق", 0x36393F), 50: ("أسود مخملي", 0x2C2F33)
}

active_users = set()

class ColorView(discord.ui.View):
    def __init__(self, page=0, user_id=None):
        super().__init__(timeout=900)
        self.page = page
        self.user_id = user_id
        self.update_buttons()

    def update_buttons(self):
        self.clear_items()
        start = (self.page * 10) + 1
        for i in range(start, start + 10):
            btn = discord.ui.Button(label=f"{i}", style=discord.ButtonStyle.secondary, custom_id=f"c{i}")
            btn.callback = self.make_callback(i)
            self.add_item(btn)
        self.add_item(discord.ui.Button(label="⬅️", style=discord.ButtonStyle.primary, custom_id="prev", row=4))
        self.add_item(discord.ui.Button(label="❌ إزالة", style=discord.ButtonStyle.danger, custom_id="remove", row=4))
        self.add_item(discord.ui.Button(label="➡️", style=discord.ButtonStyle.primary, custom_id="next", row=4))

    def make_callback(self, i):
        async def callback(interaction: discord.Interaction):
            await interaction.response.defer(ephemeral=True)
            name, color = COLOR_DATA[i]
            role = discord.utils.get(interaction.guild.roles, name=name)
            if not role: role = await interaction.guild.create_role(name=name, color=discord.Color(color))
            
            for n in range(1, 51):
                old_role = discord.utils.get(interaction.guild.roles, name=COLOR_DATA[n][0])
                if old_role in interaction.user.roles: await interaction.user.remove_roles(old_role)
            
            await interaction.user.add_roles(role)
            await interaction.followup.send(f"✅ تم تفعيل: {name}", ephemeral=True)
        return callback

    async def on_timeout(self):
        if self.user_id in active_users: active_users.remove(self.user_id)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id: return False
        cid = interaction.data.get("custom_id")
        if cid == "prev": self.page = max(0, self.page - 1)
        elif cid == "next": self.page = min(4, self.page + 1)
        elif cid == "remove":
            await interaction.response.defer(ephemeral=True)
            for n in range(1, 51):
                old_role = discord.utils.get(interaction.guild.roles, name=COLOR_DATA[n][0])
                if old_role in interaction.user.roles: await interaction.user.remove_roles(old_role)
            await interaction.followup.send("❌ تمت إزالة الألوان", ephemeral=True)
            return True
        await interaction.response.edit_message(view=self)
        return True

@bot.command()
@commands.has_permissions(administrator=True)
async def ارسال_اللوحة(ctx):
    class OpenView(discord.ui.View):
        @discord.ui.button(label="👑 افتح لوحة ألوانك الخاصة", style=discord.ButtonStyle.green)
        async def open(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer(ephemeral=True)
            if interaction.user.id in active_users:
                await interaction.followup.send("⚠️ أنت بالفعل قمت بفتح لوحتك!", ephemeral=True)
                return
            active_users.add(interaction.user.id)
            await interaction.followup.send("اختر رقم لونك:", view=ColorView(user_id=interaction.user.id), ephemeral=True)

    await ctx.send(embed=discord.Embed(title="👑 نظام ألوان YONAN"), view=OpenView())

bot.run(TOKEN)
bot.run(TOKEN)
