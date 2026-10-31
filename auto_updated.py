import re
import asyncio
from collections import defaultdict
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode

# ==========================================
# BOT SETTINGS
# ==========================================

CHANNELS = [-1002015288592]
AUTH_CHANNEL = -1002110922261
BOT_USERNAME = "Anujith1bot"
BANNER_PHOTO = "https://ibb.co/cS5zrTGD"


# ==========================================
# SERIAL MAPPING
# ==========================================

SERIALS_MAPPING = {
    "kanmashi": "Kanmashi",
    "karnan": "Karnan",
    "valyettan": "Valyettan",
    "pranayavilasam": "Pranayavilasam",
    "durga": "Durga",
    "chembarathy": "Chembarathy",
    "saregamapa": "SaReGaMaPa",
    "saregamapa_lil_champs": "SaReGaMaPa Lil Champs",
    "kudumbasametham": "Kudumbasametham",
    "meghasandhesham": "Meghasandhesham",
    "seethayanam": "Seethayanam",
    "krishnagadha": "Krishnagadha",
    "meghasandesam": "Meghasandesam",
    "aval_arundhati": "Aval Arundhati",
    "akale": "Akale",
    "snehapoorvam_shyama": "Snehapoorvam Shyama",
    "mangalyam": "Mangalyam",
    "manathe_kottaram": "Manathe Kottaram",
    "ashwathi_nakshatram": "Ashwathi Nakshatram",
    "kudumbashree_sharada": "Kudumbashree Sharada",
    "bigg_boss": "Bigg Boss",
    "taste_time": "Taste Time",
    "sindhu_bhairavi": "Sindhu Bhairavi",
    "comedy_cooks": "Comedy Cooks",
    "ivar_vivahitharayal": "Ivar Vivahitharayal",
    "oru_kochu_swapnam": "Oru Kochu Swapnam",
    "advocate_anjali": "Advocate Anjali",
    "kattathe_kilikoodu": "Kattathe Kilikoodu",
    "ee_puzhayum_kadannu": "Ee Puzhayum Kadannu",
    "sindoorapottu": "Sindoorapottu",
    "star_singer": "Star Singer",
    "teacheramma": "Teacheramma",
    "mazha_thorum_munpe": "Mazha Thorum Munpe",
    "pavithram": "Pavithram",
    "ishtam_mathram": "Ishtam Mathram",
    "santhwanam": "Santhwanam 2",
    "snehakkoottu": "Snehakkoottu",
    "mounaragam": "Mounaragam",
    "patharamattu": "Patharamattu",
    "amma_manassu": "Amma Manassu",
    "chempaneer_poovu": "Chempaneer Poovu",
    "dharmma_yoddhavu_garudan": "Dharmma Yoddhavu Garudan",
    "othiri_othiri_swapnangal": "Othiri Othiri Swapnangal",
    "ottashikharam": "Ottashikharam",
    "archana_chechi_llb": "Archana Chechi LLB",
    "super_kanmani": "Super Kanmani",
    "marimayam": "Marimayam",
    "oru_chiri_iru_chiri_bumper_chiri":
        "Oru Chiri Iru Chiri Bumper Chiri",
    "the_great_family_challenge": "The Great Family Challenge",
    "roopavathi": "Roopavathi",
    "thenmavin_kombath": "Thenmavin Kombath",
    "punnaram": "Punnaram",
    "anju_sundarikal": "Anju Sundarikal",
    "amme_mookambike": "Amme Mookambike",
    "peythozhiyathe": "Peythozhiyathe",
    "chattambipparu": "Chattambipparu",
    "hridayam": "Hridayam",
    "kanyadaanam": "Kanyadaanam",
    "swayamavarapanthal": "Swayamavarapanthal",
    "mangalyam_thanthunanena": "Mangalyam Thanthunanena",
    "mukhachithram": "Mukhachithram",
}


# ==========================================
# VIDEO QUALITY PATTERN
# ==========================================

QUALITY_PATTERN = r"(?<!\d)(\d{3,4})\s*[pP](?!\w)"


# ==========================================
# GET ORIGINAL FILE NAME
# ==========================================

def get_file_name(message):
    if message.document:
        return message.document.file_name or "Media File"

    if message.video:
        return message.video.file_name or "Media File"

    return "Media File"


# ==========================================
# FIND SERIAL NAME
# ==========================================

def find_serial_name(filename):
    normalized = re.sub(r"[._-]+", " ", filename.lower())
    normalized = re.sub(r"\s+", " ", normalized).strip()

    mapping_items = sorted(
        SERIALS_MAPPING.items(),
        key=lambda item: len(item[0]),
        reverse=True
    )

    for key, display_name in mapping_items:
        search_name = key.replace("_", " ").lower()

        pattern = (
            r"(?<!\w)"
            + re.escape(search_name)
            + r"(?!\w)"
        )

        if re.search(pattern, normalized):
            return display_name

    return clean_unknown_name(filename)


# ==========================================
# CLEAN UNKNOWN SERIAL NAME
# ==========================================

def clean_unknown_name(filename):
    name = re.sub(
        r"\.(mkv|mp4|avi|mov|webm|m4v|mpeg|mpg)$",
        "",
        filename,
        flags=re.IGNORECASE
    )

    name = re.sub(
        r"\bS\d+[ ._-]*E(?:P(?:ISODE)?)?[ ._-]*\d+"
        r"(?:[ ._-]*-[ ._-]*E?\d+)?",
        "",
        name,
        flags=re.IGNORECASE
    )

    name = re.sub(
        r"\bSeason[ ._-]*\d+\b",
        "",
        name,
        flags=re.IGNORECASE
    )

    name = re.sub(
        r"\bEpisode[ ._-]*\d+(?:[ ._-]*-[ ._-]*\d+)?",
        "",
        name,
        flags=re.IGNORECASE
    )

    name = re.sub(
        QUALITY_PATTERN,
        "",
        name,
        flags=re.IGNORECASE
    )

    name = re.sub(
        r"\b(HS|WEB|WEB-DL|HDRIP|HDTV|X264|X265)\b",
        "",
        name,
        flags=re.IGNORECASE
    )

    name = re.sub(r"[._]+", " ", name)
    name = re.sub(r"\s+", " ", name)

    return name.strip(" -_.") or "Malayalam Serial"


# ==========================================
# GET SEASON
# ==========================================

def get_season(filename):

    match = re.search(
        r"(?<![A-Za-z0-9])S(\d+)\s*E\d+",
        filename,
        re.IGNORECASE
    )

    if match:
        return match.group(1).zfill(2)

    match = re.search(
        r"\bSeason[ ._-]*(\d+)\b",
        filename,
        re.IGNORECASE
    )

    if match:
        return match.group(1).zfill(2)

    match = re.search(
        r"(?<![A-Za-z0-9])S(\d{1,2})(?![A-Za-z0-9])",
        filename,
        re.IGNORECASE
    )

    if match:
        return match.group(1).zfill(2)

    return "01"


# ==========================================
# GET VIDEO QUALITY FROM FILENAME ONLY
# ==========================================

def get_quality(filename, message=None):
    # Filename quality takes priority. Return only one exact quality tag;
    # do not join multiple matches or print duplicate quality labels.
    match = re.search(QUALITY_PATTERN, filename, re.IGNORECASE)
    if match:
        return f"{match.group(1)}p"

    # Support common aliases while keeping the output in the same format.
    normalized = filename.lower()
    if re.search(r"(?<!\\w)4k(?!\\w)", normalized):
        return "2160p"
    if re.search(r"(?<!\\w)fhd(?!\\w)", normalized):
        return "1080p"

    # If the filename has no quality, use the actual video height when
    # Telegram provides it (works for video messages and video documents).
    width = height = None
    if message is not None:
        media = getattr(message, "video", None)
        if media is not None:
            width = getattr(media, "width", None)
            height = getattr(media, "height", None)

        if not height:
            document = getattr(message, "document", None)
            for attribute in getattr(document, "attributes", []) or []:
                if getattr(attribute, "height", None):
                    width = getattr(attribute, "width", None)
                    height = getattr(attribute, "height", None)
                    break

    if height:
        standard_qualities = (144, 240, 360, 480, 576, 720, 1080, 1440, 2160)
        # Use the nearest standard label only when the dimensions are close
        # to that standard; otherwise preserve the real pixel height.
        nearest = min(standard_qualities, key=lambda value: abs(value - height))
        if abs(nearest - height) <= 8:
            return f"{nearest}p"
        return f"{height}p"

    return "-"



# ==========================================
# GET CLEAN SERIAL NAME
# ==========================================

def get_clean_serial_name(filename):
    return find_serial_name(filename)


# ==========================================
# GET FILE LINK
# SERIAL NAME ONLY
# ==========================================

def make_start_link(serial_name):

    slug = re.sub(
        r"[^A-Za-z0-9]+",
        "-",
        serial_name
    ).strip("-")

    payload = f"getfile-{slug}"

    return (
        f"https://telegram.me/{BOT_USERNAME}"
        f"?start={payload}"
    )


# ==========================================
# BATCH PROCESSING STORAGE (SERIAL WISE)
# ==========================================

pending_batches = defaultdict(list)
batch_timers = {}


async def process_batch(client, chat_id, serial_name):
    await asyncio.sleep(5)  # എല്ലാ ഫയലുകളും എത്തുവാൻ 5 സെക്കൻഡ് കാത്തിരിക്കുന്നു

    batch_key = (chat_id, serial_name)
    if batch_key not in pending_batches or not pending_batches[batch_key]:
        return

    batch_items = pending_batches[batch_key].copy()
    pending_batches[batch_key].clear()

    if batch_key in batch_timers:
        del batch_timers[batch_key]

    try:
        sample_message = batch_items[0]
        filename = get_file_name(sample_message)

        season = get_season(filename)
        quality = get_quality(filename, sample_message)

        # ഫയൽ പേരുകളിൽ നിന്ന് S01E01 അല്ലെങ്കിൽ E85 പോലുള്ള കൃത്യമായ എപ്പിസോഡ് മാത്രം എടുക്കുന്നു
        all_episodes = []
        for message in batch_items:
            f_name = get_file_name(message)
            
            # പ്രധാനമായും S01E05 അല്ലെങ്കിൽ E05 / Ep 5 രീതിയിലുള്ളവ മാത്രം ടാർഗെറ്റ് ചെയ്യുന്നു
            match_e = re.search(r'[sS]\d+[ ._-]*[eE](\d+)', f_name)
            if match_e:
                all_episodes.append(int(match_e.group(1)))
            else:
                match_ep_word = re.findall(r'\b(?:ep(?:isode)?|e)\s*[-_.]*(\d{1,4})\b', f_name, re.IGNORECASE)
                if match_ep_word:
                    for ep in match_ep_word:
                        num = int(ep)
                        if num > 0:
                            all_episodes.append(num)

        # എപ്പിസോഡ് റേഞ്ച് ശരിയായി ക്രമീകരിക്കുന്നു (ഒറ്റ ഫയൽ ആണെങ്കിൽ ആ നമ്പർ മാത്രം വരും)
        if all_episodes:
            all_episodes = sorted(list(set(all_episodes)))
            min_ep = min(all_episodes)
            max_ep = max(all_episodes)
            if min_ep != max_ep:
                episode = f"{min_ep}-{max_ep}"
            else:
                episode = str(min_ep)
        else:
            episode = "1"

        caption = (
            "<b>🍁Anujith Allu TV Serials🍁</b>\n\n"
            f"📁 <b>File Name :</b> {serial_name}\n"
            f"🎞️ <b>Season :</b> {season}\n"
            f"📌 <b>Episode :</b> {episode}\n"
            f"🎬 <b>Quality :</b> {quality}"
        )

        bot_link = make_start_link(serial_name)

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📥 Get File",
                        url=bot_link
                    )
                ]
            ]
        )

        await client.send_photo(
            chat_id=AUTH_CHANNEL,
            photo=BANNER_PHOTO,
            caption=caption,
            parse_mode=ParseMode.HTML,
            reply_markup=buttons
        )

        print(
            "Auto-post successful | "
            f"Name: {serial_name} | "
            f"Season: {season} | "
            f"Episode: {episode} | "
            f"Quality: {quality}"
        )

    except Exception as error:
        print(f"Auto-Formatter Error: {error}")


# ==========================================
# AUTO POST HANDLER (MULTI-SERIAL SUPPORT)
# ==========================================

@Client.on_message(
    filters.chat(CHANNELS)
    & (filters.document | filters.video)
)
async def auto_post_formatter(client, message):
    chat_id = message.chat.id
    filename = get_file_name(message)
    serial_name = get_clean_serial_name(filename)
    
    batch_key = (chat_id, serial_name)
    pending_batches[batch_key].append(message)

    if batch_key not in batch_timers:
        batch_timers[batch_key] = asyncio.create_task(process_batch(client, chat_id, serial_name))
