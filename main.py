import os
import discord
from discord.ext import commands

# قراءة التوكن من إعدادات الرندر (Environment Variables)
TOKEN = os.environ.get("TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="#", intents=intents)

# نظام الصفحات والأزرار للألوان
class ColorPagination(discord.ui.View):
    def __init__(self, page=0):
        super().__init__(timeout=None)
        self.page = page
        self.colors_per_page = 20
        start = page * self.colors_per_page + 1
        end = start + self.colors_per_page
        
        # إضافة أزرار الألوان (مثلاً من 1 إلى 20 في الصفحة الأولى)
        for i in range(start, end):
            btn = discord.ui.Button(label=f"لون {i}", style=discord.ButtonStyle.secondary, custom_id=f"color_{i}")
            btn.callback = self.make_callback(i)
            self.add_item(btn)
        
        # أزرار التحكم
        self.add_item(discord.ui.Button(label="⬅️", style=discord.ButtonStyle.primary, custom_id="prev", row=4))
        self.add_item(discord.ui.Button(label="إزالة الألوان", style=discord.ButtonStyle.danger, custom_id="remove", row=4))
        self.add_item(discord.ui.Button(label="➡️", style=discord.ButtonStyle.primary, custom_id="next", row=4))

    def make_callback(self, i):
        async def callback(interaction: discord.Interaction):
            role_name = f"لون {i}"
            role = discord.utils.get(interaction.guild.roles, name=role_name)
            if not role: role = await interaction.guild.create_role(name=role_name)
            
            # إزالة أي لون قديم
            for r in interaction.user.roles:
                if r.name.startswith("لون "): await interaction.user.remove_roles(r)
            
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"✅ تم تفعيل اللون {i} بنجاح!", ephemeral=True)
        return callback

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.data.get("custom_id") == "remove":
        for r in interaction.user.roles:
            if r.name.startswith("لون "): await interaction.user.remove_roles(r)
        await interaction.response.send_message("❌ تم إزالة جميع الألوان الخاصة بك!", ephemeral=True)

@bot.command()
async def لوحة(ctx):
    await ctx.send("👑 **نظام ألوان YONAN:** اختر لونك المفضل من القائمة:", view=ColorPagination())

@bot.event
async def on_ready():
    print("🚀 البوت يعمل الآن وبكل قوته!")

bot.run(TOKEN)
