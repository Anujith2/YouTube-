from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# സപ്പോർട്ട് ഗ്രൂപ്പ് ഐഡി
SUPPORT_GROUP_ID = -1002238061487

# ചാനലുകളും എപ്പിസോഡുകളുമായി ബന്ധപ്പെട്ട കീവേഡുകൾ
CHANNEL_KEYWORDS = [
    "today episode", "today's episode", "yesterday episode", 
    "asianet", "zee keralam", "mazhavil manorama", "surya tv"
]

# എല്ലാ സീരിയലുകളുടെയും ലിസ്റ്റ്
SERIALS_LIST = [
    "kanmashi", "karnan", "valyettan", "pranayavilasam", "durga", "chembarathy", 
    "saregamapa", "saregamapa lil champs", "kudumbasametham", "meghasandhesham", 
    "seethayanam", "krishnagadha", "meghasandesam", "aval arundhati", "akale", 
    "snehapoorvam shyama", "mangalyam", "manathe kottaram", "ashwathi nakshatram", 
    "kudumbashree sharada", "bigg boss", "taste time", "sindhu bhairavi", 
    "comedy cooks", "ivar vivahitharayal", "oru kochu swapnam", "advocate anjali", 
    "kattathe kilikoodu", "ee puzhayum kadannu", "sindoorapottu", "star singer", 
    "teacheramma", "mazha thorum munpe", "pavithram", "ishtam mathram", 
    "santhwanam", "snehakkoottu", "mounaragam", "patharamattu", "amma manassu", 
    "chempaneer poovu", "dharmma yoddhavu garudan", "othiri othiri swapnangal", 
    "ottashikharam", "archana chechi llb", "super kanmani", "marimayam", 
    "oru chiri iru chiri bumper chiri", "the great family challenge", "roopavathi", 
    "thenmavin kombath", "punnaram", "anju sundarikal", "amme mookambike", 
    "peythozhiyathe", "chattambipparu", "hridayam", "kanyadaanam", 
    "swayamavarapanthal", "mangalyam thanthunanena"
]

@Client.on_message(filters.text & ~filters.private, group=-1)
async def serial_restriction_handler(client, message):
    if message.chat.id != SUPPORT_GROUP_ID:
        return
        
    text = message.text.lower().strip()
    user_name = message.from_user.first_name if message.from_user else "User"
    
    # 1. Hi / Hello greetings handler
    hi_keywords = ["hi", "hello", "hlo", "hai"]
    if any(word == text for word in hi_keywords):
        reply_text = (
            f"<b>Hello 👋 {user_name}\n\n"
            f"Welcome To Allu TV Serial ❤️\n"
            f"How are you doing today? 🥰\n\n"
            f"Team 🥰👇\n"
            f"@Anujith1238 , @Arunya18</b>"
        )
        await message.reply_text(reply_text)
        return message.stop_propagation()

    # 2. GM / Good Morning / Good Night / Good Evening handler
    if "good morning" in text or text == "gm":
        await message.reply_text(f"<b>Good Morning, {user_name} 🌅 Have a wonderful day ahead! 🥰</b>")
        return message.stop_propagation()
    elif "good night" in text:
        await message.reply_text(f"<b>Good Night, {user_name} 🌙 Sweet dreams! ✨</b>")
        return message.stop_propagation()
    elif "good evening" in text:
        await message.reply_text(f"<b>Good Evening, {user_name} 🌆 Hope you had a great day! 👍</b>")
        return message.stop_propagation()

    # 3. Urgent / Help handler
    urgent_keywords = ["urgent", "help", "emergency", "support"]
    if any(keyword in text for keyword in urgent_keywords):
        reply_text = (
            f"<b>Hello {user_name},\n\n"
            f"You can contact me if you have any urgent matters. 🥰\n\n"
            f"@Anujith1238\n\n"
            f"There will be all support from our side.\n\n"
            f"Best regards,\n"
            f"ALLU Team ✅</b>"
        )
        await message.reply_text(reply_text)
        return message.stop_propagation()

    # 4. Today/Yesterday episodes or channels handler
    if any(keyword in text for keyword in CHANNEL_KEYWORDS):
        reply_text = (
            "<b>Ok bro ❤️\n\n"
            "It will be uploaded when the admin sees it ❤️\n\n"
            "Waiting until then... 🥰</b>"
        )
        await message.reply_text(reply_text)
        return message.stop_propagation()

    # 5. Serials list handler
    if any(serial in text for serial in SERIALS_LIST):
        reply_text = (
            f"<b>Hello {user_name},\n\n"
            f"This is just a support group! ⚠️\n"
            f"If you want serials, please ask in the group below: 👇</b>"
        )
        
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("👉 Click Here To Join Group 👈", url="https://t.me/AlluTvSerialGroup")]
        ])
        
        await message.reply_text(reply_text, reply_markup=buttons)
        return message.stop_propagation()
