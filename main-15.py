import os
import asyncio
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# ─── سيرفر Flask لإبقاء البوت حياً ───────────────────────────────────────────

app = Flask('')

@app.route('/')
def home():
    return "البوت يعمل! ✅"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run_flask, daemon=True).start()

# ─── إعدادات البوت ────────────────────────────────────────────────────────────

TOKEN = os.environ.get("TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="-", intents=intents)

# ─── قاموس الألوان ────────────────────────────────────────────────────────────

COLORS = {
    1:  ("أحمر صارخ",        0xFF0000),
    2:  ("أحمر برتقالي",     0xFF2200),
    3:  ("برتقالي أحمر",     0xFF4400),
    4:  ("برتقالي",          0xFF6600),
    5:  ("برتقالي ذهبي",     0xFF8800),
    6:  ("ذهبي",             0xFFAA00),
    7:  ("أصفر ذهبي",        0xFFCC00),
    8:  ("أصفر",             0xFFFF00),
    9:  ("أصفر مخضر",        0xCCFF00),
    10: ("أخضر مصفر",        0x99FF00),
    11: ("أخضر فاتح",        0x66FF00),
    12: ("أخضر عشبي",        0x44CC00),
    13: ("أخضر",             0x00AA00),
    14: ("أخضر غامق",        0x006600),
    15: ("أخضر زمردي",       0x00AA55),
    16: ("أخضر بحري",        0x00AA77),
    17: ("أخضر مائي",        0x00BBAA),
    18: ("سماوي",            0x00CCCC),
    19: ("سماوي فاتح",       0x00DDEE),
    20: ("أزرق سماوي",       0x00BBFF),
    21: ("أزرق فاتح",        0x33AAFF),
    22: ("أزرق",             0x0077FF),
    23: ("أزرق ملكي",        0x0044FF),
    24: ("أزرق نيلي",        0x0022CC),
    25: ("نيلي",             0x0000FF),
    26: ("أزرق بنفسجي",      0x2200FF),
    27: ("بنفسجي مزرق",      0x4400FF),
    28: ("بنفسجي فاتح",      0x6600FF),
    29: ("بنفسجي",           0x8800FF),
    30: ("بنفسجي غامق",      0xAA00DD),
    31: ("أرجواني",          0xBB00AA),
    32: ("أرجواني فاتح",     0xCC00BB),
    33: ("وردي بنفسجي",      0xDD00CC),
    34: ("وردي غامق",        0xFF0088),
    35: ("وردي",             0xFF0066),
    36: ("وردي فاتح",        0xFF3388),
    37: ("وردي زاهي",        0xFF1493),
    38: ("وردي مائل للأحمر", 0xFF2244),
    39: ("أحمر وردي",        0xFF3355),
    40: ("أحمر فاتح",        0xFF4455),
    41: ("مرجاني",           0xFF6B6B),
    42: ("خوخي",             0xFFAA88),
    43: ("رملي",             0xDDBB88),
    44: ("كريمي",            0xFFEECC),
    45: ("بيج",              0xF5DEB3),
    46: ("رمادي فاتح",       0xCCCCCC),
    47: ("رمادي مزرق",       0x99AABB),
    48: ("رمادي أرجواني",    0xAA99BB),
    49: ("رمادي غامق",       0x555555),
    50: ("أسود مخملي",       0x111111),
}

# ─── إنشاء الرتب مسبقاً عند تشغيل البوت ──────────────────────────────────────

async def create_all_roles(guild: discord.Guild):
    for num, (name, hex_color) in COLORS.items():
        role = discord.utils.get(guild.roles, name=str(num))
        if not role:
            try:
                await guild.create_role(
                    name=str(num),
                    color=discord.Color(hex_color)
                )
                await asyncio.sleep(0.3)
            except Exception as e:
                print(f"[خطأ إنشاء رتبة {num}] {e}")

@bot.event
async def on_ready():
    print(f"✅ البوت شغال: {bot.user} | السيرفرات: {len(bot.guilds)}")
    for guild in bot.guilds:
        print(f"⚙️ جاري إنشاء الرتب في: {guild.name}")
        await create_all_roles(guild)
        print(f"✅ تم إنشاء الرتب في: {guild.name}")

@bot.event
async def on_guild_join(guild: discord.Guild):
    await create_all_roles(guild)

# ─── أمر عرض الألوان ──────────────────────────────────────────────────────────

COLORS_IMAGE_URL = "https://i.ibb.co/C3b0kvCS/563-E3-AF2-F2-AB-411-C-8543-DFA49-E60-A8-C3.jpg"

@bot.command(name="الوان")
async def show_colors(ctx):
    try:
        await ctx.message.delete()
    except:
        pass

    embed = discord.Embed(description="🎨 لاختيار لونك يرجى استخدام أمر `-لون`", color=0x2b2d31)
    embed.set_image(url=COLORS_IMAGE_URL)
    await ctx.send(embed=embed)

# ─── أمر تفعيل اللون ──────────────────────────────────────────────────────────

@bot.command(name="لون")
async def set_color(ctx, num: int = None):
    try:
        await ctx.message.delete()
    except:
        pass

    if num is None or num not in COLORS:
        await ctx.send(
            f"❌ رقم غير صحيح! اختر رقم من 1 إلى 50\nمثال: `-لون 15`",
            delete_after=7
        )
        return

    arabic_name, hex_color = COLORS[num]
    role_name = str(num)

    try:
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if not role:
            role = await ctx.guild.create_role(
                name=role_name,
                color=discord.Color(hex_color)
            )

        # إزالة الألوان القديمة
        roles_to_remove = [
            discord.utils.get(ctx.guild.roles, name=str(n))
            for n in COLORS
        ]
        roles_to_remove = [r for r in roles_to_remove if r and r in ctx.author.roles]
        if roles_to_remove:
            await ctx.author.remove_roles(*roles_to_remove)

        await ctx.author.add_roles(role)
        await ctx.send(
            f"✅ تم تفعيل اللون **{arabic_name}** ({num}) لـ {ctx.author.mention}",
            delete_after=5
        )

    except discord.Forbidden:
        await ctx.send("❌ البوت ما عنده صلاحية لتعديل الرتب!", delete_after=5)
    except Exception as e:
        print(f"[خطأ set_color] {e}")
        await ctx.send("❌ صار خطأ، جرب مرة ثانية.", delete_after=5)

# ─── أمر إزالة اللون ──────────────────────────────────────────────────────────

@bot.command(name="ازالة")
async def remove_color(ctx):
    try:
        await ctx.message.delete()
    except:
        pass

    try:
        roles_to_remove = [
            discord.utils.get(ctx.guild.roles, name=str(n))
            for n in COLORS
        ]
        roles_to_remove = [r for r in roles_to_remove if r and r in ctx.author.roles]

        if roles_to_remove:
            await ctx.author.remove_roles(*roles_to_remove)
            await ctx.send(
                f"❌ تمت إزالة اللون من {ctx.author.mention}",
                delete_after=5
            )
        else:
            await ctx.send(
                f"⚠️ ما عندك لون مفعّل أصلاً {ctx.author.mention}",
                delete_after=5
            )

    except discord.Forbidden:
        await ctx.send("❌ البوت ما عنده صلاحية!", delete_after=5)
    except Exception as e:
        print(f"[خطأ remove_color] {e}")
        await ctx.send("❌ صار خطأ، جرب مرة ثانية.", delete_after=5)

# ─── معالجة الأخطاء ───────────────────────────────────────────────────────────

ALLOWED_CHANNEL_ID = 1497594613794345182

@bot.check
async def only_allowed_channel(ctx):
    return ctx.channel.id == ALLOWED_CHANNEL_ID

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        return  # تجاهل بصمت في القنوات الثانية
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ ما عندك صلاحية لهذا الأمر!", delete_after=5)
    elif isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ اكتب رقم صحيح! مثال: `-لون 15`", delete_after=5)
    else:
        print(f"[خطأ أمر] {error}")

# ─── تشغيل البوت ──────────────────────────────────────────────────────────────

if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ TOKEN غير موجود في المتغيرات البيئية!")
