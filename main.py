import discord
from discord.ext import commands
import os

TOKEN = os.environ.get("TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="#", intents=intents)

class ColorView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        for i in range(1, 6):
            btn = discord.ui.Button(label=f"لون {i}", style=discord.ButtonStyle.primary, custom_id=f"color_{i}")
            btn.callback = self.make_callback(i)
            self.add_item(btn)

    def make_callback(self, i):
        async def callback(interaction: discord.Interaction):
            role_name = f"Color {i}"
            role = discord.utils.get(interaction.guild.roles, name=role_name)
            if not role:
                role = await interaction.guild.create_role(name=role_name)
            for r in interaction.user.roles:
                if r.name.startswith("Color "):
                    await interaction.user.remove_roles(r)
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"✅ تم تفعيل اللون {i}!", ephemeral=True)
        return callback

@bot.command()
async def لوحة(ctx):
    embed = discord.Embed(title="🎨 لوحة ألوان YONAN FAMILY", description="اختر لونك المفضل:")
    await ctx.send(embed=embed, view=ColorView())

@bot.event
async def on_ready():
    bot.add_view(ColorView())
    print("✅ البوت جاهز ويعمل الآن!")

if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ خطأ: التوكن غير موجود!")
    
