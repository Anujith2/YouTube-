import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from yt_dlp import YoutubeDL

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("yt_quality_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    await message.reply_text("👋 **ഹലോ! യൂട്യൂബ് വീഡിയോ ലിങ്ക് അയച്ചു തരൂ, ക്വാളിറ്റി സെലക്ട് ചെയ്യാൻ ബട്ടണുകൾ ലഭിക്കും.**")

@app.on_message(filters.regex(r'https?://(?:www\.)?youtube\.com|youtu\.be') & filters.private)
async def youtube_link(client, message):
    url = message.text.strip()
    
    # ക്വാളിറ്റി തെരഞ്ഞെടുക്കാനുള്ള ബട്ടണുകൾ
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎬 1080p", callback_data=f"dl|1080|{url}"),
            InlineKeyboardButton("🎬 720p", callback_data=f"dl|720|{url}")
        ],
        [
            InlineKeyboardButton("🎬 480p", callback_data=f"dl|480|{url}"),
            InlineKeyboardButton("🎵 Audio (MP3)", callback_data=f"dl|audio|{url}")
        ]
    ])
    
    await message.reply_text("👇 **ദയവായി ആവശ്യമുള്ള ക്വാളിറ്റി സെലക്ട് ചെയ്യുക:**", reply_markup=keyboard)

@app.on_callback_query(filters.regex(r"^dl\|"))
async def download_callback(client, callback_query: CallbackQuery):
    data_parts = callback_query.data.split("|", 2)
    quality = data_parts[1]
    url = data_parts[2]
    
    await callback_query.message.edit_text(f"📥 **Downloading ({quality}) from YouTube... Please wait.**")
    
    # yt-dlp ഫോർമാറ്റ് സെറ്റിങ്സ്
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

    ydl_opts = {
        'format': fmt,
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
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

    except Exception as e:
        await callback_query.message.edit_text(f"❌ **Error:** `{e}`")

if __name__ == "__main__":
    app.run()

