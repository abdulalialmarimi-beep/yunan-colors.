import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# تشغيل البوت
app = Flask('')
@app.route('/')
def home(): return "البوت يعمل!"
Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()

TOKEN = os.environ.get("TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="#", intents=intents)

# قائمة الألوان الـ 50 المرتبة
COLORS = {
    1: "أحمر صارخ", 2: "أحمر برتقالي", 3: "برتقالي أحمر", 4: "برتقالي", 5: "برتقالي ذهبي",
    6: "ذهبي", 7: "أصفر ذهبي", 8: "أصفر", 9: "أصفر مخضر", 10: "أخضر مصفر",
    11: "أخضر فاتح", 12: "أخضر عشبي", 13: "أخضر", 14: "أخضر غامق", 15: "أخضر زمردي",
    16: "أخضر بحري", 17: "أخضر مائي", 18: "سماوي", 19: "سماوي فاتح", 20: "أزرق سماوي",
    21: "أزرق فاتح", 22: "أزرق", 23: "أزرق ملكي", 24: "أزرق نيلي", 25: "نيلي",
    26: "أزرق بنفسجي", 27: "بنفسجي مزرق", 28: "بنفسجي فاتح", 29: "بنفسجي", 30: "بنفسجي غامق",
    31: "أرجواني", 32: "أرجواني فاتح", 33: "وردي بنفسجي", 34: "وردي غامق", 35: "وردي",
    36: "وردي فاتح", 37: "وردي زاهي", 38: "وردي مائل للأحمر", 39: "أحمر وردي", 40: "أحمر فاتح",
    41: "مرجاني", 42: "خوخي", 43: "رملي", 44: "كريمي", 45: "بيج",
    46: "رمادي فاتح", 47: "رمادي مزرق", 48: "رمادي أرجواني", 49: "رمادي غامق", 50: "أسود مخملي"
}

# دالة إعطاء الرتبة
async def set_role(interaction, i):
    name = COLORS[i]
    role = discord.utils.get(interaction.guild.roles, name=name)
    if not role: role = await interaction.guild.create_role(name=name)
    
    # إزالة الألوان السابقة فوراً
    for n in COLORS.values():
        old = discord.utils.get(interaction.guild.roles, name=n)
        if old in interaction.user.roles: await interaction.user.remove_roles(old)
    
    await interaction.user.add_roles(role)
    await interaction.response.send_message(f"✅ تم تفعيل: {name}", ephemeral=True, delete_after=2)

# الكلاس الموحد للوحتين
class ColorView(discord.ui.View):
    def __init__(self, start, end, is_last=False):
        super().__init__(timeout=None)
        for i in range(start, end + 1):
            btn = discord.ui.Button(label=str(i), style=discord.ButtonStyle.secondary, custom_id=f"color_{i}")
            btn.callback = lambda inter, i=i: set_role(inter, i)
            self.add_item(btn)
        
        # إضافة زر الإزالة في نهاية اللوحة الثانية فقط
        if is_last:
            rem = discord.ui.Button(label="إزالة الألوان", style=discord.ButtonStyle.danger, custom_id="rem_all")
            rem.callback = self.remove_all
            self.add_item(rem)

    async def remove_all(self, inter):
        for name in COLORS.values():
            r = discord.utils.get(inter.guild.roles, name=name)
            if r in interaction.user.roles: await interaction.user.remove_roles(r)
        await inter.response.send_message("❌ تمت إزالة الألوان", ephemeral=True, delete_after=2)

@bot.command()
async def ارسال_اللوحة(ctx):
    # إرسال الرسالتين معاً لتعطي شكل 50 زر كاملة
    await ctx.send("👑 **لوحة الألوان (1-50):**", view=ColorView(1, 25))
    await ctx.send(view=ColorView(26, 50, is_last=True))

bot.run(TOKEN)
