import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from yt_dlp import YoutubeDL

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("yt_quality_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

os.makedirs("downloads", exist_ok=True)
URL_STORE = {}

@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    welcome_text = (
        "👋 **ഹലോ! ഞാൻ ഒരു യൂട്യൂബ് വീഡിയോ ഡൗൺലോഡ് ബോട്ടാണ്.**\n\n"
        "🎬 ഏത് യൂട്യൂബ് ലിങ്കും നേരിട്ട് അയച്ചു തരൂ (അല്ലെങ്കിൽ /ytdl <link>), "
        "ഞാൻ ക്വാളിറ്റി ബട്ടണുകൾ തരാം."
    )
    await message.reply_text(welcome_text)

# ലിങ്ക് മാത്രം അയക്കുമ്പോഴും /ytdl ലിങ്ക് എന്ന് അയക്കുമ്പോഴും വർക്ക് ചെയ്യാൻ
@app.on_message(filters.regex(r'https?://(?:www\.)?youtube\.com|youtu\.be') | filters.command("ytdl"))
async def youtube_link(client, message):
    # /ytdl കമാൻഡ് ആണെങ്കിൽ ലിങ്ക് എടുക്കാൻ
    if message.command:
        if len(message.command) > 1:
            url = message.command[1]
        else:
            await message.reply_text("⚠️ ദയവായി ലിങ്ക് കൂടെ നൽകുക. (ഉദാഹരണത്തിന്: `/ytdl <link>` അല്ലെങ്കിൽ നേരിട്ട് ലിങ്ക് അയക്കുക)")
            return
    else:
        url = message.text.strip()

    msg_id = message.id
    URL_STORE[msg_id] = url
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎬 1080p", callback_data=f"dl|1080|{msg_id}"),
            InlineKeyboardButton("🎬 720p", callback_data=f"dl|720|{msg_id}")
        ],
        [
            InlineKeyboardButton("🎬 480p", callback_data=f"dl|480|{msg_id}"),
            InlineKeyboardButton("🎵 Audio (MP3)", callback_data=f"dl|audio|{msg_id}")
        ]
    ])
    
    await message.reply_text("👇 **ദയവായി ആവശ്യമുള്ള ക്വാളിറ്റി സെലക്ട് ചെയ്യുക:**", reply_markup=keyboard)

@app.on_callback_query(filters.regex(r"^dl\|"))
async def download_callback(client, callback_query: CallbackQuery):
    data_parts = callback_query.data.split("|")
    quality = data_parts[1]
    msg_id = int(data_parts[2])
    
    url = URL_STORE.get(msg_id)
    if not url:
        await callback_query.answer("❌ URL expired! Please send the link again.", show_alert=True)
        return

    await callback_query.message.edit_text(f"📥 **Downloading ({quality}) from YouTube... Please wait.**")
    
    if quality == "1080":
        fmt = 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best'
    elif quality == "720":
        fmt = 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best'
    elif quality == "480":
        fmt = 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best'
    elif quality == "audio":
        fmt = 'bestaudio/best'
    else:
        fmt = 'best'

    # യൂട്യൂബ് ബോട്ട് പരിശോധന ഒഴിവാക്കാനുള്ള എക്സ്ട്രാ ഓപ്ഷനുകൾ
    ydl_opts = {
        'format': fmt,
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
    }

    try:
        loop = asyncio.get_event_loop()
        def extract():
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                return info, filename

        info, file_path = await loop.run_in_executor(None, extract)
        title = info.get("title", "YouTube Video")
        
        await callback_query.message.edit_text("📤 **Uploading to Telegram...**")

        if quality == "audio":
            await callback_query.message.reply_audio(audio=file_path, caption=f"🎵 **{title}**")
        else:
            await callback_query.message.reply_video(video=file_path, caption=f"🎬 **{title}** ({quality}p)", supports_streaming=True)

        if os.path.exists(file_path):
            os.remove(file_path)
            
        await callback_query.message.delete()
        
        if msg_id in URL_STORE:
            del URL_STORE[msg_id]

    except Exception as e:
        await callback_query.message.edit_text(f"❌ **Error:** `{e}`")

if __name__ == "__main__":
    app.run()
    
