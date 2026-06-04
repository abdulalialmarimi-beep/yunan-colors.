import os
import discord
import asyncio
from discord.ext import commands
from flask import Flask
from threading import Thread

# --- جزء التنشيط 24 ساعة ---
app = Flask('')
@app.route('/')
def home():
    return "البوت يعمل بكفاءة!"

def run():
    app.run(host='0.0.0.0', port=8080)

t = Thread(target=run)
t.start()
# -------------------------

TOKEN = os.environ.get("TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="#", intents=intents)

# قائمة الألوان المحدثة حسب طلبك
COLOR_NAMES = [
    "أحمر صارخ", "أحمر برتقالي", "برتقالي أحمر", "برتقالي", "برتقالي ذهبي", "ذهبي", "أصفر ذهبي", "أصفر", "أصفر مخضر", "أخضر مصفر",
    "أخضر فاتح", "أخضر عشبي", "أخضر", "أخضر غامق", "أخضر زمردي", "أخضر بحري", "أخضر مائي", "سماوي", "سماوي فاتح", "أزرق سماوي",
    "أزرق فاتح", "أزرق", "أزرق ملكي", "أزرق نيلي", "نيلي", "أزرق بنفسجي", "بنفسجي مزرق", "بنفسجي فاتح", "بنفسجي", "بنفسجي غامق",
    "أرجواني", "أرجواني فاتح", "وردي بنفسجي", "وردي غامق", "وردي", "وردي فاتح", "وردي زاهي", "وردي مائل للأحمر", "أحمر وردي", "أحمر فاتح",
    "مرجاني", "خوخي", "رملي", "كريمي", "بيج", "رمادي فاتح", "رمادي مزرق", "رمادي أرجواني", "رمادي غامق", "أسود مخملي"
]

# تم استخدام ألوان تقريبية تليق بكل اسم
COLOR_VALUES = [
    0xFF0000, 0xFF4500, 0xFF6347, 0xFFA500, 0xFFD700, 0xDAA520, 0xFFD700, 0xFFFF00, 0xADFF2F, 0x9ACD32,
    0x90EE90, 0x7CFC00, 0x008000, 0x006400, 0x50C878, 0x2E8B57, 0x008080, 0x00CED1, 0x87CEEB, 0x00BFFF,
    0xADD8E6, 0x0000FF, 0x4169E1, 0x4B0082, 0x4B0082, 0x8A2BE2, 0x9370DB, 0xDA70D6, 0x800080, 0x4B0082,
    0x9932CC, 0xBA55D3, 0xFF00FF, 0xC71585, 0xFFC0CB, 0xFFB6C1, 0xFF69B4, 0xDB7093, 0xFF1493, 0xFF7F50,
    0xFF7F50, 0xFFDAB9, 0xF4A460, 0xFFFDD0, 0xF5F5DC, 0xD3D3D3, 0x708090, 0x778899, 0x2F4F4F, 0x000000
]

class ColorPagination(discord.ui.View):
    def __init__(self, page=0):
        super().__init__(timeout=None)
        self.page = page
        self.create_buttons()

    def create_buttons(self):
        self.clear_items()
        start = self.page * 10
        end = min(start + 10, 50)
        for i in range(start, end):
            num = i + 1
            btn = discord.ui.Button(label=f"{num}. {COLOR_NAMES[i]}", style=discord.ButtonStyle.secondary, custom_id=f"c{num}")
            btn.callback = self.make_callback(i)
            self.add_item(btn)
        
        self.add_item(discord.ui.Button(label="⬅️", style=discord.ButtonStyle.primary, custom_id="prev", row=4))
        self.add_item(discord.ui.Button(label="إزالة الألوان", style=discord.ButtonStyle.danger, custom_id="remove", row=4))
        self.add_item(discord.ui.Button(label="➡️", style=discord.ButtonStyle.primary, custom_id="next", row=4))

    def make_callback(self, index):
        async def callback(interaction: discord.Interaction):
            try:
                role_name = COLOR_NAMES[index]
                role = discord.utils.get(interaction.guild.roles, name=role_name)
                if not role:
                    role = await interaction.guild.create_role(name=role_name, color=discord.Color(COLOR_VALUES[index]))
                
                for r in interaction.user.roles:
                    if r.name in COLOR_NAMES: await interaction.user.remove_roles(r)
                
                await interaction.user.add_roles(role)
                await interaction.response.send_message(f"✅ تم تفعيل {role_name}!", ephemeral=True)
                await asyncio.sleep(4)
                await interaction.delete_original_response()
            except Exception as e:
                print(f"خطأ: {e}")
        return callback

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        cid = interaction.data.get("custom_id")
        if cid == "prev": self.page = max(0, self.page - 1)
        elif cid == "next": self.page = min(4, self.page + 1)
        elif cid == "remove":
            for r in interaction.user.roles:
                if r.name in COLOR_NAMES: await interaction.user.remove_roles(r)
            await interaction.response.send_message("❌ تم إزالة اللون!", ephemeral=True)
            await asyncio.sleep(4)
            await interaction.delete_original_response()
            return True
        self.create_buttons()
        await interaction.response.edit_message(view=self)
        return True

@bot.command()
async def لوحة(ctx):
    await ctx.send("👑 **نظام ألوان YONAN (50 لوناً) - اختر لونك المفضل:**", view=ColorPagination())

bot.run(TOKEN)
