import discord
from discord.ext import commands
from discord.ui import Button, View
import os

TOKEN = os.getenv('BOT_TOKEN')
COLOR_LIST = ["#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF", "#C0C0C0", "#808080", "#800000", "#808000", "#008000", "#800080", "#008080", "#000080", "#FFA500", "#FF69B4", "#FF1493", "#ADFF2F"]

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="#", intents=intents)

# زر التفعيل الرئيسي
class MainView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎨 اضغط هنا لاختيار لونك", style=discord.ButtonStyle.success, custom_id="main_btn")
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        # عندما يضغط العضو، تظهر له لوحة الألوان مباشرة
        await interaction.response.send_message("اختر لونك من القائمة أدناه:", view=ColorView(page=1), ephemeral=True)

class ColorView(discord.ui.View):
    def __init__(self, page=1):
        super().__init__(timeout=None)
        self.page = page
        self.setup_buttons()

    def setup_buttons(self):
        start_idx = 0 if self.page == 1 else 10
        end_idx = 10 if self.page == 1 else 20
        for i in range(start_idx, end_idx):
            btn = Button(label=f"#{i}", style=discord.ButtonStyle.secondary, custom_id=f"color_btn_{i}")
            btn.callback = self.make_color_callback(i)
            self.add_item(btn)
        
        # أزرار التنقل
        nav_btn = Button(label="التالي" if self.page == 1 else "رجوع", style=discord.ButtonStyle.primary)
        nav_btn.callback = self.next_page_callback if self.page == 1 else self.prev_page_callback
        self.add_item(nav_btn)

    def make_color_callback(self, color_index):
        async def callback(interaction: discord.Interaction):
            role_name = f"Color #{color_index}"
            role = discord.utils.get(interaction.guild.roles, name=role_name)
            if not role:
                role = await interaction.guild.create_role(name=role_name, color=discord.Color(int(COLOR_LIST[color_index].lstrip('#'), 16)))
            for r in interaction.user.roles:
                if r.name.startswith("Color #"): await interaction.user.remove_roles(r)
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"✅ تم تفعيل اللون #{color_index}", ephemeral=True)
        return callback

    async def next_page_callback(self, interaction: discord.Interaction):
        self.page = 2
        self.setup_buttons()
        await interaction.response.edit_message(view=self)

    async def prev_page_callback(self, interaction: discord.Interaction):
        self.page = 1
        self.setup_buttons()
        await interaction.response.edit_message(view=self)

@bot.event
async def on_ready():
    bot.add_view(MainView())
    bot.add_view(ColorView(page=1))
    print("✅ البوت جاهز!")

@bot.command()
@commands.has_permissions(administrator=True)
async def لوحة(ctx):
    embed = discord.Embed(title="🎨 نظام الألوان الخاص بـ Yunan Family", description="اضغط على الزر أدناه لاختيار لونك!", color=0x000000)
    embed.set_image(url="ضع_رابط_صورتك_هنا")
    await ctx.send(embed=embed, view=MainView())

bot.run(TOKEN)
        @bot.command(name="لون")
@commands.has_permissions(administrator=True)
async def setup_colors(ctx):
    embed = discord.Embed(
        title="🎨 لوحة ألوان سيرفر Yunan Family",
        description="اختر رقم اللون المناسب لك من الجدول وسيتم تفعيله لاسمك فوراً!\n\n• استخدم **التالي** و **رجوع** للتنقل.\n• اضغط **حذف اللون** لإزالته.",
        color=discord.Color.from_rgb(46, 139, 87)
    )
    await ctx.send(embed=embed, view=ColorView(page=1))
    await ctx.message.delete()

bot.run(TOKEN)
      
