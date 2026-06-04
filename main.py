import discord
from discord.ext import commands

TOKEN = "ضع_التوكن_هنا"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="#", intents=intents)

# قائمة بألوان المربعات (يمكنك تغيير الأكواد للألوان التي تفضلها)
# قمت بتنويع الألوان لتظهر اللوحة زاهية
COLORS = {i: (0xFF0000 if i%5==0 else 0x00FF00 if i%3==0 else 0x0000FF if i%2==0 else 0xFFFF00) for i in range(1, 41)}
EMOJIS = {1: "🟥", 2: "🟧", 3: "🟨", 4: "🟩", 5: "🟦", 6: "🟪", 7: "⬛", 8: "⬜", 9: "🟫", 10: "🔴"}

class ColorView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        for i in range(1, 41):
            # استخدام الإيموجي لجعل الزر يبدو كمربع ملون حقيقي
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
            
            # إزالة الألوان القديمة (ليتغير اللون فوراً)
            for r in interaction.user.roles:
                if r.name.startswith("لون "):
                    await interaction.user.remove_roles(r)
            
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"✅ تم تفعيل اللون {i} بنجاح!", ephemeral=True)
        return callback

@bot.command()
async def لوحة(ctx):
    embed = discord.Embed(
        title="👑 أقوى نظام ألوان في ديسكورد - YONAN FAMILY",
        description="اختر المربع الملون ليتغير اسمك فوراً! يمكنك التغيير وقتما تشاء.",
        color=0x2b2d31
    )
    await ctx.send(embed=embed, view=ColorView())

@bot.event
async def on_ready():
    bot.add_view(ColorView())
    print("✅ البوت التاريخي يعمل الآن بكامل قوته!")

bot.run(TOKEN)
