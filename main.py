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

# القائمة الدقيقة بأسماء الألوان
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

async def set_role(interaction, i):
    await interaction.response.defer(ephemeral=True)
    name = COLORS[i]
    role = discord.utils.get(interaction.guild.roles, name=name)
    if not role: role = await interaction.guild.create_role(name=name)
    
    for n in COLORS.values():
        old = discord.utils.get(interaction.guild.roles, name=n)
        if old in interaction.user.roles: await interaction.user.remove_roles(old)
    
    await interaction.user.add_roles(role)
    await interaction.followup.send(f"✅ تم تفعيل: {name}", ephemeral=True, delete_after=3)

# بناء الرسالة التوضيحية
def build_desc(start, end):
    return "\n".join([f"**{i}.** {COLORS[i]}" for i in range(start, end + 1)])

class View1(discord.ui.View): 
    def __init__(self):
        super().__init__(timeout=None)
        for i in range(1, 26):
            btn = discord.ui.Button(label=str(i), style=discord.ButtonStyle.secondary, custom_id=f"c{i}")
            btn.callback = lambda inter, i=i: set_role(inter, i)
            self.add_item(btn)

class View2(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        for i in range(26, 51):
            btn = discord.ui.Button(label=str(i), style=discord.ButtonStyle.secondary, custom_id=f"c{i}")
            btn.callback = lambda inter, i=i: set_role(inter, i)
            self.add_item(btn)
        rem = discord.ui.Button(label="❌ إزالة", style=discord.ButtonStyle.danger, custom_id="rem")
        rem.callback = self.remove
        self.add_item(rem)

    async def remove(self, inter):
        await inter.response.defer(ephemeral=True)
        for name in COLORS.values():
            r = discord.utils.get(inter.guild.roles, name=name)
            if r in inter.user.roles: await inter.user.remove_roles(r)
        await inter.followup.send("❌ تمت إزالة الألوان", ephemeral=True, delete_after=3)

@bot.command()
async def ارسال_اللوحة(ctx):
    class Open(discord.ui.View):
        @discord.ui.button(label="👑 افتح لوحة الألوان", style=discord.ButtonStyle.green)
        async def click(self, inter, btn):
            await inter.response.send_message(f"**اختر لونك (1-25):**\n{build_desc(1, 25)}", view=View1(), ephemeral=True)
            await inter.followup.send(f"**اختر لونك (26-50):**\n{build_desc(26, 50)}", view=View2(), ephemeral=True)
    await ctx.send("نظام YONAN:", view=Open())

bot.run(TOKEN)
