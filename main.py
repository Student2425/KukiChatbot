from pyrogram import Client, filters
from pyrogram.types import *
from pymongo import MongoClient
import requests
import os
import re


API_ID = os.environ.get("24311411", None) 
API_HASH = os.environ.get("886b01d1d7beb0d1609274f0ff381271", None) 
BOT_TOKEN = os.environ.get("7369123789:AAEh2AmhtOUncqAeSwpqMcNh8GyJoqaKX6Q", None) 
KUKI_API = os.environ.get("KUKI_API", None) 
ERROR_LOG = os.environ.get("ERROR_LOG", None) 
MONGO_URL = os.environ.get("MONGO_URL", None)


bot = Client(
    "KukiBot" ,
    api_id = API_ID,
    api_hash = API_HASH ,
    bot_token = BOT_TOKEN
)

async def is_admins(chat_id: int):
    return [
        member.user.id
        async for member in bot.iter_chat_members(
            chat_id, filter="administrators"
        )
    ]


@bot.on_message(
    filters.command("setupchat", prefixes=["/", ".", "?", "-"])
    & ~filters.private)
async def addchat(_, message): 
    kukidb = MongoClient(MONGO_URL)
    
    kuki = kukidb["KukiDb"]["Kuki"] 
    if message.from_user:
        user = message.from_user.id
        chat_id = message.chat.id
        if user not in (
            await is_admins(chat_id)
        ):
            return await message.reply_text(
                "You are not admin"
            )
    is_kuki = kuki.find_one({"chat_id": message.chat.id})
    if not is_kuki:
        kuki.insert_one({"chat_id": message.chat.id})
        await message.reply_text(f"✅ | Successfully\nKuki Chatbot of this Group is set to @{message.chat.username}\n Requested by [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n© @MetaVoid")
    else:
        await message.reply_text(f"Already Setup Kuki Chatbot of this Group Is @{message.chat.username}")


@bot.on_message(
    filters.command("removechat", prefixes=["/", ".", "?", "-"])
    & ~filters.private)
async def rmchat(_, message): 
    kukidb = MongoClient(MONGO_URL)
    
    kuki = kukidb["KukiDb"]["Kuki"] 
    if message.from_user:
        user = message.from_user.id
        chat_id = message.chat.id
        if user not in (
            await is_admins(chat_id)
        ):
            return await message.reply_text(
                "You are not admin"
            )
    is_kuki = kuki.find_one({"chat_id": message.chat.id})
    if not is_kuki:
        await message.reply_text("Already Kuki ChatBot Disable")
    else:
        kuki.delete_one({"chat_id": message.chat.id})
        await message.reply_text("✅ | Kuki Chatbot is disable!")





@bot.on_message(
    filters.text
    & filters.reply
    & ~filters.private
    & ~filters.bot
    & ~filters.edited,
    group=2,
)
async def kukiai(client: Client, message: Message):

   kukidb = MongoClient(MONGO_URL)
    
   kuki = kukidb["KukiDb"]["Kuki"] 

   is_kuki = kuki.find_one({"chat_id": message.chat.id})
   if is_kuki:
       if message.reply_to_message:      
           botget = await bot.get_me()
           botid = botget.id
           if not message.reply_to_message.from_user.id == botid:
               return
           await bot.send_chat_action(message.chat.id, "typing")
           if not message.text:
               msg = "/"
           else:
               msg = message.text
           try: 
               x = requests.get(f"https://kukiapi.xyz/api/apikey={KUKI_API}/message={msg}").json()
               x = x['reply']
               await asyncio.sleep(1)
           except Exception as e:
               error = str(e)
           await message.reply_text(x)
           await bot.send_message(
           ERROR_LOG, f"""{error}""")
           await bot.send_chat_action(message.chat.id, "cencel") 
   


@bot.on_message(
    filters.text
    & filters.reply
    & filters.private
    & ~filters.bot
    & ~filters.edited,
    group=2,
)
async def kukiai(client: Client, message: Message):
    await bot.send_chat_action(message.chat.id, "typing")
    if not message.text:
        msg = "/"
    else:
        msg = message.text
    try:
        x = requests.get(f"https://kukiapi.xyz/api/apikey={KUKI_API}/message={msg}").json()
        x = x['reply']
        await asyncio.sleep(1)
    except Exception as e:
        ERROR = str(e)
    await message.reply_text(x)
    await bot.send_message(
           ERROR_LOG, f"""{ERROR}""")
    await bot.send_chat_action(message.chat.id, "cancel")



@bot.on_message(
    filters.command("chat", prefixes=["/", ".", "?", "-"]))
async def kukiai(client: Client, message: Message):
    await bot.send_chat_action(message.chat.id, "typing")
    if not message.text:
        msg = "/"
    else:
        msg = message.text.replace(message.text.split(" ")[0], "")
    try:
        x = requests.get(f"https://kukiapi.xyz/api/apikey={KUKI_API}/message={msg}").json()
        x = x['reply']
        await asyncio.sleep(1)
    except Exception as e:
        ERROR = str(e)
    await bot.send_message(
           ERROR_LOG, f"""{ERROR}""")
    await message.reply_text(x)
    





@bot.on_message(filters.command(["start"], prefixes=["/", "!"]))
async def start(client, message):
    self = await bot.get_me()
    busername = self.username
    if message.chat.type != "private":
        buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Click here",
                url=f"t.me/Kukichttiiie_bot?start")]])
        await message.reply("Contact me in PM",
                            reply_markup=buttons)
        
    else:
        buttons = [[InlineKeyboardButton("Support", url="https://t.me/Simply_sweetheart04"),
                    InlineKeyboardButton("Channel", url="https://t.me/unwanted_Infundibulum"),
                    InlineKeyboardButton("Repo", url="Khikhikhi 🤭 nhi milega ")
        Photo = "https://telegra.ph/file/b04509cc8486f23690bba.jpg"
        await message.reply_photo(Photo, caption=f"Hello [{message.from_user.first_name}](tg://user?id={message.from_user.id}), Machine Learning Chat Bot that can talk about any topic in any language\n /help - Help Commands\n Powered By @Welcome to Gboard clipboard, any text you copy will be saved here.powered by @Simply_sweetheart0_016, reply_markup=InlineKeyboardMarkup(buttons))



@bot.on_message(filters.command(["help"], prefixes=["/", "!"]))
async def help(client, message):
    self = await bot.get_me()
    busername = self.username
    if message.chat.type != "private":
        buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Click here",
                url=f"t.me/kukichatbot?start=help_")]])
        await message.reply("Contact me in PM",
                            reply_markup=buttons)
        
    else:    
        await message.reply_text("/start - Start The Bot\n/chat - Send a message to this bot\n/setupchat - Active Kuki Chatbot In Group\n/removechat - Disable Kuki Chatbot In Group")






bot.run()

