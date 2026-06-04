import os
import discord
from discord.ext import commands

# تأكد أن اسم الـ Key في موقع Render هو BOT_TOKEN
TOKEN = os.environ.get("BOT_TOKEN")
IMAGE_URL = "ضع_رابط_صورتك_هنا"

bot = commands.Bot(command_prefix="#", intents=discord.Intents.all())

class ColorView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        for i in range(1, 41):
            btn = discord.ui.Button(label=str(i), style=discord.ButtonStyle.primary, custom_id=f"color_{i}")
            btn.callback = self.make_callback(i)
            self.add_item(btn)

    def make_callback(self, i):
        async def callback(interaction: discord.Interaction):
            role_name = f"Color #{i}"
            role = discord.utils.get(interaction.guild.roles, name=role_name)
            if not role:
                role = await interaction.guild.create_role(name=role_name)
            for r in interaction.user.roles:
                if r.name.startswith("Color #"): 
                    await interaction.user.remove_roles(r)
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"✅ تم تفعيل اللون #{i}", ephemeral=True)
        return callback

@bot.event
async def on_ready():
    bot.add_view(ColorView())
    print("✅ البوت جاهز!")

@bot.command()
async def لون(ctx):
    embed = discord.Embed(title="🎨 لوحة ألوان YONAN FAMILY")
    embed.set_image(url=IMAGE_URL)
    await ctx.send(embed=embed, view=ColorView())

bot.run(TOKEN)
