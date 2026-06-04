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

# تشغيل خادم التنشيط في الخلفية
t = Thread(target=run)
t.start()
# -------------------------

TOKEN = os.environ.get("TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="#", intents=intents)

COLOR_LIST = [
    0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFF, 0xFF8000, 0x800080, 0x008000, 0x800000,
    0x000080, 0xFF1493, 0x7FFF00, 0x00CED1, 0xFF4500, 0x32CD32, 0x1E90FF, 0xF0E68C, 0xEE82EE, 0x00FF7F,
    0xDC143C, 0x4682B4, 0xD2691E, 0x20B2AA, 0x9370DB, 0x778899, 0xBC8F8F, 0xBA55D3, 0x2E8B57, 0xCD5C5C,
    0x48D1CC, 0xFFD700, 0xADFF2F, 0xDB7093, 0x40E0D0, 0x8B4513, 0xFF69B4, 0x6495ED, 0x7B68EE, 0x2F4F4F,
    0xFF6347, 0x8A2BE2, 0x00BFFF, 0xFA8072, 0x5F9EA0, 0xDDA0DD, 0xB0C4DE, 0xE9967A, 0x8FBC8F, 0xFF00FF
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
            btn = discord.ui.Button(label=f"لون {num}", style=discord.ButtonStyle.secondary, custom_id=f"c{num}")
            btn.callback = self.make_callback(num)
            self.add_item(btn)
        
        # أزرار التحكم
        self.add_item(discord.ui.Button(label="⬅️", style=discord.ButtonStyle.primary, custom_id="prev", row=4))
        self.add_item(discord.ui.Button(label="إزالة الألوان", style=discord.ButtonStyle.danger, custom_id="remove", row=4))
        self.add_item(discord.ui.Button(label="➡️", style=discord.ButtonStyle.primary, custom_id="next", row=4))

    def make_callback(self, num):
        async def callback(interaction: discord.Interaction):
            try:
                role_name = f"لون {num}"
                role = discord.utils.get(interaction.guild.roles, name=role_name)
                if not role:
                    role = await interaction.guild.create_role(name=role_name, color=discord.Color(COLOR_LIST[num-1]))
                
                # إزالة رتب الألوان السابقة لتجنب التراكم
                for r in interaction.user.roles:
                    if r.name.startswith("لون "): await interaction.user.remove_roles(r)
                
                await interaction.user.add_roles(role)
                await interaction.response.send_message(f"✅ تم تفعيل {role_name}!", ephemeral=True)
                await asyncio.sleep(4)
                await interaction.delete_original_response()
            except Exception as e:
                print(f"خطأ أثناء اختيار اللون: {e}")
        return callback

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        cid = interaction.data.get("custom_id")
        if cid == "prev": self.page = max(0, self.page - 1)
        elif cid == "next": self.page = min(4, self.page + 1)
        elif cid == "remove":
            for r in interaction.user.roles:
                if r.name.startswith("لون "): await interaction.user.remove_roles(r)
            await interaction.response.send_message("❌ تم إزالة جميع ألوانك!", ephemeral=True)
            await asyncio.sleep(4)
            await interaction.delete_original_response()
            return True
        self.create_buttons()
        await interaction.response.edit_message(view=self)
        return True

@bot.event
async def on_ready():
    print(f'البوت {bot.user} جاهز للعمل 24/7!')

@bot.command()
async def لوحة(ctx):
    await ctx.send("👑 **نظام ألوان YONAN (50 لوناً) - اختر لونك المفضل:**", view=ColorPagination())

bot.run(TOKEN)
        
