import discord
from discord.ext import commands

# ضع التوكن الخاص بك هنا
TOKEN = "ضع_التوكن_هنا"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="#", intents=intents)

class ColorView(discord.ui.View):
    def __init__(self):
        # timeout=None يجعل الأزرار تعمل للأبد ولا تنتهي صلاحيتها
        super().__init__(timeout=None)
        # إنشاء 40 زر (مربعات الألوان)
        for i in range(1, 41):
            btn = discord.ui.Button(label=f"لون {i}", style=discord.ButtonStyle.primary, custom_id=f"color_{i}")
            btn.callback = self.make_callback(i)
            self.add_item(btn)

    def make_callback(self, i):
        async def callback(interaction: discord.Interaction):
            role_name = f"لون {i}"
            role = discord.utils.get(interaction.guild.roles, name=role_name)
            if not role:
                # إنشاء الرتبة تلقائياً إذا لم تكن موجودة
                role = await interaction.guild.create_role(name=role_name)
            
            # إزالة رتب الألوان القديمة (ليتغير اللون فوراً عند اختيار لون جديد)
            for r in interaction.user.roles:
                if r.name.startswith("لون "):
                    await interaction.user.remove_roles(r)
            
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"✅ تم تفعيل اللون {i} بنجاح!", ephemeral=True)
        return callback

@bot.command()
async def لوحة(ctx):
    # مسح الرسائل القديمة في القناة قبل إرسال اللوحة (للحفاظ على نظافة القناة)
    await ctx.channel.purge(limit=10)
    
    embed = discord.Embed(
        title="👑 أقوى نظام ألوان - YONAN FAMILY",
        description="اضغط على أي مربع ملون لتغيير لون اسمك فوراً:",
        color=0x2b2d31
    )
    await ctx.send(embed=embed, view=ColorView())

@bot.event
async def on_ready():
    # تسجيل الأزرار في ذاكرة البوت لتعمل دائماً
    bot.add_view(ColorView())
    print("🚀 البوت التاريخي جاهز للعمل!")

bot.run(TOKEN)
