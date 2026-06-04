import discord
from discord.ext import commands

# ضع التوكن هنا
TOKEN = "ضع_التوكن_هنا"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="#", intents=intents)

# إعدادات الصورة والألوان
IMAGE_URL = "https://i.imgur.com/your-image-link.jpg" 
COLORS = {i: (0xFF0000 if i%5==0 else 0x00FF00 if i%3==0 else 0x0000FF if i%2==0 else 0xFFFF00) for i in range(1, 41)}
EMOJIS = {1: "🟥", 2: "🟧", 3: "🟨", 4: "🟩", 5: "🟦", 6: "🟪", 7: "⬛", 8: "⬜", 9: "🟫", 10: "🔴"}

class ColorView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # يجعل الأزرار تعمل للأبد
        for i in range(1, 41):
            emoji = EMOJIS.get(i if i <= 10 else (i%10)+1, "🎨")
            btn = discord.ui.Button(label=f"{i}", emoji=emoji, style=discord.ButtonStyle.secondary, custom_id=f"color_{i}")
            btn.callback = self.make_callback(i)
            self.add_item(btn)

    def make_callback(self, i):
        async def callback(interaction: discord.Interaction):
            role_name = f"لون {i}"
            role = discord.utils.get(interaction.guild.roles, name=role_name)
            if not role:
                role = await interaction.guild.create_role(name=role_name, color=discord.Color(COLORS[i]))
            
            # إزالة رتب الألوان القديمة فقط
            for r in interaction.user.roles:
                if r.name.startswith("لون "):
                    await interaction.user.remove_roles(r)
            
            # إعطاء اللون الجديد
            await interaction.user.add_roles(role)
            # رد سريع ومختصر
            await interaction.response.send_message(f"✅ تم تغيير لونك إلى المربع {i}", ephemeral=True)
        return callback

@bot.event
async def on_ready():
    # تسجيل اللوحة في ذاكرة البوت لتعمل دائماً
    bot.add_view(ColorView())
    print("🚀 البوت التاريخي يعمل بكامل طاقته!")

@bot.command()
async def لوحة(ctx):
    # مسح الرسائل القديمة في القناة
    await ctx.channel.purge(limit=5)
    
    embed = discord.Embed(
        title="👑 YONAN FAMILY - نظام الألوان المطور",
        description="اختر المربع الملون لتغيير لون اسمك فوراً وبدون قيود.",
        color=0x2b2d31
    )
    if IMAGE_URL.startswith("http"):
        embed.set_image(url=IMAGE_URL)
    
    await ctx.send(embed=embed, view=ColorView())

bot.run(TOKEN)
