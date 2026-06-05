import os
import asyncio
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# ─── سيرفر Flask لإبقاء البوت حياً ───────────────────────────────────────────
app = Flask('')

@app.route('/')
def home():
    return "البوت يعمل! ✅"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run_flask, daemon=True).start()

# ─── إعدادات البوت ────────────────────────────────────────────────────────────
TOKEN = os.environ.get("TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="#", intents=intents)

# ─── قاموس الألوان المحدث (50 لون) ───────────────────────────────────────────
COLORS = {
    1: ("أحمر صارخ", 0xFF0000), 2: ("أحمر برتقالي", 0xFF2200), 3: ("برتقالي أحمر", 0xFF4400), 
    4: ("برتقالي", 0xFF6600), 5: ("برتقالي ذهبي", 0xFF8800), 6: ("ذهبي", 0xFFAA00), 
    7: ("أصفر ذهبي", 0xFFCC00), 8: ("أصفر", 0xFFFF00), 9: ("أصفر مخضر", 0xCCFF00), 10: ("أخضر مصفر", 0x99FF00),
    11: ("أخضر فاتح", 0x66FF00), 12: ("أخضر عشبي", 0x44CC00), 13: ("أخضر", 0x00AA00), 
    14: ("أخضر غامق", 0x006600), 15: ("أخضر زمردي", 0x00AA55), 16: ("أخضر بحري", 0x00AA77), 
    17: ("أخضر مائي", 0x00BBAA), 18: ("سماوي", 0x00CCCC), 19: ("سماوي فاتح", 0x00DDEE), 20: ("أزرق سماوي", 0x00BBFF),
    21: ("أزرق فاتح", 0x33AAFF), 22: ("أزرق", 0x0077FF), 23: ("أزرق ملكي", 0x0044FF), 
    24: ("أزرق نيلي", 0x0022CC), 25: ("نيلي", 0x0000FF), 26: ("أزرق بنفسجي", 0x2200FF), 
    27: ("بنفسجي مزرق", 0x4400FF), 28: ("بنفسجي فاتح", 0x6600FF), 29: ("بنفسجي", 0x8800FF), 30: ("بنفسجي غامق", 0xAA00DD),
    31: ("أرجواني", 0xBB00AA), 32: ("أرجواني فاتح", 0xCC00BB), 33: ("وردي بنفسجي", 0xDD00CC), 
    34: ("وردي غامق", 0xFF0088), 35: ("وردي", 0xFF0066), 36: ("وردي فاتح", 0xFF3388), 
    37: ("وردي زاهي", 0xFF1493), 38: ("وردي مائل للأحمر", 0xFF2244), 39: ("أحمر وردي", 0xFF3355), 40: ("أحمر فاتح", 0xFF4455),
    41: ("مرجاني", 0xFF6B6B), 42: ("خوخي", 0xFFAA88), 43: ("رملي", 0xDDBB88), 44: ("كريمي", 0xFFEECC), 
    45: ("بيج", 0xF5DEB3), 46: ("رمادي فاتح", 0xCCCCCC), 47: ("رمادي مزرق", 0x99AABB), 
    48: ("رمادي أرجواني", 0xAA99BB), 49: ("رمادي غامق", 0x555555), 50: ("أسود مخملي", 0x111111),
}

# ─── كلاس الأزرار (ColorView) ────────────────────────────────────────────────
class ColorView(discord.ui.View):
    def __init__(self, start: int, end: int, show_remove: bool = False):
        super().__init__(timeout=None)
        for i in range(start, end + 1):
            btn = discord.ui.Button(label=str(i), style=discord.ButtonStyle.secondary, custom_id=f"color_{i}")
            btn.callback = lambda inter, num=i: set_role(inter, num)
            self.add_item(btn)
        if show_remove:
            rem = discord.ui.Button(label="❌ إزالة اللون", style=discord.ButtonStyle.danger, custom_id="remove_all")
            rem.callback = self.remove_all
            self.add_item(rem)

    async def remove_all(self, interaction: discord.Interaction):
        roles_to_remove = [discord.utils.get(interaction.guild.roles, name=str(num)) for num in COLORS]
        roles_to_remove = [r for r in roles_to_remove if r and r in interaction.user.roles]
        if roles_to_remove: await interaction.user.remove_roles(*roles_to_remove)
        await interaction.response.send_message("❌ تمت إزالة جميع الألوان", ephemeral=True, delete_after=5)

# ─── دالة تعيين اللون ─────────────────────────────────────────────────────────
async def set_role(interaction: discord.Interaction, i: int):
    arabic_name, hex_color = COLORS[i]
    role = discord.utils.get(interaction.guild.roles, name=str(i))
    if not role: role = await interaction.guild.create_role(name=str(i), color=discord.Color(hex_color))
    
    roles_to_remove = [discord.utils.get(interaction.guild.roles, name=str(num)) for num in COLORS]
    roles_to_remove = [r for r in roles_to_remove if r and r in interaction.user.roles]
    if roles_to_remove: await interaction.user.remove_roles(*roles_to_remove)
    
    await interaction.user.add_roles(role)
    await interaction.response.send_message(f"✅ تم تفعيل اللون **{arabic_name}** ({i})", ephemeral=True, delete_after=5)

# ─── تشغيل البوت ──────────────────────────────────────────────────────────────
@bot.event
async def on_ready():
    # تسجيل الأزرار لتعمل دائماً
    bot.add_view(ColorView(1, 25))
    bot.add_view(ColorView(26, 37))
    bot.add_view(ColorView(38, 49))
    bot.add_view(ColorView(50, 50, show_remove=True))
    print(f"✅ البوت شغال: {bot.user}")

@bot.command(name="ارسال_اللوحة")
@commands.has_permissions(administrator=True)
async def send_panel(ctx):
    await ctx.send("🎨 **اختر لونك (1-25):**", view=ColorView(1, 25))
    await ctx.send("🎨 **اختر لونك (26-37):**", view=ColorView(26, 37))
    await ctx.send("🎨 **اختر لونك (38-49):**", view=ColorView(38, 49))
    await ctx.send("🎨 **اختر لونك (50):**", view=ColorView(50, 50, show_remove=True))

if TOKEN: bot.run(TOKEN)
    
