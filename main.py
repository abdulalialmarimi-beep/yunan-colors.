import discord
from discord.ext import commands

TOKEN = "ضع_التوكن_هنا"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="#", intents=intents)

# الفئة المسؤولة عن الأزرار
class ColorView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        # إنشاء 40 زر (مربع)
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
            
            # إزالة رتب الألوان القديمة (ليتغير اللون فوراً)
            for r in interaction.user.roles:
                if r.name.startswith("لون "):
                    await interaction.user.remove_roles(r)
            
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"✅ تم تفعيل اللون {i} بنجاح!", ephemeral=True)
        return callback

# أمر إظهار اللوحة
@bot.command()
async def لوحة(ctx):
    await ctx.channel.purge(limit=5) # مسح الرسائل القديمة
    embed = discord.Embed(
        title="👑 نظام ألوان YONAN FAMILY المطور",
        description="اضغط على أي مربع ملون لتغيير لونك فوراً:",
        color=0x2b2d31
    )
    await ctx.send(embed=embed, view=ColorView())

@bot.event
async def on_ready():
    bot.add_view(ColorView()) # تفعيل الأزرار لتعمل دائماً
    print("✅ البوت جاهز ويعمل بكامل قوته!")

bot.run(TOKEN)
