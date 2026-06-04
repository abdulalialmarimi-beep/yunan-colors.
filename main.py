import discord
from discord.ext import commands

TOKEN = "ضع_التوكن_هنا"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="#", intents=intents)

class ColorView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        # إنشاء 40 زر
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
            
            # إزالة الألوان القديمة
            for r in interaction.user.roles:
                if r.name.startswith("لون "):
                    await interaction.user.remove_roles(r)
            
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"✅ تم تفعيل اللون {i}!", ephemeral=True)
        return callback

@bot.command()
async def لوحة(ctx):
    # هذا السطر يحذف الرسائل القديمة في القناة قبل إرسال اللوحة
    await ctx.channel.purge(limit=10)
    
    embed = discord.Embed(title="👑 لوحة ألوان YONAN FAMILY", description="اختر المربع الملون ليتغير لون اسمك فوراً!", color=0x2b2d31)
    await ctx.send(embed=embed, view=ColorView())

@bot.event
async def on_ready():
    bot.add_view(ColorView())
    print("🚀 البوت جاهز ويعمل بكامل قوته!")

bot.run(TOKEN)
