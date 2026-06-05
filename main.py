import os
import asyncio
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# ─── سيرفر Flask ─────────────────────────────────────────────────────────────
app = Flask('')
@app.route('/')
def home(): return "البوت يعمل! ✅"
def run_flask(): app.run(host='0.0.0.0', port=8080)
Thread(target=run_flask, daemon=True).start()

# ─── إعدادات البوت ────────────────────────────────────────────────────────────
TOKEN = os.environ.get("TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="#", intents=intents)

# ─── قاموس الألوان المحدث (ألوان احترافية) ──────────────────────────────────
COLORS = {
    1: ("أحمر صارخ", 0xE74C3C), 2: ("أحمر برتقالي", 0xF39C12), 3: ("برتقالي أحمر", 0xD35400), 4: ("برتقالي", 0xE67E22), 5: ("برتقالي ذهبي", 0xF1C40F),
    6: ("ذهبي", 0xF1C40F), 7: ("أصفر ذهبي", 0xF7DC6F), 8: ("أصفر", 0xFFF176), 9: ("أصفر مخضر", 0xD4E157), 10: ("أخضر مصفر", 0xC0CA33),
    11: ("أخضر فاتح", 0x8BC34A), 12: ("أخضر عشبي", 0x7CB342), 13: ("أخضر", 0x4CAF50), 14: ("أخضر غامق", 0x2E7D32), 15: ("أخضر زمردي", 0x009688),
    16: ("أخضر بحري", 0x26A69A), 17: ("أخضر مائي", 0x80CBC4), 18: ("سماوي", 0x4DD0E1), 19: ("سماوي فاتح", 0x80DEEA), 20: ("أزرق سماوي", 0x29B6F6),
    21: ("أزرق فاتح", 0x03A9F4), 22: ("أزرق", 0x2196F3), 23: ("أزرق ملكي", 0x1E88E5), 24: ("أزرق نيلي", 0x3949AB), 25: ("نيلي", 0x5C6BC0),
    26: ("أزرق بنفسجي", 0x7E57C2), 27: ("بنفسجي مزرق", 0x9575CD), 28: ("بنفسجي فاتح", 0xB39DDB), 29: ("بنفسجي", 0x673AB7), 30: ("بنفسجي غامق", 0x512DA8),
    31: ("أرجواني", 0xAB47BC), 32: ("أرجواني فاتح", 0xCE93D8), 33: ("وردي بنفسجي", 0xEC407A), 34: ("وردي غامق", 0xD81B60), 35: ("وردي", 0xF06292),
    36: ("وردي فاتح", 0xF48FB1), 37: ("وردي زاهي", 0xFF80AB), 38: ("وردي مائل للأحمر", 0xEF5350), 39: ("أحمر وردي", 0xE57373), 40: ("أحمر فاتح", 0xFF8A80),
    41: ("مرجاني", 0xFF7043), 42: ("خوخي", 0xFFCCBC), 43: ("رملي", 0xD7CCC8), 44: ("كريمي", 0xFFF9C4), 45: ("بيج", 0xD7CCC8),
    46: ("رمادي فاتح", 0xCFD8DC), 47: ("رمادي مزرق", 0x90A4AE), 48: ("رمادي أرجواني", 0x9FA8DA), 49: ("رمادي غامق", 0x546E7A), 50: ("أسود مخملي", 0x212121)
}

# ─── دالة تعيين اللون (محدثة لمنع التعليق) ───────────────────────────────────
async def set_role(interaction: discord.Interaction, i: int):
    # استخدام defer لتجنب خطأ فشل التفاعل عند الضغط المتكرر
    await interaction.response.defer(ephemeral=True)
    
    try:
        arabic_name, hex_color = COLORS[i]
        role_name = str(i)
        role = discord.utils.get(interaction.guild.roles, name=role_name)
        if not role: role = await interaction.guild.create_role(name=role_name, color=discord.Color(hex_color))

        # إزالة الرتب القديمة مع تأخير بسيط للحماية
        roles_to_remove = [discord.utils.get(interaction.guild.roles, name=str(num)) for num in COLORS]
        roles_to_remove = [r for r in roles_to_remove if r and r in interaction.user.roles]
        
        if roles_to_remove:
            await interaction.user.remove_roles(*roles_to_remove)
            await asyncio.sleep(0.3) 

        await interaction.user.add_roles(role)
        await interaction.followup.send(f"✅ تم تفعيل اللون **{arabic_name}** ({i})", ephemeral=True)
    except Exception as e:
        await interaction.followup.send("❌ حدث خطأ، يرجى المحاولة بعد قليل.", ephemeral=True)

# ─── كلاس الأزرار ─────────────────────────────────────────────────────────────
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
        await interaction.response.defer(ephemeral=True)
        roles_to_remove = [discord.utils.get(interaction.guild.roles, name=str(num)) for num in COLORS]
        roles_to_remove = [r for r in roles_to_remove if r and r in interaction.user.roles]
        if roles_to_remove: await interaction.user.remove_roles(*roles_to_remove)
        await interaction.followup.send("❌ تمت إزالة جميع الألوان", ephemeral=True)

# ─── التشغيل ────────────────────────────────────────────────────────────────
@bot.event
async def on_ready():
    bot.add_view(ColorView(1, 25))
    bot.add_view(ColorView(26, 37))
    bot.add_view(ColorView(38, 49))
    bot.add_view(ColorView(50, 50, show_remove=True))
    print(f"✅ البوت جاهز: {bot.user}")

@bot.command(name="ارسال_اللوحة")
@commands.has_permissions(administrator=True)
async def send_panel(ctx):
    await ctx.send("🎨 **اختر لونك (1-25):**", view=ColorView(1, 25))
    await ctx.send("🎨 **اختر لونك (26-37):**", view=ColorView(26, 37))
    await ctx.send("🎨 **اختر لونك (38-49):**", view=ColorView(38, 49))
    await ctx.send("🎨 **اختر لونك (50):**", view=ColorView(50, 50, show_remove=True))

bot.run(TOKEN)
