import discord
from discord.ext import commands
from discord.ui import Button, View
import os

# السحب التلقائي للتوكن من إعدادات موقع ريندر للأمان
TOKEN = os.getenv("BOT_TOKEN")

# قائمة الـ 40 لون احترافي
COLOR_LIST = [
    "000000", "FFFFFF", "FF0000", "00FF00", "0000FF", "FFFF00", "00FFFF", "FF00FF", "C0C0C0", "808080",
    "800000", "808000", "008000", "800080", "008080", "000080", "FFA500", "FFD700", "7FFF00", "D2691E",
    "FF69B4", "FF1493", "ADFF2F", "40E0D0", "1E90FF", "9370DB", "8B008B", "FF4500", "2E8B57", "4682B4",
    "D2B48C", "BC8F8F", "F0E68C", "E6E6FA", "FFF0F5", "F0FFFF", "F5FFFA", "F0F8FF", "FFF8DC", "FAEBD7"
]

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="#", intents=intents)

async def remove_current_colors(member):
    for role in member.roles:
        if role.name.startswith("Color #"):
            try: await member.remove_roles(role)
            except discord.Forbidden: pass

class ColorView(View):
    def __init__(self, page=1):
        super().__init__(timeout=None)
        self.page = page
        self.setup_buttons()

    def setup_buttons(self):
        self.clear_items()
        start_idx = 0 if self.page == 1 else 20
        end_idx = 20 if self.page == 1 else 40

        for i in range(start_idx, end_idx):
            btn = Button(
                label=f"#{i}", 
                style=discord.ButtonStyle.secondary, 
                custom_id=f"color_btn_{i}",
                row=i // 5 % 4
            )
            btn.callback = self.make_color_callback(i)
            self.add_item(btn)

        delete_btn = Button(label="حذف اللون", style=discord.ButtonStyle.danger, custom_id="delete_color_btn", row=4)
        delete_btn.callback = self.delete_color_callback
        self.add_item(delete_btn)

        if self.page == 1:
            next_btn = Button(label="التالي", style=discord.ButtonStyle.primary, custom_id="next_page_btn", row=4)
            next_btn.callback = self.next_page_callback
            self.add_item(next_btn)
        else:
            prev_btn = Button(label="رجوع", style=discord.ButtonStyle.primary, custom_id="prev_page_btn", row=4)
            prev_btn.callback = self.prev_page_callback
            self.add_item(prev_btn)

    def make_color_callback(self, color_index):
        async def callback(interaction: discord.Interaction):
            await interaction.response.defer(ephemeral=True)
            guild = interaction.guild
            member = interaction.user
            role_name = f"Color #{color_index}"
            
            role = discord.utils.get(guild.roles, name=role_name)
            if not role:
                hex_color = COLOR_LIST[color_index]
                color_obj = discord.Color(int(hex_color, 16))
                role = await guild.create_role(name=role_name, color=color_obj, reason="لوحة الألوان")
                
                bot_member = guild.get_member(bot.user.id)
                if bot_member and bot_member.top_role.position > role.position:
                    try: await role.edit(position=bot_member.top_role.position - 1)
                    except discord.Forbidden: pass

            await remove_current_colors(member)
            await member.add_roles(role)
            await interaction.followup.send(f"✅ تم تفعيل اللون **#{color_index}** بنجاح!", ephemeral=True)
        return callback

    async def delete_color_callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await remove_current_colors(interaction.user)
        await interaction.followup.send("❌ تم حذف لونك الحالي بنجاح.", ephemeral=True)

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
    print(f"✅ {bot.user} جاهز للعمل!")
    bot.add_view(ColorView(page=1))
    bot.add_view(ColorView(page=2))

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
      
