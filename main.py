import discord
from discord.ext import commands

TOKEN = "ضع_التوكن_هنا"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="#", intents=intents)

# فئة الأزرار (40 زر مرتبة)
class ColorView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # يجعل الأزرار دائمة
        for i in range(1, 41):
            btn = discord.ui.Button(label=f"لون {i}", style=discord.ButtonStyle.primary, custom_id=f"color_{i}")
            btn.callback = self.make_callback(i)
            self.add_item(btn)

    def make_callback(self, i):
        async def callback(interaction: discord.Interaction):
            role_name = f"لون {i}"
            role = discord.utils.get(interaction.guild.roles, name=role_name)
            if not role:
                role = await interaction.guild.create_role(name=role_name)
            
            # إزالة رتب الألوان القديمة للعضو
            for r in interaction.user.roles:
                if r.name.startswith("لون "):
                    await interaction.user.remove_roles(r)
            
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"✅ تم تفعيل اللون {i} بنجاح!", ephemeral=True)
        return callback

# الأمر الوحيد الذي تحتاجه
@bot.command()
async def لوحة(ctx):
    # يحذف أي لوحة قديمة في القناة قبل إرسال الجديدة
    await ctx.channel.purge(limit=5)
    
    embed = discord.Embed(
        title="👑 أقوى نظام ألوان - YONAN FAMILY",
        description="اضغط على أي مربع ملون لتغيير لون اسمك فوراً:",
        color=0x2b2d31
    )
    await ctx.send(embed=embed, view=ColorView())

@bot.event
async def on_ready():
    bot.add_view(ColorView()) # يربط الأزرار بالذاكرة
    print("🚀 البوت جاهز ويعمل بكامل قوته!")

bot.run(TOKEN)
