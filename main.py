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

# القائمة الدقيقة حسب طلبك
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

class ColorPagination(discord.ui.View):
    def __init__(self, page=0):
        super().__init__(timeout=None)
        self.page = page
        self.create_buttons()

    def create_buttons(self):
        self.clear_items()
        start = (self.page * 10) + 1
        end = start + 10
        for i in range(start, end):
            name, color = COLOR_DATA[i]
            btn = discord.ui.Button(label=f"{i}. {name}", style=discord.ButtonStyle.secondary, custom_id=f"c{i}")
            btn.callback = self.make_callback(name, color)
            self.add_item(btn)
        self.add_item(discord.ui.Button(label="⬅️", style=discord.ButtonStyle.primary, custom_id="prev", row=4))
        self.add_item(discord.ui.Button(label="❌ إزالة الألوان", style=discord.ButtonStyle.danger, custom_id="remove", row=4))
        self.add_item(discord.ui.Button(label="➡️", style=discord.ButtonStyle.primary, custom_id="next", row=4))

    def make_callback(self, name, color_hex):
        async def callback(interaction: discord.Interaction):
            try:
                # حذف الرتب القديمة قبل الإضافة
                for r in interaction.user.roles:
                    if r.name in [COLOR_DATA[i][0] for i in range(1, 51)]:
                        await interaction.user.remove_roles(r)
                # إضافة الرتبة
                role = discord.utils.get(interaction.guild.roles, name=name)
                if not role:
                    role = await interaction.guild.create_role(name=name, color=discord.Color(color_hex))
                await interaction.user.add_roles(role)
                await interaction.response.send_message(f"✅ تم تفعيل {name}!", ephemeral=True)
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
                if r.name in [COLOR_DATA[i][0] for i in range(1, 51)]:
                    await interaction.user.remove_roles(r)
            await interaction.response.send_message("❌ تمت إزالة الألوان!", ephemeral=True)
            await asyncio.sleep(4)
            await interaction.delete_original_response()
            return True
        self.create_buttons()
        await interaction.response.edit_message(view=self)
        return True

@bot.event
async def on_ready():
    print(f'البوت {bot.user} جاهز تماماً!')

@bot.command()
async def لوحة(ctx):
    await ctx.send("👑 **نظام ألوان YONAN (50 لوناً):**", view=ColorPagination())

bot.run(TOKEN)
