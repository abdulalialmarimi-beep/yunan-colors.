import os
import discord
import asyncio
import random
from discord.ext import commands
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home(): return "البوت يعمل 24/7!"
Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()

TOKEN = os.environ.get("TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="#", intents=intents)

class ColorView(discord.ui.View):
    def __init__(self, page=0):
        super().__init__(timeout=None)
        self.page = page
        self.update_buttons()

    def update_buttons(self):
        self.clear_items()
        start = (self.page * 10) + 1
        for i in range(start, start + 10):
            btn = discord.ui.Button(label=str(i), style=discord.ButtonStyle.secondary, custom_id=f"color_{i}")
            btn.callback = self.make_callback(i)
            self.add_item(btn)
        self.add_item(discord.ui.Button(label="⬅️", style=discord.ButtonStyle.primary, custom_id="prev", row=4))
        self.add_item(discord.ui.Button(label="❌ إزالة", style=discord.ButtonStyle.danger, custom_id="remove", row=4))
        self.add_item(discord.ui.Button(label="➡️", style=discord.ButtonStyle.primary, custom_id="next", row=4))

    def make_callback(self, i):
        async def callback(interaction: discord.Interaction):
            role_name = f"رول {i}"
            # البحث عن الرولة أو إنشاؤها تلقائياً إذا لم توجد
            role = discord.utils.get(interaction.guild.roles, name=role_name)
            if not role:
                # إنشاء رولة جديدة بلون عشوائي إذا لم تكن موجودة
                color = discord.Color(random.randint(0, 0xFFFFFF))
                role = await interaction.guild.create_role(name=role_name, color=color)
            
            # إزالة الرولات القديمة
            for n in range(1, 51):
                old_role = discord.utils.get(interaction.guild.roles, name=f"رول {n}")
                if old_role in interaction.user.roles:
                    await interaction.user.remove_roles(old_role)
            
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"✅ تم تفعيل: {role_name}", ephemeral=True)
            await asyncio.sleep(4)
            try: await interaction.delete_original_response()
            except: pass
        return callback

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        cid = interaction.data.get("custom_id")
        if cid == "prev": self.page = max(0, self.page - 1)
        elif cid == "next": self.page = min(4, self.page + 1)
        elif cid == "remove":
            for n in range(1, 51):
                role = discord.utils.get(interaction.guild.roles, name=f"رول {n}")
                if role in interaction.user.roles: await interaction.user.remove_roles(role)
            await interaction.response.send_message("❌ تمت إزالة الألوان", ephemeral=True)
            await asyncio.sleep(4)
            try: await interaction.delete_original_response()
            except: pass
            return True
        self.update_buttons()
        await interaction.response.edit_message(view=self)
        return True

@bot.command()
@commands.has_permissions(administrator=True)
async def ارسال_اللوحة(ctx):
    image_url = "https://cdn.discordapp.com/attachments/801930633635037194/1512226140025131070/1000099891.jpg"
    embed = discord.Embed(title="👑 نظام ألوان YONAN", description="اضغط الرقم المطلوب (سيتم إنشاء الرولة تلقائياً):")
    embed.set_image(url=image_url)
    await ctx.send(embed=embed, view=ColorView())

bot.run(TOKEN)
        
