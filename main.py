import discord
from discord.ext import commands
from discord.ui import Button, View

TOKEN = "MTA..." # ضع توكنك هنا
IMAGE_URL = "رابط_صورتك_هنا"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="#", intents=intents)

class ColorView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        for i in range(40):
            btn = discord.ui.Button(label=f"#{i}", style=discord.ButtonStyle.primary, custom_id=f"color_{i}")
            btn.callback = self.make_callback(i)
            self.add_item(btn)

    def make_callback(self, i):
        async def callback(interaction: discord.Interaction):
            role = discord.utils.get(interaction.guild.roles, name=f"Color #{i}")
            if not role:
                role = await interaction.guild.create_role(name=f"Color #{i}")
            
            for r in interaction.user.roles:
                if r.name.startswith("Color #"): await interaction.user.remove_roles(r)
            
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

bot.run(MTUxMjA4OTMyMzkyNTkzMDA5NQ.GvB_P5.2MeMskAxcZfEnWE_FVk6smDxeL3A6l0quaIn7M)
