import os
import discord
import asyncio
from discord.ext import commands
from flask import Flask
from threading import Thread

# تشغيل السيرفر 24/7
app = Flask('')
@app.route('/')
def home(): return "البوت يعمل!"
Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()

TOKEN = os.environ.get("TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="#", intents=intents)

# جدول الـ 50 لون الثابت
COLOR_DATA = {
    1: ("أحمر صارخ", 0xFF0000), 2: ("أحمر برتقالي", 0xFF4500), 3: ("برتقالي", 0xFFA500), 4: ("ذهبي", 0xFFD700), 5: ("أصفر", 0xFFFF00),
    6: ("أخضر فاتح", 0x7FFF00), 7: ("أخضر عشبي", 0x32CD32), 8: ("أخضر", 0x228B22), 9: ("أخضر غامق", 0x006400), 10: ("أخضر بحري", 0x2E8B57),
    11: ("مائي", 0x48D1CC), 12: ("سماوي", 0x00CED1), 13: ("أزرق فاتح", 0x87CEEB), 14: ("أزرق", 0x0000FF), 15: ("أزرق ملكي", 0x4169E1),
    16: ("نيلي", 0x4B0082), 17: ("بنفسجي", 0x800080), 18: ("أرجواني", 0x9932CC), 19: ("وردي", 0xFFC0CB), 20: ("وردي زاهي", 0xFF69B4),
    21: ("مرجاني", 0xFF7F50), 22: ("خوخي", 0xFFDAB9), 23: ("كريمي", 0xFFFDD0), 24: ("بيج", 0xF5F5DC), 25: ("رمادي", 0x808080),
    26: ("أسود", 0x000000), 27: ("أبيض", 0xFFFFFF), 28: ("فضي", 0xC0C0C0), 29: ("نحاسي", 0xB87333), 30: ("تركواز", 0x40E0D0),
    31: ("عنابي", 0x800020), 32: ("زيتوني", 0x808000), 33: ("ليموني", 0xCCFF00), 34: ("بني", 0xA52A2A), 35: ("بنفسجي فاتح", 0xE6E6FA),
    36: ("أزرق غامق", 0x00008B), 37: ("أحمر وردي", 0xE91E63), 38: ("أصفر فاتح", 0xFFFFE0), 39: ("أخضر ليموني", 0x32CD32), 40: ("أخضر مائي غامق", 0x008080),
    41: ("أزرق سماوي", 0x87CEFA), 42: ("بنفسجي غامق", 0x4B0082), 43: ("خوخي غامق", 0xFFB347), 44: ("وردي غامق", 0xC71585), 45: ("رمادي غامق", 0x36393F),
    46: ("برتقالي محروق", 0xCC5500), 47: ("بنفسجي زاهي", 0x9370DB), 48: ("أحمر فاتح", 0xFF5C5C), 49: ("ذهبي داكن", 0xB8860B), 50: ("أسود مخملي", 0x2C2F33)
}

active_users = {}

class ColorView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=900)
        self.user_id = user_id
        self.page = 0
        self.update_buttons()

    def update_buttons(self):
        self.clear_items()
        start = (self.page * 10) + 1
        for i in range(start, start + 10):
            if i > 50: break
            btn = discord.ui.Button(label=str(i), style=discord.ButtonStyle.secondary, custom_id=f"color_{i}")
            btn.callback = self.make_callback(i)
            self.add_item(btn)
        self.add_item(discord.ui.Button(label="⬅️", style=discord.ButtonStyle.primary, custom_id="prev", row=4))
        self.add_item(discord.ui.Button(label="❌ إزالة", style=discord.ButtonStyle.danger, custom_id="remove", row=4))
        self.add_item(discord.ui.Button(label="➡️", style=discord.ButtonStyle.primary, custom_id="next", row=4))

    def make_callback(self, i):
        async def callback(interaction: discord.Interaction):
            await interaction.response.defer(ephemeral=True)
            name, color_hex = COLOR_DATA[i]
            role = discord.utils.get(interaction.guild.roles, name=name)
            if not role: role = await interaction.guild.create_role(name=name, color=discord.Color(color_hex))
            for n in COLOR_DATA:
                old_role = discord.utils.get(interaction.guild.roles, name=COLOR_DATA[n][0])
                if old_role in interaction.user.roles: await interaction.user.remove_roles(old_role)
            await interaction.user.add_roles(role)
            await interaction.followup.send(f"✅ تم تفعيل: {name}", ephemeral=True, delete_after=3)
        return callback

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id: return False
        cid = interaction.data["custom_id"]
        if cid == "prev": self.page = max(0, self.page - 1)
        elif cid == "next": self.page = min(4, self.page + 1)
        elif cid == "remove":
            await interaction.response.defer(ephemeral=True)
            for n in COLOR_DATA:
                old_role = discord.utils.get(interaction.guild.roles, name=COLOR_DATA[n][0])
                if old_role in interaction.user.roles: await interaction.user.remove_roles(old_role)
            await interaction.followup.send("❌ تمت إزالة الألوان", ephemeral=True, delete_after=3)
            return True
        self.update_buttons()
        await interaction.response.edit_message(view=self)
        return True

@bot.command()
async def ارسال_اللوحة(ctx):
    class OpenView(discord.ui.View):
        @discord.ui.button(label="👑 افتح لوحة ألوانك", style=discord.ButtonStyle.green)
        async def open(self, interaction: discord.Interaction, button: discord.ui.Button):
            active_users[interaction.user.id] = True
            await interaction.response.send_message("اختر رقم لونك (اللوحة تغلق بعد 15 دقيقة):", view=ColorView(user_id=interaction.user.id), ephemeral=True)
    await ctx.send("نظام YONAN للألوان:", view=OpenView())

bot.run(TOKEN)

bot.run(TOKEN)
