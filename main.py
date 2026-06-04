
import os
import discord
from discord.ext import commands
import asyncio

# قراءة التوكن بأمان
TOKEN = os.environ.get("TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="#", intents=intents)

# توليد 50 لوناً مختلفاً بجودة عالية
COLORS = [discord.Color.from_hsv(i/50, 0.7, 0.9) for i in range(50)]

class ColorPagination(discord.ui.View):
    def __init__(self, page=0):
        super().__init__(timeout=None)
        self.page = page
        self.create_buttons()

    def create_buttons(self):
        self.clear_items()
        # عرض 10 أزرار في كل صفحة (5 صفحات إجمالاً)
        start = self.page * 10
        end = min(start + 10, 50)
        
        for i in range(start, end):
            num = i + 1
            btn = discord.ui.Button(label=f"لون {num}", style=discord.ButtonStyle.secondary, custom_id=f"c{num}")
            btn.callback = self.make_callback(num)
            self.add_item(btn)
        
        # أزرار التنقل (في الصف الخامس row=4)
        self.add_item(discord.ui.Button(label="⬅️", style=discord.ButtonStyle.primary, custom_id="prev", row=4))
        self.add_item(discord.ui.Button(label="إزالة الألوان", style=discord.ButtonStyle.danger, custom_id="remove", row=4))
        self.add_item(discord.ui.Button(label="➡️", style=discord.ButtonStyle.primary, custom_id="next", row=4))

    def make_callback(self, num):
        async def callback(interaction: discord.Interaction):
            await interaction.response.defer(ephemeral=True)
            role_name = f"لون {num}"
            role = discord.utils.get(interaction.guild.roles, name=role_name)
            
            # إنشاء الرتبة إذا لم تكن موجودة أو تحديث لونها
            if not role:
                role = await interaction.guild.create_role(name=role_name, color=COLORS[num-1])
            elif role.color.value != COLORS[num-1].value:
                await role.edit(color=COLORS[num-1])
            
            # إزالة الألوان القديمة للعضو
            for r in interaction.user.roles:
                if r.name.startswith("لون "): await interaction.user.remove_roles(r)
            
            await interaction.user.add_roles(role)
            msg = await interaction.followup.send(f"✅ تم تفعيل {role_name} بنجاح!", ephemeral=True)
            await asyncio.sleep(4)
            await msg.delete()
        return callback

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        cid = interaction.data.get("custom_id")
        if cid == "prev":
            self.page = max(0, self.page - 1)
            self.create_buttons()
            await interaction.response.edit_message(view=self)
        elif cid == "next":
            self.page = min(4, self.page + 1)
            self.create_buttons()
            await interaction.response.edit_message(view=self)
        elif cid == "remove":
            await interaction.response.defer(ephemeral=True)
            for r in interaction.user.roles:
                if r.name.startswith("لون "): await interaction.user.remove_roles(r)
            msg = await interaction.followup.send("❌ تم إزالة جميع الألوان!", ephemeral=True)
            await asyncio.sleep(4)
            await msg.delete()
        return True

@bot.event
async def on_ready():
    print(f"🚀 البوت {bot.user} يعمل الآن بنظام 50 لوناً!")

@bot.command()
async def لوحة(ctx):
    await ctx.send("👑 **نظام ألوان YONAN (50 لوناً) - اختر لونك المفضل:**", view=ColorPagination())

bot.run(TOKEN)
                    
