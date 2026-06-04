import discord
from discord.ext import commands
import logging

logging.getLogger('discord').setLevel(logging.ERROR)

TOKEN = "ضع_التوكن_الخاص_بك_هنا"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="#", intents=intents, help_command=None)

# قاموس الألوان (كل لون ورقم الرتبة الخاص به)
# يمكنك تغيير الألوان هنا (Hex Codes)
COLOR_MAP = {
    1: 0xFF0000, 2: 0x00FF00, 3: 0x0000FF, 4: 0xFFFF00, 5: 0xFF00FF,
    6: 0x00FFFF, 7: 0xFF8000, 8: 0x800080, 9: 0xFF1493, 10: 0x7FFF00,
    11: 0x8B4513, 12: 0xFFFFFF, 13: 0x808080, 14: 0x000000, 15: 0xB22222,
    16: 0x228B22, 17: 0x4169E1, 18: 0xFFD700, 19: 0x9400D3, 20: 0x20B2AA,
    21: 0xFF4500, 22: 0x32CD32, 23: 0x1E90FF, 24: 0xF0E68C, 25: 0xEE82EE,
    26: 0xAFEEEE, 27: 0xA52A2A, 28: 0x708090, 29: 0xDC143C, 30: 0x006400,
    31: 0x00008B, 32: 0xFF8C00, 33: 0x4B0082, 34: 0x00CED1, 35: 0x8B0000,
    36: 0x556B2F, 37: 0x483D8B, 38: 0xB8860B, 39: 0x8FBC8F, 40: 0x2F4F4F
}

class ColorView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        for i in range(1, 41):
            # نحدد لون الزر بناءً على لون الرتبة
            # ملاحظة: ديسكورد لا يدعم كل الألوان في الزر، لذا نستخدم Secondary للجميع لضمان التوافق
            btn = discord.ui.Button(label=f"لون {i}", style=discord.ButtonStyle.secondary, custom_id=f"color_{i}")
            btn.callback = self.make_callback(i)
            self.add_item(btn)

    def make_callback(self, i):
        async def callback(interaction: discord.Interaction):
            role_name = f"لون {i}"
            role = discord.utils.get(interaction.guild.roles, name=role_name)
            
            # إذا لم توجد الرتبة، ننشئها باللون المحدد في القاموس
            if not role:
                role = await interaction.guild.create_role(name=role_name, color=discord.Color(COLOR_MAP[i]))
            
            # إزالة رتب الألوان القديمة
            for r in interaction.user.roles:
                if r.name.startswith("لون "):
                    await interaction.user.remove_roles(r)
            
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"✅ تم تفعيل اللون {i}!", ephemeral=True)
        return callback

@bot.command()
async def لوحة(ctx):
    await ctx.channel.purge(limit=5)
    embed = discord.Embed(
        title="👑 YONAN FAMILY | نظام الألوان المتكامل", 
        description="اضغط على الزر ليصبح اسمك بهذا اللون:", 
        color=0x2b2d31
    )
    await ctx.send(embed=embed, view=ColorView())

@bot.event
async def on_ready():
    bot.add_view(ColorView())
    print("🔥 البوت يعمل الآن وبألوان مخصصة لكل رتبة!")

bot.run(TOKEN)
