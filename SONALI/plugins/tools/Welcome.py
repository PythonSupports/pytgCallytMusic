#<<<<<<<<<<<<<<Krish>>>>>>>>>>>>>>#
import os
from PIL import ImageDraw, Image, ImageFont, ImageChops, Image
from pyrogram import Client, filters, enums
from pyrogram.types import *
from pyrogram.types import ChatMemberUpdated
from pyrogram.errors import PeerIdInvalid
from logging import getLogger
from SONALI import app

LOGGER = getLogger(__name__)

class WelDatabase:
    def __init__(self):
        self.data = set()

    async def find_one(self, chat_id):
        return chat_id in self.data

    async def add_wlcm(self, chat_id):
        self.data.add(chat_id)

    async def rm_wlcm(self, chat_id):
        self.data.discard(chat_id)

wlcm = WelDatabase()

class temp:
    MELCOW = {}

def circle(pfp, size=(500, 500)):
    pfp = pfp.resize(size, Image.LANCZOS).convert("RGBA")
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.LANCZOS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp

def welcomepic(pic, user, chatname, id, uname):
    background = Image.open("SONALI/assets/Kr.png")
    pfp = Image.open(pic).convert("RGBA")
    pfp = circle(pfp)
    pfp = pfp.resize((1157, 1158))
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype('SONALI/assets/font.ttf', size=110)
    draw.text((1800, 700), f'NAME: {user}', fill=(255, 255, 255), font=font)
    draw.text((1800, 830), f'ID: {id}', fill=(255, 255, 255), font=font)
    draw.text((1800, 965), f"USERNAME : {uname}", fill=(255, 255, 255), font=font)
    background.paste(pfp, (391, 336), pfp)
    output_path = f"downloads/welcome#{id}.png"
    background.save(output_path)
    return output_path

@app.on_message(filters.command("swel") & ~filters.private)
async def toggle_welcome(_, message):
    usage = "**ᴜsᴀɢᴇ:**\n**⦿ /swel [on|off]**"
    if len(message.command) == 1:
        return await message.reply_text(usage)

    chat_id = message.chat.id
    user = await app.get_chat_member(chat_id, message.from_user.id)
    if user.status not in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
        return await message.reply("**sᴏʀʀʏ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴄʜᴀɴɢᴇ ᴡᴇʟᴄᴏᴍᴇ sᴇᴛᴛɪɴɢs.**")

    state = message.text.split(None, 1)[1].strip().lower()
    if state == "on":
        await wlcm.add_wlcm(chat_id)
        await message.reply_text(f"**ᴇɴᴀʙʟᴇᴅ ᴡᴇʟᴄᴏᴍᴇ ɪɴ {message.chat.title}**")
    elif state == "off":
        await wlcm.rm_wlcm(chat_id)
        await message.reply_text(f"**ᴅɪsᴀʙʟᴇᴅ ᴡᴇʟᴄᴏᴍᴇ ɪɴ {message.chat.title}**")
    else:
        await message.reply_text(usage)

@app.on_chat_member_updated()
async def greet_user(_, member: ChatMemberUpdated):
    chat_id = member.chat.id
    if not await wlcm.find_one(chat_id):
        return
    if member.old_chat_member.status not in ["left", "kicked"]:
        return
    if member.new_chat_member.status not in ["member"]:
        return

    user = member.new_chat_member.user
    try:
        photos = await app.get_profile_photos(user.id, limit=1)
        if photos:
            pic_path = await app.download_media(photos[0].file_id, file_name=f"downloads/pp{user.id}.png")
        else:
            pic_path = "SONALI/assets/upic.png"
    except Exception:
        pic_path = "SONALI/assets/upic.png"

    welcome_img = welcomepic(pic_path, user.first_name, member.chat.title, user.id, user.username or "None")
    try:
        temp.MELCOW[f"welcome-{chat_id}"] = await app.send_photo(
            chat_id,
            photo=welcome_img,
            caption=f"""
❣️𝐖ᴇʟᴄᴏᴍᴇ 𝐓ᴏ {member.chat.title} ❣️

● 𝐍ᴀᴍᴇ ➥ {user.mention} 
● 𝐔ꜱᴇʀɴᴀᴍᴇ ➥ @{user.username or 'None'}

┏━━━━━━━━━━━━━━━
┣ 𝟏 ➥ ᴅᴏɴᴛ ᴀʙᴜsᴇ
┣ 𝟐 ➥ ʀᴇsᴘᴇᴄᴛ ᴇᴠᴇʀʏᴏɴᴇ
┣ 𝟑 ➥ ʟɪɴᴋs ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ
┣ 𝟒 ➥ ɴᴏ 18+ sᴛᴜғғ
┗━━━━━━━━━━━━━━━

❖ ᴍᴀᴅᴇ ʙʏ [𝐊ʀɪsʜ 𝐌ᴜsɪᴄ](https://t.me/krishnetwork)
""",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("𝐀ᴅᴅ 𝐌ᴇ 𝐁ᴀʙʏ", url="https://t.me/syn_ixbot?startgroup=true")]
            ])
        )
    except Exception as e:
        LOGGER.error(f"Welcome error: {e}")
    try:
        os.remove(welcome_img)
        if os.path.exists(pic_path):
            os.remove(pic_path)
    except Exception:
        pass
