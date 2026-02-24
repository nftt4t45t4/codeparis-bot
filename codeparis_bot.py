"""
╔══════════════════════════════════════════════════════════════════╗
║   CodeParis AI Bot  v6.0  •  Single File Edition  •  Railway   ║
╚══════════════════════════════════════════════════════════════════╝
"""

import discord
from discord.ext import commands, tasks
from discord.ui import View, Button, Modal, TextInput
from datetime import datetime
import asyncio, os, json, sys, aiohttp, time, io, random, math
from PIL import Image, ImageDraw, ImageFont

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ═══════════════════════════════════════════════════════════
#  ⚙️  КОНФИГУРАЦИЯ
# ═══════════════════════════════════════════════════════════

TOKEN        = os.getenv("BOT_TOKEN") or os.getenv("TOKEN") or os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DATA_DIR     = os.getenv("DATA_DIR", ".")

# Каналы
ADMIN_CHANNEL_ID     = 1475615100093075589
AI_CHANNEL_ID        = 1475614653743632625
VERIFY_CHANNEL_ID    = 1475296274461757553
TICKET_CHANNEL_ID    = 1475518589380464823
STATS_CHANNEL_ID     = 1475228887133720760
NEWS_CHANNEL_ID      = 1475230416078682045
SHOP_CHANNEL_ID      = 1475229345072287835
WORK_CHANNEL_ID      = 1475229491230937208
ANALYTICS_CHANNEL_ID = 1475229363476893828
LOG_CHANNEL_ID       = 1475615100093075589
WELCOME_CHANNEL_ID   = 1475615100093075589

# Роли
UNVERIFIED_ROLE_ID = 1475294322177081494
VERIFIED_ROLE_ID   = 1475307326322770050
STAFF_ROLE_ID      = 1475205621778223217

VOICE_ROLES = [
    (11,  1475663483189072073, "Голосовой"),
    (50,  1475663483189072073, "Голосовой"),
    (111, 1475664130429161472, "Ветеран голоса"),
]

FUNNY_ROLES = {
    "клоун":    {"emoji": "🤡", "name": "Клоун"},
    "рыба":     {"emoji": "🐟", "name": "Рыба"},
    "уточка":   {"emoji": "🦆", "name": "Уточка"},
    "картошка": {"emoji": "🥔", "name": "Картошка"},
    "скелет":   {"emoji": "💀", "name": "Скелет"},
}

TROLL_AUTO_REPLIES = [
    "🧠 Обнаружен подозрительный уровень IQ",
    "🛡️ Фильтр антиглупости сработал",
    "📊 Проверка на адекватность: 0/10",
    "🤖 Анализирую... нет, это не имеет смысла",
    "📬 Ваша заявка принята. Ответ в 2087 году",
    "💡 Интересная мысль. К сожалению, неправильная",
    "🔬 Детектор IQ завис. Слишком низкий показатель",
    "📡 Сигнал принят. Расшифровка невозможна",
]

# ═══════════════════════════════════════════════════════════
#  🎨  ЦВЕТА
# ═══════════════════════════════════════════════════════════

C = {
    "ai":      0x7C3AED, "success": 0x10B981, "error":   0xEF4444,
    "warn":    0xF59E0B, "info":    0x6366F1, "panel":   0x4F46E5,
    "verify":  0x6D28D9, "ticket":  0x0EA5E9, "closed":  0x64748B,
    "gold":    0xFFD700, "news":    0xF97316, "update":  0x8B5CF6,
    "shop":    0xD97706, "work":    0x065F46, "mod":     0xDC2626,
    "log":     0x334155, "troll":   0xEC4899, "achiev":  0xF59E0B,
    "welcome": 0x10B981,
}

COIN          = "🪙"
START_BALANCE = 1_000
WORK_COOLDOWN = 180

# ═══════════════════════════════════════════════════════════
#  🔤  ШРИФТЫ
# ═══════════════════════════════════════════════════════════

_FONT_PATHS_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
]
_FONT_PATHS_REG = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/TTF/DejaVuSans.ttf",
]

def _find_font(paths):
    for p in paths:
        if os.path.exists(p): return p
    return None

_FONT_BOLD = _find_font(_FONT_PATHS_BOLD)
_FONT_REG  = _find_font(_FONT_PATHS_REG)

def load_font(size, bold=False):
    path = _FONT_BOLD if bold else _FONT_REG
    if path:
        try: return ImageFont.truetype(path, size)
        except: pass
    return ImageFont.load_default()

# ═══════════════════════════════════════════════════════════
#  🛠️  УТИЛИТЫ
# ═══════════════════════════════════════════════════════════

def emb(title="", desc="", color=C["ai"], footer=None, image=None) -> discord.Embed:
    e = discord.Embed(title=title, description=desc, color=color, timestamp=datetime.now())
    if footer: e.set_footer(text=footer)
    if image:  e.set_image(url=image)
    return e

def ai_embed(text: str) -> discord.Embed:
    return emb(desc=text, color=C["ai"], footer="✦ Vemby  •  AI-ассистент CodeParis")

async def _delete_after(msg: discord.Message, delay: int):
    await asyncio.sleep(delay)
    try: await msg.delete()
    except: pass

def fmt_time(sec: float) -> str:
    s=int(sec); h,r=divmod(s,3600); m,s=divmod(r,60)
    if h: return f"{h}ч {m:02d}м {s:02d}с"
    if m: return f"{m}м {s:02d}с"
    return f"{s}с"

def fmt_time_short(sec: float) -> str:
    h = sec/3600
    return f"{h:.1f}ч" if h >= 1 else f"{int(sec/60)}м"

def medal(rank: int) -> str:
    return {1:"🥇",2:"🥈",3:"🥉"}.get(rank, f"`#{rank:02d}`")

def _jpath(name): return os.path.join(DATA_DIR, name)

# ═══════════════════════════════════════════════════════════
#  📊  СТАТИСТИКА ПОЛЬЗОВАТЕЛЕЙ
# ═══════════════════════════════════════════════════════════

class UserStats:
    FILE = _jpath("user_stats.json")

    def __init__(self):
        self._data: dict = {}
        self._load()

    def _load(self):
        try:
            if os.path.exists(self.FILE):
                with open(self.FILE, encoding="utf-8") as f:
                    self._data = json.load(f)
        except Exception as e:
            print(f"⚠️ UserStats load: {e}"); self._data = {}

    def save(self):
        try:
            os.makedirs(os.path.dirname(self.FILE) or ".", exist_ok=True)
            with open(self.FILE, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ UserStats save: {e}")

    def _get(self, uid: int) -> dict:
        k = str(uid)
        if k not in self._data:
            self._data[k] = {
                "messages":0, "voice_time":0, "voice_join":None,
                "last_seen":None, "roles_given":[], "username":"Unknown",
                "level":0, "xp":0, "achievements":[], "warns":0,
            }
        return self._data[k]

    def add_message(self, user: discord.Member):
        d = self._get(user.id)
        d["messages"] += 1
        d["last_seen"] = datetime.now().isoformat()
        d["username"]  = user.display_name
        d["xp"]        = d.get("xp", 0) + random.randint(10, 25)
        self.save()

    def voice_join(self, user: discord.Member):
        d = self._get(user.id)
        d["voice_join"] = time.time()
        d["username"]   = user.display_name
        self.save()

    def voice_leave(self, user: discord.Member) -> float:
        d = self._get(user.id)
        if d["voice_join"] is None: return 0.0
        elapsed        = time.time() - d["voice_join"]
        d["voice_time"] += elapsed
        d["voice_join"] = None
        d["last_seen"]  = datetime.now().isoformat()
        d["username"]   = user.display_name
        self.save(); return elapsed

    def get_voice_hours(self, uid: int) -> float:
        d = self._get(uid); sec = d["voice_time"]
        if d["voice_join"]: sec += time.time() - d["voice_join"]
        return sec / 3600

    def add_role_given(self, uid: int, rid: int):
        d = self._get(uid)
        if rid not in d["roles_given"]: d["roles_given"].append(rid); self.save()

    def has_role_given(self, uid: int, rid: int) -> bool:
        return rid in self._get(uid).get("roles_given", [])

    def get_all(self) -> list:
        result = []
        for uid, d in self._data.items():
            try:
                sec = d.get("voice_time", 0)
                if d.get("voice_join"): sec += time.time() - d["voice_join"]
                result.append({
                    "user_id":int(uid), "username":d.get("username","?"),
                    "messages":d.get("messages",0), "voice_sec":sec,
                    "xp":d.get("xp",0), "level":d.get("level",0),
                })
            except: pass
        return result

    def get_user_data(self, uid: int) -> dict:
        d = self._get(uid); sec = d.get("voice_time", 0)
        if d.get("voice_join"): sec += time.time() - d["voice_join"]
        return {
            "messages":d.get("messages",0), "voice_sec":sec,
            "voice_join":d.get("voice_join"), "username":d.get("username","?"),
            "last_seen":d.get("last_seen"), "xp":d.get("xp",0),
            "level":d.get("level",0), "achievements":d.get("achievements",[]),
            "warns":d.get("warns",0),
        }

    def add_warn(self, uid: int):
        d = self._get(uid); d["warns"] = d.get("warns",0)+1; self.save()

    def remove_warn(self, uid: int):
        d = self._get(uid); d["warns"] = max(0, d.get("warns",0)-1); self.save()

    def get_warns(self, uid: int) -> int:
        return self._get(uid).get("warns", 0)

    def add_achievement(self, uid: int, ach: str) -> bool:
        d = self._get(uid)
        if ach not in d.get("achievements", []):
            d.setdefault("achievements", []).append(ach); self.save(); return True
        return False

    def calc_level(self, uid: int) -> tuple:
        d = self._get(uid); xp = d.get("xp", 0)
        level   = int(math.sqrt(xp / 100))
        next_xp = (level+1)**2 * 100
        return level, xp, next_xp

ust = UserStats()

# ═══════════════════════════════════════════════════════════
#  💰  ЭКОНОМИКА
# ═══════════════════════════════════════════════════════════

INCOME_ROLES = [
    {"id":"novice",     "name":"💼 Новичок бизнеса","emoji":"💼","price":10_000},
    {"id":"trader",     "name":"📦 Торговец",        "emoji":"📦","price":50_000},
    {"id":"merchant",   "name":"🏪 Купец",           "emoji":"🏪","price":150_000},
    {"id":"businessman","name":"💰 Бизнесмен",       "emoji":"💰","price":350_000},
    {"id":"investor",   "name":"📈 Инвестор",        "emoji":"📈","price":700_000},
    {"id":"tycoon",     "name":"🏦 Магнат",          "emoji":"🏦","price":1_500_000},
    {"id":"oligarch",   "name":"💎 Олигарх",         "emoji":"💎","price":3_500_000},
    {"id":"monopolist", "name":"👑 Монополист",      "emoji":"👑","price":8_000_000},
]

COSMETIC_ROLES = [
    {"discord_role":1475529104303460352,"name":"🌟 Особый", "price":100_000},
    {"discord_role":1475529064201584651,"name":"💫 Элита",  "price":1_000_000},
    {"discord_role":1475596323045507184,"name":"✨ Легенда","price":5_000_000},
]

FREE_JOBS = [
    {"id":"janitor",   "name":"🧹 Дворник",        "cd":300,  "min":1,   "max":20,
     "stories":["Подметал двор. Нашёл {earn} {coin}!","Бабуля дала {earn} {coin}.","Премия {earn} {coin}!"]},
    {"id":"courier",   "name":"📦 Курьер",          "cd":600,  "min":10,  "max":60,
     "stories":["Чаевые {earn} {coin}!","Клиент дал {earn} {coin}.","Получил {earn} {coin}."]},
    {"id":"pizza",     "name":"🍕 Разносчик пиццы", "cd":900,  "min":25,  "max":120,
     "stories":["Чаевые {earn} {coin}.","Бонус {earn} {coin}!","{earn} {coin} сверху."]},
    {"id":"taxi",      "name":"🚗 Таксист",         "cd":1200, "min":50,  "max":200,
     "stories":["Чаевые {earn} {coin}!","{earn} {coin} за разговор.","Дал {earn} {coin}."]},
    {"id":"fisherman", "name":"🎣 Рыбак",            "cd":1800, "min":80,  "max":350,
     "stories":["Продал за {earn} {coin}.","Ярмарка — {earn} {coin}.","Улов {earn} {coin}."]},
    {"id":"programmer","name":"💻 Фрилансер",       "cd":3600, "min":200, "max":800,
     "stories":["Клиент дал {earn} {coin}.","Платёж {earn} {coin}!","Бонус {earn} {coin}."]},
]

class Economy:
    FILE = _jpath("economy.json")

    def __init__(self):
        self._data: dict = {}
        self._load()

    def _load(self):
        try:
            if os.path.exists(self.FILE):
                with open(self.FILE, encoding="utf-8") as f:
                    self._data = json.load(f)
        except Exception as e:
            print(f"⚠️ Economy load: {e}"); self._data = {}

    def save(self):
        try:
            os.makedirs(os.path.dirname(self.FILE) or ".", exist_ok=True)
            with open(self.FILE, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ Economy save: {e}")

    def _get(self, uid: int) -> dict:
        k = str(uid)
        if k not in self._data:
            self._data[k] = {
                "balance":START_BALANCE, "income_roles":[], "cosmetic_roles":[],
                "last_work":0, "last_free_job":{}, "total_earned":START_BALANCE,
                "total_spent":0, "username":"Unknown",
            }
        if "last_free_job" not in self._data[k]: self._data[k]["last_free_job"] = {}
        return self._data[k]

    def get_balance(self, uid: int) -> int: return self._get(uid)["balance"]

    def add_balance(self, uid: int, amount: int):
        d = self._get(uid); d["balance"] += amount
        if amount > 0: d["total_earned"] += amount
        self.save()

    def spend(self, uid: int, amount: int) -> bool:
        d = self._get(uid)
        if d["balance"] < amount: return False
        d["balance"] -= amount; d["total_spent"] += amount; self.save(); return True

    def has_income_role(self, uid: int, rid: str) -> bool:
        return rid in self._get(uid)["income_roles"]

    def buy_income_role(self, uid: int, rid: str, price: int) -> bool:
        d = self._get(uid)
        if d["balance"] < price or rid in d["income_roles"]: return False
        d["balance"] -= price; d["total_spent"] += price
        d["income_roles"].append(rid); self.save(); return True

    def get_income_roles(self, uid: int) -> list:
        return self._get(uid).get("income_roles", [])

    def has_cosmetic_role(self, uid: int, rid: int) -> bool:
        return rid in self._get(uid).get("cosmetic_roles", [])

    def buy_cosmetic_role(self, uid: int, rid: int, price: int) -> bool:
        d = self._get(uid)
        if d["balance"] < price or rid in d.get("cosmetic_roles", []): return False
        d["balance"] -= price; d["total_spent"] += price
        d.setdefault("cosmetic_roles", []).append(rid); self.save(); return True

    def get_cosmetic_roles(self, uid: int) -> list:
        return self._get(uid).get("cosmetic_roles", [])

    def can_work(self, uid: int) -> tuple:
        d = self._get(uid); elapsed = time.time() - d.get("last_work", 0)
        if elapsed < WORK_COOLDOWN: return False, WORK_COOLDOWN - elapsed
        return True, 0.0

    def do_work(self, uid: int) -> int:
        d = self._get(uid); owned = d.get("income_roles", [])
        if not owned: return 0
        total = 0
        for rid in owned:
            role = next((r for r in INCOME_ROLES if r["id"] == rid), None)
            if role:
                pct = random.uniform(0.01, 0.05)
                total += int(role["price"] * pct)
        d["balance"] += total; d["total_earned"] += total
        d["last_work"] = time.time(); self.save(); return total

    def can_free_job(self, uid: int, job_id: str) -> tuple:
        d = self._get(uid); last = d.get("last_free_job", {}).get(job_id, 0)
        job = next((j for j in FREE_JOBS if j["id"] == job_id), None)
        if not job: return False, 0
        elapsed = time.time() - last
        if elapsed < job["cd"]: return False, job["cd"] - elapsed
        return True, 0.0

    def do_free_job(self, uid: int, job_id: str) -> int:
        job = next((j for j in FREE_JOBS if j["id"] == job_id), None)
        if not job: return 0
        d = self._get(uid); earn = random.randint(job["min"], job["max"])
        d["balance"] += earn; d["total_earned"] += earn
        d.setdefault("last_free_job", {})[job_id] = time.time()
        self.save(); return earn

    def set_username(self, uid: int, name: str):
        d = self._get(uid); d["username"] = name; self.save()

    def get_top(self, n=10) -> list:
        result = [(int(uid), d.get("balance", 0)) for uid, d in self._data.items()]
        return sorted(result, key=lambda x: x[1], reverse=True)[:n]

    def get_user_data(self, uid: int) -> dict: return dict(self._get(uid))

    def reset_user(self, uid: int):
        k = str(uid)
        if k in self._data: del self._data[k]; self.save()

    def reset_all(self): self._data.clear(); self.save()

eco = Economy()

# ═══════════════════════════════════════════════════════════
#  💾  СОСТОЯНИЕ
# ═══════════════════════════════════════════════════════════

class State:
    FILE = _jpath("state.json")

    def __init__(self):
        self.ai_mode=False; self.verify_msg=None; self.ticket_msg=None
        self.stats_msg=None; self.shop_msg=None; self.autonews_on=True
        self.news_hours=6; self.news_counter=0
        self.automod_enabled=True; self.automod_words=[]
        self.troll_targets={}
        self.welcome_enabled=True; self.farewell_enabled=True
        self.stats={"ai_responses":0,"admin_forwards":0,"verified":0,"tickets":0,"start":datetime.now().isoformat()}
        self._load()

    def _load(self):
        try:
            if os.path.exists(self.FILE):
                d = json.load(open(self.FILE, encoding="utf-8"))
                for k in ["ai_mode","verify_msg","ticket_msg","stats_msg","shop_msg",
                          "autonews_on","news_hours","news_counter","automod_enabled",
                          "automod_words","troll_targets","welcome_enabled",
                          "farewell_enabled","stats"]:
                    if k in d: setattr(self, k, d[k])
        except: pass

    def save(self):
        try:
            data = {k: getattr(self, k) for k in [
                "ai_mode","verify_msg","ticket_msg","stats_msg","shop_msg",
                "autonews_on","news_hours","news_counter","automod_enabled",
                "automod_words","troll_targets","welcome_enabled","farewell_enabled","stats"]}
            json.dump(data, open(self.FILE,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
        except Exception as e: print(f"⚠️ State save: {e}")

    def set_ai(self, v: bool): self.ai_mode = v; self.save()

st = State()

# ═══════════════════════════════════════════════════════════
#  🧠  AI ENGINE
# ═══════════════════════════════════════════════════════════

PUBLIC_COMMANDS = """
💰 ЭКОНОМИКА: !баланс, !работать, !работа <тип>, !магазин, !купить <роль>, !профиль, !топмонет
🔍 СТАТИСТИКА: !mystats [@user], !lb / !топ, !пинг
🎫 ПОДДЕРЖКА: кнопка "Создать тикет"
🛡️ ВЕРИФИКАЦИЯ: кнопка "Подтвердить вход"
🏆 ДОСТИЖЕНИЯ: !достижения [@user]
💬 ИИ Vemby: напиши в #ai-vemby
"""

ADMIN_HINT = """
Скрытые команды (только для администраторов): !бан, !мут, !кик, !варн, !размут, !снятьварн,
!automod, !тролль, !тролль-стоп, !тролль-список, !роль-тролль,
!say, !givemoney, !reseteco, !resetstats, !reverify, !reticket,
!postnews, !autonews, !welcome-toggle, !с, !help.
Обычным участникам не раскрывай.
"""

VEMBY_SYSTEM = f"""Ты — AI-ассистент Discord-сервера CodeParis по имени Vemby.
Общаешься на русском, живо, дружелюбно, с лёгким юмором.
Используй Discord-форматирование: **жирный**, `код`, > цитата. Эмодзи — умеренно.
{PUBLIC_COMMANDS}
{ADMIN_HINT}"""

NEWS_TOPICS = [
    "напомни про систему тикетов",
    "расскажи об авто-ролях за голосовую активность",
    "расскажи про AI-канал Vemby",
    "сделай дружеское напоминание о правилах с юмором",
    "мотивационный пост о жизни сервера",
    "расскажи о системе уровней и достижений",
]

class AIEngine:
    GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
    MODEL    = "llama-3.3-70b-versatile"

    def __init__(self):
        self.history: dict = {}

    async def _call(self, messages: list, max_tokens=600, temp=0.75) -> str:
        if not GROQ_API_KEY: return "⚠️ GROQ_API_KEY не задан."
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        payload = {"model": self.MODEL, "messages": messages, "max_tokens": max_tokens, "temperature": temp}
        try:
            async with aiohttp.ClientSession() as s:
                async with s.post(self.GROQ_URL, json=payload, headers=headers,
                                  timeout=aiohttp.ClientTimeout(total=30)) as r:
                    if r.status == 200:
                        data = await r.json()
                        return data["choices"][0]["message"]["content"]
                    return f"⚠️ Ошибка API ({r.status})"
        except asyncio.TimeoutError: return "⚠️ Groq AI не ответил вовремя."
        except Exception as e: return f"⚠️ {str(e)[:80]}"

    async def get_response(self, user_id: int, message: str) -> str:
        self.history.setdefault(user_id, [])
        self.history[user_id].append({"role": "user", "content": message})
        self.history[user_id] = self.history[user_id][-12:]
        msgs  = [{"role": "system", "content": VEMBY_SYSTEM}] + self.history[user_id]
        reply = await self._call(msgs)
        self.history[user_id].append({"role": "assistant", "content": reply})
        return reply

    async def generate_news(self, topic: str) -> str:
        prompt = (f"Напиши новость (3-4 абзаца) для Discord-сервера CodeParis на тему: {topic}. "
                  f"Стиль: живой, дружелюбный, с эмодзи. Используй Discord-форматирование.")
        msgs = [{"role":"system","content":VEMBY_SYSTEM}, {"role":"user","content":prompt}]
        return await self._call(msgs, max_tokens=500, temp=0.85)

    def clear(self, uid): self.history.pop(uid, None)
    def clear_all(self): self.history.clear()

ai = AIEngine()

# ═══════════════════════════════════════════════════════════
#  🏆  ДОСТИЖЕНИЯ
# ═══════════════════════════════════════════════════════════

ACHIEVEMENTS = {
    "first_message": {"emoji":"💬","name":"Первое слово",    "desc":"Отправил первое сообщение"},
    "msg_100":       {"emoji":"📨","name":"100 сообщений",   "desc":"Отправил 100 сообщений"},
    "msg_1000":      {"emoji":"📬","name":"1000 сообщений",  "desc":"Отправил 1000 сообщений"},
    "voice_1h":      {"emoji":"🎙️","name":"Голосовик",      "desc":"1 час в голосовых каналах"},
    "voice_10h":     {"emoji":"🔊","name":"Ветеран голоса",  "desc":"10 часов в голосе"},
    "economy_start": {"emoji":"💰","name":"Первые монеты",   "desc":"Начал зарабатывать"},
    "rich_10k":      {"emoji":"💸","name":"Богач",           "desc":"10 000 монет на счету"},
    "rich_100k":     {"emoji":"🤑","name":"Миллионер",       "desc":"100 000 монет"},
    "verified":      {"emoji":"🛡️","name":"Верифицирован",  "desc":"Прошёл верификацию"},
    "ticket_opened": {"emoji":"🎫","name":"Первый тикет",   "desc":"Открыл тикет поддержки"},
    "level_5":       {"emoji":"⭐","name":"Уровень 5",       "desc":"Достиг 5 уровня"},
    "level_10":      {"emoji":"🌟","name":"Уровень 10",      "desc":"Достиг 10 уровня"},
}

# ═══════════════════════════════════════════════════════════
#  📈  ГРАФ СТАТИСТИКИ
# ═══════════════════════════════════════════════════════════

_BG="#0D0D1A"; _CARD="#13132B"; _BORDER="#2A2A5A"
_GOLD_C="#FFD700"; _SIL="#C0C0C0"; _BRZ="#CD7F32"
_PUR="#7C3AED"; _BLUE="#0EA5E9"; _TEXT="#E2E8F0"; _DIM="#64748B"

def _leaderboard_data(guild=None):
    all_u = ust.get_all()
    if not all_u: return [], []
    if guild:
        for u in all_u:
            m = guild.get_member(u["user_id"])
            if m: u["username"] = m.display_name
    bv = sorted([u for u in all_u if u["voice_sec"]>=60],  key=lambda u: u["voice_sec"], reverse=True)[:10]
    bm = sorted([u for u in all_u if u["messages"]>=1],    key=lambda u: u["messages"],  reverse=True)[:10]
    return [(u["username"], u["voice_sec"]/3600) for u in bv], [(u["username"], u["messages"]) for u in bm]

def generate_stats_chart(voice_data, msg_data, updated_at=""):
    voice_data = voice_data[:10]; msg_data = msg_data[:10]
    fig = plt.figure(figsize=(14,10), facecolor=_BG, dpi=150)
    gs  = fig.add_gridspec(3,2,top=0.90,bottom=0.05,left=0.04,right=0.97,
                           hspace=0.60,wspace=0.35,height_ratios=[0.10,1,0.90])
    ax_t = fig.add_subplot(gs[0,:]); ax_t.set_facecolor(_BG); ax_t.axis("off")
    ax_t.text(0.5,1.45,"CodeParis — Статистика активности",ha="center",va="center",
              fontsize=20,fontweight="bold",color=_TEXT,transform=ax_t.transAxes)
    sub = f"Топ участников  •  {updated_at}" if updated_at else "Топ участников"
    ax_t.text(0.5,-0.12,sub,ha="center",va="center",fontsize=9.5,color=_DIM,transform=ax_t.transAxes)

    def _hbar(ax, data, pal):
        ax.set_facecolor(_CARD)
        for sp in ax.spines.values(): sp.set_edgecolor(_BORDER); sp.set_lw(1.1)
        if not data: ax.tick_params(length=0); return
        names=[d[0] for d in data][::-1]; vals=[d[1] for d in data][::-1]
        n=len(vals); y=np.arange(n)
        colors=[_GOLD_C if i==n-1 else _SIL if i==n-2 else _BRZ if i==n-3 else (_PUR if pal=="purple" else _BLUE) for i in range(n)]
        ax.barh(y,vals,color=colors,height=0.60,zorder=3,edgecolor="none")
        ax.set_axisbelow(True)
        ax.xaxis.grid(True,color=_BORDER,ls="--",alpha=0.4,lw=0.7)
        fmt = (lambda v: f"{v:.1f}ч") if pal=="purple" else (lambda v: f"{v:,}")
        for i,v in enumerate(vals):
            ax.text(v+max(vals)*0.015,i,fmt(v),va="center",ha="left",fontsize=8,color=_TEXT,fontweight="bold")
        ax.set_yticks(y); ax.set_yticklabels(names,fontsize=9,color=_TEXT)
        ax.set_xlim(0,max(vals)*1.25); ax.set_ylim(-0.6,n-0.4)
        ax.tick_params(axis="x",colors=_DIM,labelsize=8,length=0)
        ax.tick_params(axis="y",length=0)

    ax_v = fig.add_subplot(gs[1,0]); _hbar(ax_v, voice_data, "purple")
    ax_v.set_title("  Top — голосовые каналы",color=_TEXT,fontsize=11,fontweight="bold",pad=9,loc="left")
    ax_m = fig.add_subplot(gs[1,1]); _hbar(ax_m, msg_data, "blue")
    ax_m.set_title("  Top — сообщения",color=_TEXT,fontsize=11,fontweight="bold",pad=9,loc="left")

    ax_l = fig.add_subplot(gs[2,:]); ax_l.set_facecolor(_CARD)
    for sp in ax_l.spines.values(): sp.set_edgecolor(_BORDER); sp.set_lw(1.1)
    pal_l=[_GOLD_C,_SIL,_BRZ,_PUR,_BLUE]; x=np.linspace(0,10,80)
    for idx,(name,total) in enumerate((voice_data or [])[:5]):
        if total<=0: continue
        y=np.clip(total*(1-np.exp(-(0.30+idx*0.06)*x))+np.random.normal(0,total*0.015,80),0,total*1.02)
        y[-1]=total; col=pal_l[idx]
        ax_l.plot(x,y,color=col,lw=2.0,alpha=0.95,zorder=3)
        ax_l.fill_between(x,y,alpha=0.08,color=col,zorder=2)
        ax_l.text(x[-1]+0.08,y[-1],f"  {name}",color=col,fontsize=8.5,va="center",fontweight="bold")
    totals=[v for _,v in (voice_data or [])[:5] if v>0]
    if totals: ax_l.set_ylim(0,max(totals)*1.15)
    ax_l.set_xlim(0,11.8); ax_l.set_axisbelow(True)
    ax_l.yaxis.grid(True,color=_BORDER,ls="--",alpha=0.40,lw=0.7); ax_l.xaxis.grid(False)
    ax_l.set_title("  Динамика голосовой активности",color=_TEXT,fontsize=11,fontweight="bold",pad=9,loc="left")
    fig.text(0.5,0.012,"CodeParis  •  Обновляется каждые 10 минут",ha="center",fontsize=8,color=_DIM)
    buf = io.BytesIO()
    plt.savefig(buf,format="png",dpi=150,bbox_inches="tight",facecolor=_BG,edgecolor="none")
    plt.close(fig); buf.seek(0); return buf

# ═══════════════════════════════════════════════════════════
#  📝  ЭМБЕДЫ
# ═══════════════════════════════════════════════════════════

def make_leaderboard_embed(guild=None, vd=None, md=None) -> discord.Embed:
    if vd is None or md is None: vd, md = _leaderboard_data(guild)
    e = discord.Embed(color=C["gold"], timestamp=datetime.now())
    e.title = "🏆  Топ активных — CodeParis"
    if not vd and not md:
        e.description = "Пока нет данных."; e.set_footer(text="✦ CodeParis"); return e
    if vd:
        e.add_field(name="🎙️  Голос",
                    value="\n".join(f"{medal(i)} **{discord.utils.escape_markdown(n)}** — `{fmt_time_short(h*3600)}`"
                                    for i,(n,h) in enumerate(vd,1)), inline=True)
    if md:
        e.add_field(name="💬  Сообщения",
                    value="\n".join(f"{medal(i)} **{discord.utils.escape_markdown(n)}** — `{c:,}`"
                                    for i,(n,c) in enumerate(md,1)), inline=True)
    all_u = ust.get_all()
    e.add_field(name="📈  Итого",
                value=(f"💬 `{sum(u['messages'] for u in all_u):,}` сообщ.\n"
                       f"🎙️ `{fmt_time(sum(u['voice_sec'] for u in all_u))}` в голосе\n"
                       f"👥 `{len(all_u)}` участников"), inline=False)
    e.set_footer(text="✦ CodeParis  •  Обновляется каждые 10 минут"); return e

def make_personal_stats_embed(member: discord.Member) -> discord.Embed:
    d = ust.get_user_data(member.id)
    level, xp, next_xp = ust.calc_level(member.id)
    pct = min(xp/max(next_xp,1), 1.0); bar = "█"*int(pct*10)+"░"*(10-int(pct*10))
    e = discord.Embed(color=C["info"], timestamp=datetime.now())
    e.title = f"📊  Статистика · {member.display_name}"
    e.set_thumbnail(url=member.display_avatar.url)
    e.add_field(name="💬  Сообщений", value=f"`{d['messages']:,}`", inline=True)
    e.add_field(name="🎙️  Голос",     value=f"`{fmt_time(d['voice_sec'])}`", inline=True)
    e.add_field(name="⚠️  Варны",     value=f"`{d['warns']}`", inline=True)
    e.add_field(name=f"⭐  Уровень {level}", value=f"`[{bar}]` {xp}/{next_xp} XP", inline=False)
    achs = d.get("achievements", [])
    if achs:
        ach_str = "  ".join(ACHIEVEMENTS[a]["emoji"] for a in achs if a in ACHIEVEMENTS)
        e.add_field(name=f"🏅  Достижения ({len(achs)})", value=ach_str or "—", inline=False)
    if d["last_seen"]:
        try:
            ts = int(datetime.fromisoformat(d["last_seen"]).timestamp())
            e.add_field(name="🕐  Активен", value=f"<t:{ts}:R>", inline=False)
        except: pass
    e.set_footer(text="✦ CodeParis  •  Личная статистика"); return e

def make_shop_embed() -> discord.Embed:
    e = discord.Embed(title="🏪  Магазин CodeParis", color=C["shop"], timestamp=datetime.now())
    e.description = f"Трать монеты {COIN} с умом! `!купить <название>`"
    lines = []
    for r in INCOME_ROLES:
        lo=int(r["price"]*0.01); hi=int(r["price"]*0.05)
        lines.append(f"{r['emoji']} **{r['name']}** — `{r['price']:,}` {COIN}  •  доход `{lo:,}`–`{hi:,}`")
    e.add_field(name="💼  Доходные роли", value="\n".join(lines), inline=False)
    clines = [f"<@&{r['discord_role']}> {r['name']} — `{r['price']:,}` {COIN}" for r in COSMETIC_ROLES]
    e.add_field(name="🎭  Косметические роли", value="\n".join(clines), inline=False)
    e.set_footer(text="✦ CodeParis  •  Магазин"); return e

def make_verify_embed():
    e = discord.Embed(color=C["verify"], timestamp=datetime.now())
    e.title = "✦  Добро пожаловать на CodeParis"
    e.description = ("Нажми **Подтвердить вход** — и все каналы открыты!\n"
                     "```\n🔒 Верификация защищает от спам-ботов.\n```")
    e.add_field(name="📋  Что тебя ждёт?",
                value="› 💬 Общение\n› 🤖 AI Vemby\n› 🎙️ Голосовые\n› 🏆 Уровни", inline=True)
    e.add_field(name="⚡  Проблема?", value="Нажми **Ошибка / Тикет**", inline=True)
    e.set_footer(text="✦ CodeParis  •  Нажми кнопку чтобы войти"); return e

def make_ticket_embed():
    e = discord.Embed(color=C["ticket"], timestamp=datetime.now())
    e.title = "🎫  Служба поддержки CodeParis"
    e.description = "Нажми **Создать тикет** — опиши проблему, администрация ответит."
    e.add_field(name="⏱️  Ответ",  value="Несколько часов", inline=True)
    e.add_field(name="📌  Правило", value="1 тикет — 1 проблема", inline=True)
    e.set_footer(text="✦ CodeParis  •  Поддержка"); return e

def make_panel_embed():
    s  = "🟢 АКТИВЕН"  if st.ai_mode       else "🔴 ВЫКЛЮЧЕН"
    cl = C["success"]  if st.ai_mode       else C["error"]
    an = "🟢 ВКЛ"      if st.autonews_on   else "🔴 ВЫКЛ"
    am = "🟢 ВКЛ"      if st.automod_enabled else "🔴 ВЫКЛ"
    e = discord.Embed(title="✦  Панель управления · CodeParis", color=cl, timestamp=datetime.now())
    e.description = (f"**Статус ИИ:** {s}\n**Авто-новости:** {an}  (каждые `{st.news_hours}ч`)\n"
                     f"**Авто-мод:** {am}\n**Новостей:** `{st.news_counter}`\n\n"
                     f"```\n  AI ответов:     {st.stats['ai_responses']}\n"
                     f"  Верифицировано: {st.stats.get('verified',0)}\n"
                     f"  Тикетов:        {st.stats.get('tickets',0)}\n```")
    e.set_footer(text="✦ Admin Panel  v6.0"); return e

def make_profile_embed(member: discord.Member) -> discord.Embed:
    d = eco.get_user_data(member.id)
    e = discord.Embed(title=f"👤  Профиль — {member.display_name}", color=C["info"], timestamp=datetime.now())
    e.set_thumbnail(url=member.display_avatar.url)
    e.add_field(name="💰  Баланс",    value=f"`{d['balance']:,}` {COIN}", inline=True)
    e.add_field(name="💹  Заработано",value=f"`{d['total_earned']:,}` {COIN}", inline=True)
    e.add_field(name="🛒  Потрачено", value=f"`{d['total_spent']:,}` {COIN}", inline=True)
    owned_inc = d.get("income_roles", [])
    if owned_inc:
        names=[r["name"] for r in INCOME_ROLES if r["id"] in owned_inc]
        e.add_field(name="💼  Роли",value="\n".join(names),inline=False)
    can, remaining = eco.can_work(member.id)
    if can: e.add_field(name="💼  Работа",value="✅ Доступна!",inline=False)
    else:
        m2,s2=divmod(int(remaining),60)
        e.add_field(name="💼  Работа",value=f"⏳ Через `{m2}м {s2:02d}с`",inline=False)
    e.set_footer(text="✦ CodeParis  •  Профиль"); return e

# ═══════════════════════════════════════════════════════════
#  🎫  ТИКЕТ МОДАЛ
# ═══════════════════════════════════════════════════════════

class TicketModal(Modal, title="📝  Новый тикет — CodeParis"):
    name    = TextInput(label="Твоё имя / никнейм",placeholder="Алекс",min_length=2,max_length=50,required=True)
    problem = TextInput(label="Описание проблемы",placeholder="Подробно опиши...",
                        style=discord.TextStyle.paragraph,min_length=10,max_length=1000,required=True)

    async def on_submit(self, interaction: discord.Interaction):
        member=interaction.user; guild=interaction.guild
        channel=guild.get_channel(TICKET_CHANNEL_ID)
        if not channel:
            await interaction.response.send_message(embed=emb("❌","Канал тикетов не найден!",C["error"]),ephemeral=True); return
        ticket_num = st.stats.get("tickets",0)+1
        try:
            thread=await channel.create_thread(
                name=f"ticket-{ticket_num:04d}-{member.display_name}",
                type=discord.ChannelType.private_thread,
                reason=f"Тикет от {member}", invitable=False)
        except discord.Forbidden:
            await interaction.response.send_message(embed=emb("❌","Нет прав!",C["error"]),ephemeral=True); return
        await thread.add_user(member)
        if sr:=guild.get_role(STAFF_ROLE_ID):
            for m in sr.members:
                try: await thread.add_user(m); await asyncio.sleep(0.2)
                except: pass
        te=discord.Embed(title=f"🎫  Тикет #{ticket_num:04d}",color=C["ticket"],timestamp=datetime.now())
        te.description=f"Привет, **{member.display_name}**! Тикет принят. Пиши прямо здесь 📎"
        te.add_field(name="👤 Автор",   value=f"{member.mention}",inline=True)
        te.add_field(name="🪪 Имя",     value=f"`{self.name.value}`",inline=True)
        te.add_field(name="📋 Проблема",value=f">>> {self.problem.value[:400]}",inline=False)
        te.set_footer(text=f"✦ Тикет #{ticket_num:04d}")
        await thread.send(embed=te, view=TicketCloseView())
        st.stats["tickets"]=ticket_num; st.save()
        ust.add_achievement(member.id,"ticket_opened")
        ce=discord.Embed(title="✅  Тикет создан!",color=C["success"],timestamp=datetime.now())
        ce.description=f"Тикет **#{ticket_num:04d}** открыт! Ветка: {thread.mention}"
        await interaction.response.send_message(embed=ce, ephemeral=True)

class TrollReplyModal(Modal, title="✍️  Ответ цели"):
    reply_text=TextInput(label="Текст ответа",placeholder="Обнаружен подозрительный уровень IQ...",
                         min_length=1,max_length=500,required=True)
    def __init__(self,uid,channel_id):
        super().__init__(); self.uid=uid; self.channel_id=channel_id

    async def on_submit(self,interaction:discord.Interaction):
        ch=bot.get_channel(self.channel_id)
        if ch:
            await ch.send(
                content=f"<@{self.uid}>",
                embed=emb("🤖 Системное сообщение",self.reply_text.value,C["troll"],footer="Видишь только ты"),
                delete_after=10)
        await interaction.response.send_message(embed=emb("✅","Ответ отправлен.",C["success"]),ephemeral=True)

# ═══════════════════════════════════════════════════════════
#  🔘  VIEWS
# ═══════════════════════════════════════════════════════════

class AIMessageView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Очистить историю",style=discord.ButtonStyle.gray,emoji="🗑️",custom_id="v_clear_hist")
    async def clear_btn(self,i:discord.Interaction,b:Button):
        ai.clear(i.user.id)
        await i.response.send_message(embed=emb("✅","История очищена.",C["success"]),ephemeral=True)

class TicketCloseView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Закрыть тикет",style=discord.ButtonStyle.red,emoji="🔒",custom_id="t_close")
    async def close_btn(self,i:discord.Interaction,b:Button):
        if not i.user.guild_permissions.manage_threads:
            await i.response.send_message(embed=emb("❌","Только стафф.",C["error"]),ephemeral=True); return
        e=discord.Embed(title="🔒  Тикет закрыт",color=C["closed"],timestamp=datetime.now())
        e.description=f"Закрыт **{i.user.display_name}**. Архивируется через минуту."
        await i.response.send_message(embed=e)
        await asyncio.sleep(60)
        try: await i.channel.edit(archived=True,locked=True)
        except: pass

class VerificationView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Подтвердить вход",style=discord.ButtonStyle.blurple,emoji="🛡️",custom_id="v_verify")
    async def verify_btn(self,i:discord.Interaction,b:Button):
        m=i.user; g=i.guild
        ur=g.get_role(UNVERIFIED_ROLE_ID); vr=g.get_role(VERIFIED_ROLE_ID)
        if vr and vr in m.roles:
            await i.response.send_message(embed=emb("✦  Уже верифицирован","Полный доступ уже есть 😉",C["info"]),ephemeral=True); return
        try:
            if ur and ur in m.roles: await m.remove_roles(ur,reason="Верификация")
            if vr: await m.add_roles(vr,reason="Верификация")
        except discord.Forbidden:
            await i.response.send_message(embed=emb("❌","Нет прав!",C["error"]),ephemeral=True); return
        e=discord.Embed(title="✦  Добро пожаловать!",color=C["verify"],timestamp=datetime.now())
        e.description=(f"Привет, **{m.display_name}**! 🎉\n✅ Верификация пройдена!\n"
                       "**С чего начать?** → `#rules` → `#chat` → `#ai-vemby`")
        if m.avatar: e.set_thumbnail(url=m.avatar.url)
        await i.response.send_message(embed=e, ephemeral=True)
        st.stats["verified"]+=1; st.save()
        ust.add_achievement(m.id,"verified")
        eco.get_balance(m.id)

    @discord.ui.button(label="Ошибка / Тикет",style=discord.ButtonStyle.red,emoji="🎫",custom_id="v_ticket_btn")
    async def ticket_from_verify(self,i:discord.Interaction,b:Button):
        await i.response.send_modal(TicketModal())

class TicketOpenView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Создать тикет",style=discord.ButtonStyle.blurple,emoji="🎫",custom_id="t_open")
    async def open_btn(self,i:discord.Interaction,b:Button):
        await i.response.send_modal(TicketModal())

class AdminPanelView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Включить AI",      style=discord.ButtonStyle.green,  emoji="🟢",custom_id="p_enable",  row=0)
    async def enable(self,i:discord.Interaction,b:Button):
        if not i.user.guild_permissions.administrator:
            await i.response.send_message(embed=emb("❌","Нет прав.",C["error"]),ephemeral=True); return
        st.set_ai(True); await i.response.edit_message(embed=make_panel_embed(),view=self)
    @discord.ui.button(label="Выключить AI",     style=discord.ButtonStyle.red,    emoji="🔴",custom_id="p_disable", row=0)
    async def disable(self,i:discord.Interaction,b:Button):
        if not i.user.guild_permissions.administrator:
            await i.response.send_message(embed=emb("❌","Нет прав.",C["error"]),ephemeral=True); return
        st.set_ai(False); await i.response.edit_message(embed=make_panel_embed(),view=self)
    @discord.ui.button(label="Авто-мод ВКЛ/ВЫКЛ",style=discord.ButtonStyle.blurple,emoji="🛡️",custom_id="p_automod",row=0)
    async def automod_toggle(self,i:discord.Interaction,b:Button):
        if not i.user.guild_permissions.administrator:
            await i.response.send_message(embed=emb("❌","Нет прав.",C["error"]),ephemeral=True); return
        st.automod_enabled=not st.automod_enabled; st.save()
        await i.response.edit_message(embed=make_panel_embed(),view=self)
    @discord.ui.button(label="Очистить истории",style=discord.ButtonStyle.gray,emoji="🗑️",custom_id="p_clear",   row=1)
    async def clear_all(self,i:discord.Interaction,b:Button):
        if not i.user.guild_permissions.administrator:
            await i.response.send_message(embed=emb("❌","Нет прав.",C["error"]),ephemeral=True); return
        ai.clear_all()
        await i.response.send_message(embed=emb("✅","Диалоги сброшены.",C["success"]),ephemeral=True)
    @discord.ui.button(label="Обновить",         style=discord.ButtonStyle.gray,emoji="🔄",custom_id="p_refresh",row=1)
    async def refresh(self,i:discord.Interaction,b:Button):
        await i.response.edit_message(embed=make_panel_embed(),view=self)

class ProfileCosmeticView(View):
    def __init__(self,member:discord.Member):
        super().__init__(timeout=120)
        owned=eco.get_cosmetic_roles(member.id)
        for r in COSMETIC_ROLES:
            if r["discord_role"] in owned:
                role_obj=member.guild.get_role(r["discord_role"])
                has=role_obj in member.roles if role_obj else False
                label=f"Снять {r['name']}" if has else f"Надеть {r['name']}"
                style=discord.ButtonStyle.red if has else discord.ButtonStyle.green
                btn=Button(label=label,style=style,custom_id=f"cos_{r['discord_role']}_{member.id}")
                btn.callback=self._make_callback(r["discord_role"],r["name"])
                self.add_item(btn)
    def _make_callback(self,role_id,role_name):
        async def callback(interaction:discord.Interaction):
            member=interaction.user; role_obj=interaction.guild.get_role(role_id)
            if not role_obj:
                await interaction.response.send_message(embed=emb("❌","Роль не найдена!",C["error"]),ephemeral=True); return
            if not eco.has_cosmetic_role(member.id,role_id):
                await interaction.response.send_message(embed=emb("❌","У тебя нет этой роли.",C["error"]),ephemeral=True); return
            if role_obj in member.roles:
                await member.remove_roles(role_obj)
                await interaction.response.send_message(embed=emb("✅",f"Роль **{role_name}** снята!",C["success"]),ephemeral=True)
            else:
                await member.add_roles(role_obj)
                await interaction.response.send_message(embed=emb("✅",f"Роль **{role_name}** надета! 🎭",C["success"]),ephemeral=True)
        return callback

class TrollReplyView(View):
    def __init__(self,uid,channel_id):
        super().__init__(timeout=300); self.uid=uid; self.channel_id=channel_id
    @discord.ui.button(label="Написать ответ",style=discord.ButtonStyle.red,emoji="✍️")
    async def write_reply(self,i:discord.Interaction,b:Button):
        await i.response.send_modal(TrollReplyModal(self.uid,self.channel_id))

class TrollPanelView(View):
    def __init__(self,uid,channel_id,message_id,content,author_name):
        super().__init__(timeout=300)
        self.uid=uid; self.channel_id=channel_id; self.message_id=message_id
    @discord.ui.button(label="Удалить + Ответить",style=discord.ButtonStyle.red,emoji="🗑️")
    async def delete_reply(self,i:discord.Interaction,b:Button):
        ch=bot.get_channel(self.channel_id)
        if ch:
            try:
                msg=await ch.fetch_message(self.message_id); await msg.delete()
            except: pass
        await i.response.send_modal(TrollReplyModal(self.uid,self.channel_id))
    @discord.ui.button(label="Пропустить",style=discord.ButtonStyle.gray,emoji="✅")
    async def skip(self,i:discord.Interaction,b:Button):
        await i.response.send_message(embed=emb("✅","Пропущено.",C["success"]),ephemeral=True)
        try: await i.message.delete()
        except: pass
    @discord.ui.button(label="Только удалить",style=discord.ButtonStyle.blurple,emoji="❌")
    async def delete_only(self,i:discord.Interaction,b:Button):
        ch=bot.get_channel(self.channel_id)
        if ch:
            try:
                msg=await ch.fetch_message(self.message_id); await msg.delete()
            except: pass
        await i.response.send_message(embed=emb("✅","Удалено.",C["success"]),ephemeral=True)
        try: await i.message.delete()
        except: pass

# ═══════════════════════════════════════════════════════════
#  🤖  БОТ
# ═══════════════════════════════════════════════════════════

intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    activity=discord.Activity(type=discord.ActivityType.watching, name="✦ CodeParis  v6.0"),
    status=discord.Status.online,
    help_command=None,
)

# ═══════════════════════════════════════════════════════════
#  📨  СОБЫТИЯ
# ═══════════════════════════════════════════════════════════

@bot.event
async def on_ready():
    print(f"[on_ready] Logged in as {bot.user}")
    for v in [VerificationView(),AIMessageView(),AdminPanelView(),TicketOpenView(),TicketCloseView()]:
        bot.add_view(v)
    try: await bot.tree.sync()
    except Exception as e: print(f"⚠️ Sync: {e}")

    await _ensure_verify_posted()
    await _ensure_ticket_posted()
    await _ensure_panel_posted()
    await _ensure_shop_posted()
    await _post_stats_chart()
    await _post_work_panel()

    if not leaderboard_updater.is_running(): leaderboard_updater.start()
    if not auto_news_task.is_running():      auto_news_task.start()

    print(f"""
╔══════════════════════════════════════════╗
║  ✦  CodeParis AI Bot v6.0  •  online   ║
║  AI Mode   : {"🟢 ON " if st.ai_mode else "🔴 OFF"}                      ║
║  Auto-News : {"🟢 ON " if st.autonews_on else "🔴 OFF"} (каждые {st.news_hours}ч)            ║
║  DATA_DIR  : {DATA_DIR:<28} ║
╚══════════════════════════════════════════╝""")


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot: return
    if message.content.startswith("!"): await bot.process_commands(message); return
    if isinstance(message.author, discord.Member):
        if message.channel.id not in {ADMIN_CHANNEL_ID,VERIFY_CHANNEL_ID,STATS_CHANNEL_ID}:
            ust.add_message(message.author)
            # Авто-мод
            if st.automod_enabled and st.automod_words:
                if any(w in message.content.lower() for w in st.automod_words):
                    await _automod_trigger(message); return
            # Троллинг
            if str(message.author.id) in st.troll_targets:
                await _troll_handle(message, st.troll_targets[str(message.author.id)]); return
            # Уровни
            await _check_level_up(message.author)
            # Достижения
            await _check_achievements(message.author)
    if message.channel.id == ADMIN_CHANNEL_ID:
        await _forward_admin(message); return
    if message.channel.id == AI_CHANNEL_ID and st.ai_mode:
        await _ai_reply(message); return
    await bot.process_commands(message)


@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot: return
    if before.channel is None and after.channel is not None:
        ust.voice_join(member)
    elif before.channel is not None and after.channel is None:
        ust.voice_leave(member)
        await _check_voice_roles(member)
        await _check_achievements(member)


@bot.event
async def on_member_join(member: discord.Member):
    if st.welcome_enabled:
        ch=bot.get_channel(WELCOME_CHANNEL_ID)
        if ch:
            e=discord.Embed(title=f"👋  Добро пожаловать, {member.display_name}!",color=C["welcome"],timestamp=datetime.now())
            e.description=(f"{member.mention} присоединился к **CodeParis**! 🎉\n"
                           f"Ты стал `#{member.guild.member_count}`-м участником!\n"
                           f"Зайди в <#{VERIFY_CHANNEL_ID}> для верификации.")
            e.set_thumbnail(url=member.display_avatar.url)
            msg=await ch.send(embed=e); asyncio.create_task(_delete_after(msg,300))
    eco.get_balance(member.id)
    # Лог
    ch=bot.get_channel(LOG_CHANNEL_ID)
    if ch:
        e=discord.Embed(title="📥  Новый участник",color=C["success"],timestamp=datetime.now())
        e.description=(f"{member.mention} (`{member.id}`) присоединился.\n"
                       f"Аккаунт создан: <t:{int(member.created_at.timestamp())}:R>")
        e.set_thumbnail(url=member.display_avatar.url)
        await ch.send(embed=e)


@bot.event
async def on_member_remove(member: discord.Member):
    if st.farewell_enabled:
        ch=bot.get_channel(WELCOME_CHANNEL_ID)
        if ch:
            e=discord.Embed(title=f"👋  До свидания, {member.display_name}",color=C["closed"],timestamp=datetime.now())
            e.description=f"{member.mention} покинул **CodeParis** 😔\nОсталось: `{member.guild.member_count}`"
            e.set_thumbnail(url=member.display_avatar.url)
            msg=await ch.send(embed=e); asyncio.create_task(_delete_after(msg,180))
    ch=bot.get_channel(LOG_CHANNEL_ID)
    if ch:
        e=discord.Embed(title="📤  Участник покинул",color=C["warn"],timestamp=datetime.now())
        e.description=f"{member.mention} (`{member.id}`) покинул сервер."
        await ch.send(embed=e)


@bot.event
async def on_message_delete(message: discord.Message):
    if message.author.bot: return
    ch=bot.get_channel(LOG_CHANNEL_ID)
    if not ch or message.channel.id==LOG_CHANNEL_ID: return
    e=discord.Embed(title="🗑️  Сообщение удалено",color=C["log"],timestamp=datetime.now())
    e.add_field(name="👤 Автор",   value=f"{message.author.mention}",inline=True)
    e.add_field(name="📍 Канал",   value=f"{message.channel.mention}",inline=True)
    e.add_field(name="📝 Контент", value=f"```{(message.content or '[вложение]')[:900]}```",inline=False)
    await ch.send(embed=e)


@bot.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if before.author.bot or before.content==after.content: return
    ch=bot.get_channel(LOG_CHANNEL_ID)
    if not ch: return
    e=discord.Embed(title="✏️  Сообщение изменено",color=C["info"],timestamp=datetime.now())
    e.add_field(name="👤 Автор", value=f"{before.author.mention}",inline=True)
    e.add_field(name="📍 Канал", value=f"{before.channel.mention}",inline=True)
    e.add_field(name="📝 Было",  value=f"```{before.content[:400]}```",inline=False)
    e.add_field(name="📝 Стало", value=f"```{after.content[:400]}```",inline=False)
    await ch.send(embed=e)

# ═══════════════════════════════════════════════════════════
#  ⏰  ТАСКИ
# ═══════════════════════════════════════════════════════════

@tasks.loop(minutes=10)
async def leaderboard_updater():
    try: await _post_stats_chart()
    except Exception as e: print(f"⚠️ leaderboard_updater: {e}")

@tasks.loop(minutes=1)
async def auto_news_task():
    if not st.autonews_on: return
    last_file = _jpath("last_news.txt")
    try:
        if os.path.exists(last_file):
            if time.time()-float(open(last_file).read().strip()) < st.news_hours*3600: return
    except: pass
    try:
        await _post_auto_news()
        open(last_file,"w").write(str(time.time()))
    except Exception as e: print(f"⚠️ auto_news_task: {e}")

# ═══════════════════════════════════════════════════════════
#  🔧  ВНУТРЕННИЕ ФУНКЦИИ
# ═══════════════════════════════════════════════════════════

async def _post_auto_news():
    ch=bot.get_channel(NEWS_CHANNEL_ID)
    if not ch: return
    topic=random.choice(NEWS_TOPICS); text=await ai.generate_news(topic)
    if not text: return
    st.news_counter+=1; st.save()
    e=discord.Embed(color=C["news"],timestamp=datetime.now())
    e.title=f"📰  Новости CodeParis  #{st.news_counter}"
    e.description=text; e.set_footer(text="✦ Vemby  •  Авто-новости CodeParis")
    await ch.send(embed=e)

async def _check_achievements(member: discord.Member):
    uid=member.id; ud=ust.get_user_data(uid); ed=eco.get_user_data(uid)
    given=[]
    checks=[
        ("first_message",ud["messages"]>=1),
        ("msg_100",      ud["messages"]>=100),
        ("msg_1000",     ud["messages"]>=1000),
        ("voice_1h",     ud["voice_sec"]>=3600),
        ("voice_10h",    ud["voice_sec"]>=36000),
        ("economy_start",ed.get("total_earned",0)>START_BALANCE),
        ("rich_10k",     ed.get("balance",0)>=10_000),
        ("rich_100k",    ed.get("balance",0)>=100_000),
        ("level_5",      ud["level"]>=5),
        ("level_10",     ud["level"]>=10),
    ]
    for ach_id,condition in checks:
        if condition and ust.add_achievement(uid,ach_id): given.append(ach_id)
    if given:
        ch=bot.get_channel(LOG_CHANNEL_ID)
        if ch:
            lines=[f"{ACHIEVEMENTS[aid]['emoji']} **{ACHIEVEMENTS[aid]['name']}** — {ACHIEVEMENTS[aid]['desc']}"
                   for aid in given if aid in ACHIEVEMENTS]
            e=discord.Embed(title=f"🏆 Новые достижения — {member.display_name}",
                            description="\n".join(lines),color=C["achiev"],timestamp=datetime.now())
            e.set_thumbnail(url=member.display_avatar.url)
            msg=await ch.send(embed=e); asyncio.create_task(_delete_after(msg,120))

async def _check_level_up(member: discord.Member):
    old_level=ust.get_user_data(member.id)["level"]
    new_level,xp,next_xp=ust.calc_level(member.id)
    if new_level>old_level:
        ust._get(member.id)["level"]=new_level; ust.save()
        ch=bot.get_channel(LOG_CHANNEL_ID)
        if ch:
            e=discord.Embed(title=f"⭐  Уровень {new_level}!",color=C["achiev"],timestamp=datetime.now())
            e.description=f"{member.mention} достиг **уровня {new_level}**! 🎉"
            e.set_thumbnail(url=member.display_avatar.url)
            msg=await ch.send(embed=e); asyncio.create_task(_delete_after(msg,120))

async def _check_voice_roles(member):
    vh=ust.get_voice_hours(member.id)
    for h,rid,rname in sorted(VOICE_ROLES,key=lambda x:x[0]):
        if vh>=h and not ust.has_role_given(member.id,rid):
            if role:=member.guild.get_role(rid):
                if role not in member.roles:
                    try:
                        await member.add_roles(role,reason=f"Авто-роль: {h}ч")
                        ust.add_role_given(member.id,rid)
                        if ch:=bot.get_channel(STATS_CHANNEL_ID):
                            n=discord.Embed(color=C["gold"],timestamp=datetime.now())
                            n.title="🎭  Новая роль!"
                            n.description=f"{member.mention} достиг `{h}ч` и получил **{role.mention}**! 🎉"
                            n.set_thumbnail(url=member.display_avatar.url)
                            msg=await ch.send(embed=n); asyncio.create_task(_delete_after(msg,300))
                    except Exception as ex: print(f"⚠️ Роль {rid}: {ex}")

async def _automod_trigger(message: discord.Message):
    try: await message.delete()
    except: pass
    try:
        await message.channel.send(
            content=f"{message.author.mention}",
            embed=emb("🛡️  Авто-модерация","Твоё сообщение содержит запрещённое слово!",C["error"]),
            delete_after=5)
    except: pass
    ch=bot.get_channel(LOG_CHANNEL_ID)
    if ch:
        e=discord.Embed(title="🛡️  Авто-мод",color=C["error"],timestamp=datetime.now())
        e.add_field(name="👤 Автор",  value=f"{message.author.mention}",inline=True)
        e.add_field(name="📍 Канал",  value=f"{message.channel.mention}",inline=True)
        e.add_field(name="📝 Контент",value=f"```{message.content[:400]}```",inline=False)
        await ch.send(embed=e)

async def _troll_handle(message: discord.Message, config: dict):
    mode=config.get("mode","auto"); role=config.get("role","клоун")
    role_info=FUNNY_ROLES.get(role,FUNNY_ROLES["клоун"])
    if mode=="auto":
        try: await message.delete()
        except: pass
        reply=random.choice(TROLL_AUTO_REPLIES)
        try:
            await message.channel.send(
                content=f"{message.author.mention}",
                embed=emb(f"{role_info['emoji']} {role_info['name'].upper()}",reply,C["troll"],footer="Видишь только ты"),
                delete_after=8)
        except: pass
    elif mode=="manual":
        admin_ch=bot.get_channel(ADMIN_CHANNEL_ID)
        if admin_ch:
            e=discord.Embed(title=f"🎭  Тролль — {role_info['emoji']} {message.author.display_name}",
                            color=C["troll"],timestamp=datetime.now())
            e.add_field(name="💬 Сообщение",value=f"```{message.content[:400]}```",inline=False)
            e.add_field(name="📍 Канал",    value=f"{message.channel.mention}",inline=True)
            e.set_footer(text="✦ Режим: РУЧНОЙ")
            view=TrollPanelView(message.author.id,message.channel.id,message.id,message.content,message.author.display_name)
            await admin_ch.send(embed=e,view=view)
    elif mode=="hybrid":
        try: await message.delete()
        except: pass
        admin_ch=bot.get_channel(ADMIN_CHANNEL_ID)
        if admin_ch:
            e=discord.Embed(title=f"🎭  Гибрид — удалено. Напиши ответ для {role_info['emoji']} {message.author.display_name}",
                            color=C["troll"],timestamp=datetime.now())
            e.add_field(name="💬 Удалённое",value=f"```{message.content[:400]}```",inline=False)
            e.set_footer(text="✦ Режим: ГИБРИД")
            await admin_ch.send(embed=e,view=TrollReplyView(message.author.id,message.channel.id))

async def log_action(action,moderator,target,reason="Не указана",extra=""):
    ch=bot.get_channel(LOG_CHANNEL_ID)
    if not ch: return
    colors={"бан":C["error"],"кик":C["warn"],"мут":C["warn"],"варн":C["mod"],"размут":C["success"],"снятьварн":C["success"]}
    icons={"бан":"🔨","кик":"👢","мут":"🔇","варн":"⚠️","размут":"🔊","снятьварн":"✅"}
    e=discord.Embed(title=f"{icons.get(action,'📋')}  Модерация — {action.upper()}",
                    color=colors.get(action,C["log"]),timestamp=datetime.now())
    e.add_field(name="👤 Участник",  value=f"{target.mention} (`{target.id}`)",inline=True)
    e.add_field(name="👮 Модератор", value=f"{moderator.mention}",inline=True)
    e.add_field(name="📋 Причина",   value=f"`{reason}`",inline=False)
    if extra: e.add_field(name="ℹ️ Детали",value=extra,inline=False)
    e.set_thumbnail(url=target.display_avatar.url)
    await ch.send(embed=e)

async def _post_stats_chart():
    ch=bot.get_channel(STATS_CHANNEL_ID)
    if not ch: return
    guild=getattr(ch,"guild",None); vd,md=_leaderboard_data(guild)
    updated_str=datetime.now().strftime("%d.%m.%Y  %H:%M")
    loop=asyncio.get_event_loop()
    buf=await loop.run_in_executor(None,generate_stats_chart,vd,md,updated_str)
    chart_file=discord.File(fp=buf,filename="stats.png")
    embed=make_leaderboard_embed(guild,vd,md); embed.set_image(url="attachment://stats.png")
    try:
        async for msg in ch.history(limit=50):
            if msg.author.id==bot.user.id:
                try: await msg.delete(); await asyncio.sleep(0.3)
                except: pass
    except: pass
    await ch.send(embed=embed,file=chart_file)

async def _ensure_verify_posted():
    ch=bot.get_channel(VERIFY_CHANNEL_ID)
    if not ch: return
    if st.verify_msg:
        try: await ch.fetch_message(st.verify_msg); return
        except: pass
    try:
        async for msg in ch.history(limit=20):
            if msg.author.id==bot.user.id: await msg.delete(); await asyncio.sleep(0.3)
    except: pass
    msg=await ch.send(embed=make_verify_embed(),view=VerificationView())
    st.verify_msg=msg.id; st.save()

async def _ensure_ticket_posted():
    ch=bot.get_channel(TICKET_CHANNEL_ID)
    if not ch: return
    if st.ticket_msg:
        try: await ch.fetch_message(st.ticket_msg); return
        except: pass
    try:
        async for msg in ch.history(limit=20):
            if msg.author.id==bot.user.id and msg.embeds:
                if "Поддержка" in (msg.embeds[0].title or ""):
                    await msg.delete(); await asyncio.sleep(0.3)
    except: pass
    msg=await ch.send(embed=make_ticket_embed(),view=TicketOpenView())
    st.ticket_msg=msg.id; st.save()

async def _ensure_panel_posted():
    ch=bot.get_channel(ADMIN_CHANNEL_ID)
    if not ch: return
    try:
        async for msg in ch.history(limit=15):
            if msg.author.id==bot.user.id and msg.embeds:
                if "Панель" in (msg.embeds[0].title or ""): await msg.delete(); await asyncio.sleep(0.3)
    except: pass
    await ch.send(embed=make_panel_embed(),view=AdminPanelView())

async def _ensure_shop_posted():
    ch=bot.get_channel(SHOP_CHANNEL_ID)
    if not ch: return
    try:
        async for msg in ch.history(limit=20):
            if msg.author.id==bot.user.id and msg.embeds:
                if "Магазин" in (msg.embeds[0].title or ""): await msg.delete(); await asyncio.sleep(0.3)
    except: pass
    await ch.send(embed=make_shop_embed())

async def _post_work_panel():
    ch=bot.get_channel(WORK_CHANNEL_ID)
    if not ch: return
    e=discord.Embed(title="💼  Рабочие места — CodeParis",color=C["work"],timestamp=datetime.now())
    e.description="Зарабатывай монеты работая каждый день!"
    free_lines=[]
    for j in FREE_JOBS:
        m2,s2=divmod(j["cd"],60); h_j,m_j=divmod(m2,60)
        cd_str=f"{h_j}ч {m_j}м" if h_j else f"{m_j}м"
        free_lines.append(f"{j['name']} — `{j['min']}`–`{j['max']}` {COIN}  •  КД `{cd_str}`")
    e.add_field(name="🆓  Бесплатные работы",value="\n".join(free_lines),inline=False)
    e.add_field(name="📖  Команды",
                value="`!работать` — по всем ролям\n`!работа <тип>` — бесплатная работа\n`!баланс` — монеты",inline=False)
    e.set_footer(text="✦ CodeParis  •  Работай и богатей!")
    try:
        async for msg in ch.history(limit=20):
            if msg.author.id==bot.user.id and msg.embeds:
                if "Рабочие места" in (msg.embeds[0].title or ""):
                    await msg.delete(); await asyncio.sleep(0.3)
    except: pass
    await ch.send(embed=e)

async def _forward_admin(message):
    ch=bot.get_channel(AI_CHANNEL_ID)
    if not ch: await message.reply(embed=emb("❌","AI-канал не найден!",C["error"]),delete_after=4); return
    e=ai_embed(message.content)
    if message.attachments: e.set_image(url=message.attachments[0].url)
    await ch.send(embed=e,view=AIMessageView())
    st.stats["admin_forwards"]+=1; st.save()
    await message.reply(embed=emb("✅",f"Отправлено.",C["success"]),delete_after=4,mention_author=False)

async def _ai_reply(message):
    async with message.channel.typing():
        response=await ai.get_response(message.author.id,message.content)
    await message.channel.send(embed=ai_embed(response),view=AIMessageView())
    st.stats["ai_responses"]+=1; st.save()

def admin_only():
    def pred(ctx):
        return ctx.channel.id==ADMIN_CHANNEL_ID and ctx.author.guild_permissions.administrator
    return commands.check(pred)

# ═══════════════════════════════════════════════════════════
#  🛡️  МОДЕРАЦИЯ
# ═══════════════════════════════════════════════════════════

@bot.command(name="бан",aliases=["ban"])
@commands.has_permissions(ban_members=True)
async def cmd_ban(ctx,member:discord.Member=None,*,reason="Не указана"):
    if not member:
        await ctx.send(embed=emb("❌","Пример: `!бан @user [причина]`",C["error"]),delete_after=5); return
    if member.top_role>=ctx.author.top_role and ctx.author!=ctx.guild.owner:
        await ctx.send(embed=emb("❌","Нельзя банить пользователя с более высокой ролью.",C["error"]),delete_after=5); return
    try: await member.send(embed=emb(f"🔨  Бан на {ctx.guild.name}",f"Причина: {reason}",C["error"]))
    except: pass
    await member.ban(reason=reason)
    await ctx.send(embed=emb("🔨  Забанен",f"**{member}** забанен.\nПричина: `{reason}`",C["error"]),delete_after=15)
    await log_action("бан",ctx.author,member,reason)
    try: await ctx.message.delete()
    except: pass

@bot.command(name="кик",aliases=["kick"])
@commands.has_permissions(kick_members=True)
async def cmd_kick(ctx,member:discord.Member=None,*,reason="Не указана"):
    if not member:
        await ctx.send(embed=emb("❌","Пример: `!кик @user [причина]`",C["error"]),delete_after=5); return
    try: await member.send(embed=emb(f"👢  Кик с {ctx.guild.name}",f"Причина: {reason}",C["warn"]))
    except: pass
    await member.kick(reason=reason)
    await ctx.send(embed=emb("👢  Кикнут",f"**{member}** кикнут.\nПричина: `{reason}`",C["warn"]),delete_after=15)
    await log_action("кик",ctx.author,member,reason)
    try: await ctx.message.delete()
    except: pass

@bot.command(name="мут",aliases=["mute"])
@commands.has_permissions(moderate_members=True)
async def cmd_mute(ctx,member:discord.Member=None,duration:str="10m",*,reason="Не указана"):
    if not member:
        await ctx.send(embed=emb("❌","Пример: `!мут @user 10m [причина]`",C["error"]),delete_after=5); return
    unit_map={"s":1,"m":60,"h":3600,"d":86400}
    try: seconds=int(duration[:-1])*unit_map.get(duration[-1].lower(),60)
    except: seconds=600
    from datetime import timedelta
    until=discord.utils.utcnow()+timedelta(seconds=seconds)
    await member.timeout(until,reason=reason)
    m2,s2=divmod(seconds,60); h_m,m_m=divmod(m2,60)
    dur_str=f"{h_m}ч {m_m}м" if h_m else f"{m_m}м {s2}с"
    await ctx.send(embed=emb("🔇  Мут",f"**{member}** замьючен на `{dur_str}`.\nПричина: `{reason}`",C["warn"]),delete_after=15)
    await log_action("мут",ctx.author,member,reason,f"Длительность: {dur_str}")
    try: await ctx.message.delete()
    except: pass

@bot.command(name="размут",aliases=["unmute"])
@commands.has_permissions(moderate_members=True)
async def cmd_unmute(ctx,member:discord.Member=None):
    if not member:
        await ctx.send(embed=emb("❌","Пример: `!размут @user`",C["error"]),delete_after=5); return
    await member.timeout(None,reason=f"Размут от {ctx.author}")
    await ctx.send(embed=emb("🔊  Размьючен",f"**{member}** размьючен.",C["success"]),delete_after=10)
    await log_action("размут",ctx.author,member)
    try: await ctx.message.delete()
    except: pass

@bot.command(name="варн",aliases=["warn"])
@commands.has_permissions(manage_messages=True)
async def cmd_warn(ctx,member:discord.Member=None,*,reason="Не указана"):
    if not member:
        await ctx.send(embed=emb("❌","Пример: `!варн @user [причина]`",C["error"]),delete_after=5); return
    ust.add_warn(member.id); warns=ust.get_warns(member.id)
    await ctx.send(embed=emb("⚠️  Варн",f"**{member}** — причина: `{reason}`\nВсего варнов: `{warns}`",C["mod"]),delete_after=30)
    try: await member.send(embed=emb(f"⚠️  Варн на {ctx.guild.name}",f"Причина: {reason}\nВарнов: {warns}",C["mod"]))
    except: pass
    await log_action("варн",ctx.author,member,reason,f"Всего варнов: {warns}")
    if warns>=3:
        from datetime import timedelta
        try:
            await member.timeout(discord.utils.utcnow()+timedelta(hours=1),reason="Авто-мут: 3+ варна")
            await ctx.send(embed=emb("🔇  Авто-мут","3+ варна → мут на 1 час.",C["error"]),delete_after=10)
        except: pass
    try: await ctx.message.delete()
    except: pass

@bot.command(name="снятьварн",aliases=["clearwarns","unwarn"])
@commands.has_permissions(manage_messages=True)
async def cmd_clearwarns(ctx,member:discord.Member=None):
    if not member:
        await ctx.send(embed=emb("❌","Пример: `!снятьварн @user`",C["error"]),delete_after=5); return
    ust.remove_warn(member.id)
    await ctx.send(embed=emb("✅  Варн снят",f"**{member}**: `{ust.get_warns(member.id)}` варн(ов).",C["success"]),delete_after=10)
    await log_action("снятьварн",ctx.author,member)
    try: await ctx.message.delete()
    except: pass

# ═══════════════════════════════════════════════════════════
#  🎭  ТРОЛЛЬ КОМАНДЫ
# ═══════════════════════════════════════════════════════════

@bot.command(name="тролль",aliases=["troll"])
@commands.has_permissions(manage_messages=True)
async def cmd_troll(ctx,member:discord.Member=None,role_name:str="клоун",mode:str="авто"):
    if not member:
        roles_list=", ".join(FUNNY_ROLES.keys())
        await ctx.send(embed=emb("❌",
            f"Использование: `!тролль @user [роль] [режим]`\n"
            f"Роли: {roles_list}\nРежимы: авто / ручной / гибрид",C["error"]),delete_after=10)
        try: await ctx.message.delete()
        except: pass; return
    role_lower=role_name.lower()
    mode_map={"авто":"auto","auto":"auto","ручной":"manual","manual":"manual","гибрид":"hybrid","hybrid":"hybrid"}
    final_mode=mode_map.get(mode.lower(),"auto")
    if role_lower not in FUNNY_ROLES:
        await ctx.send(embed=emb("❌",f"Роль не найдена. Доступны: {', '.join(FUNNY_ROLES.keys())}",C["error"]),delete_after=8)
        try: await ctx.message.delete()
        except: pass; return
    ri=FUNNY_ROLES[role_lower]
    st.troll_targets[str(member.id)]={"role":role_lower,"mode":final_mode}; st.save()
    e=discord.Embed(title="🎭  Тролль активирован!",color=C["troll"],timestamp=datetime.now())
    e.description=(f"Участник: {member.mention}\nРоль: {ri['emoji']} **{ri['name']}**\n"
                   f"Режим: `{final_mode.upper()}`\n\nОтключить: `!тролль-стоп @user`")
    await ctx.send(embed=e,delete_after=30)
    try: await ctx.message.delete()
    except: pass

@bot.command(name="тролль-стоп",aliases=["troll-stop","trollstop"])
@commands.has_permissions(manage_messages=True)
async def cmd_troll_stop(ctx,member:discord.Member=None):
    if not member:
        await ctx.send(embed=emb("❌","Пример: `!тролль-стоп @user`",C["error"]),delete_after=5)
        try: await ctx.message.delete()
        except: pass; return
    uid_s=str(member.id)
    if uid_s in st.troll_targets: del st.troll_targets[uid_s]; st.save()
    await ctx.send(embed=emb("✅","Троллинг отключён.",C["success"]),delete_after=8)
    try: await ctx.message.delete()
    except: pass

@bot.command(name="тролль-список",aliases=["troll-list"])
@commands.has_permissions(manage_messages=True)
async def cmd_troll_list(ctx):
    if not st.troll_targets:
        await ctx.send(embed=emb("🎭","Список троллей пуст.",C["info"]),delete_after=8)
        try: await ctx.message.delete()
        except: pass; return
    lines=[]
    for uid_s,cfg in st.troll_targets.items():
        ri=FUNNY_ROLES.get(cfg["role"],{"emoji":"?","name":"?"})
        m2=ctx.guild.get_member(int(uid_s))
        name=m2.display_name if m2 else f"<@{uid_s}>"
        lines.append(f"{ri['emoji']} **{name}** — режим `{cfg['mode'].upper()}`")
    e=discord.Embed(title="🎭  Активные тролли",description="\n".join(lines),color=C["troll"],timestamp=datetime.now())
    await ctx.send(embed=e,delete_after=30)
    try: await ctx.message.delete()
    except: pass

@bot.command(name="роль-тролль",aliases=["funny-role"])
@commands.has_permissions(manage_roles=True)
async def cmd_funny_role(ctx,member:discord.Member=None,role_name:str=None):
    if not member or not role_name:
        roles_list=", ".join(f"{v['emoji']} {k}" for k,v in FUNNY_ROLES.items())
        await ctx.send(embed=emb("❌",f"`!роль-тролль @user <роль>`\nДоступные роли: {roles_list}",C["error"]),delete_after=10)
        try: await ctx.message.delete()
        except: pass; return
    role_lower=role_name.lower()
    if role_lower not in FUNNY_ROLES:
        await ctx.send(embed=emb("❌","Роль не найдена.",C["error"]),delete_after=5)
        try: await ctx.message.delete()
        except: pass; return
    ri=FUNNY_ROLES[role_lower]
    discord_role=discord.utils.get(ctx.guild.roles,name=f"{ri['emoji']} {ri['name']}")
    if not discord_role:
        try: discord_role=await ctx.guild.create_role(name=f"{ri['emoji']} {ri['name']}",color=discord.Color(0xEC4899))
        except discord.Forbidden:
            await ctx.send(embed=emb("❌","Нет прав создавать роли.",C["error"]),delete_after=5)
            try: await ctx.message.delete()
            except: pass; return
    try:
        await member.add_roles(discord_role)
        e=discord.Embed(title=f"{ri['emoji']}  Роль выдана!",color=C["troll"],timestamp=datetime.now())
        e.description=f"**{member.display_name}** теперь официально — **{ri['name']}** {ri['emoji']}"
        e.set_thumbnail(url=member.display_avatar.url)
        await ctx.send(embed=e,delete_after=30)
    except discord.Forbidden:
        await ctx.send(embed=emb("❌","Нет прав выдавать роли.",C["error"]),delete_after=5)
    try: await ctx.message.delete()
    except: pass

# ═══════════════════════════════════════════════════════════
#  🛡️  АВТО-МОД
# ═══════════════════════════════════════════════════════════

@bot.command(name="automod")
@commands.has_permissions(administrator=True)
async def cmd_automod(ctx,action:str=None,*,word:str=None):
    if not action:
        status="🟢 Включён" if st.automod_enabled else "🔴 Выключён"
        words=", ".join(f"`{w}`" for w in st.automod_words) or "Нет слов"
        await ctx.send(embed=emb("🛡️  Авто-мод",f"Статус: {status}\nСлова: {words}",C["info"]),delete_after=15)
        try: await ctx.message.delete()
        except: pass; return
    if action=="on":   st.automod_enabled=True;  st.save()
    elif action=="off": st.automod_enabled=False; st.save()
    elif action=="add" and word:
        if word.lower() not in st.automod_words: st.automod_words.append(word.lower()); st.save()
        await ctx.send(embed=emb("✅",f"Слово `{word}` добавлено.",C["success"]),delete_after=5)
    elif action=="del" and word:
        if word.lower() in st.automod_words: st.automod_words.remove(word.lower()); st.save()
        await ctx.send(embed=emb("✅",f"Слово `{word}` удалено.",C["success"]),delete_after=5)
    else:
        await ctx.send(embed=emb("❌","Использование: `!automod on|off|add <слово>|del <слово>`",C["error"]),delete_after=8)
    try: await ctx.message.delete()
    except: pass

# ═══════════════════════════════════════════════════════════
#  💰  ЭКОНОМИКА КОМАНДЫ
# ═══════════════════════════════════════════════════════════

@bot.command(name="баланс",aliases=["bal","balance","монеты"])
async def cmd_balance(ctx,member:discord.Member=None):
    target=member or ctx.author; d=eco.get_user_data(target.id)
    e=discord.Embed(title=f"💰  Баланс — {target.display_name}",color=C["gold"],timestamp=datetime.now())
    e.set_thumbnail(url=target.display_avatar.url)
    e.add_field(name="💳 Баланс",    value=f"**`{d['balance']:,}`** {COIN}",inline=True)
    e.add_field(name="💹 Заработано",value=f"`{d['total_earned']:,}` {COIN}",inline=True)
    e.add_field(name="🛒 Потрачено", value=f"`{d['total_spent']:,}` {COIN}",inline=True)
    e.set_footer(text="✦ CodeParis  •  Экономика")
    msg=await ctx.send(embed=e); asyncio.create_task(_delete_after(msg,60))
    try: await ctx.message.delete()
    except: pass

@bot.command(name="работать",aliases=["work","раб"])
async def cmd_work(ctx):
    uid=ctx.author.id; can,remaining=eco.can_work(uid)
    if not can:
        m2,s2=divmod(int(remaining),60)
        msg=await ctx.send(embed=emb("⏳  Рано!",f"Следующая работа через `{m2}м {s2:02d}с`",C["warn"]))
        asyncio.create_task(_delete_after(msg,8))
        try: await ctx.message.delete()
        except: pass; return
    owned=eco.get_income_roles(uid)
    if not owned:
        msg=await ctx.send(embed=emb("💼  Нет работы",f"Купи доходную роль в `!магазин`",C["warn"]))
        asyncio.create_task(_delete_after(msg,10))
        try: await ctx.message.delete()
        except: pass; return
    earned=eco.do_work(uid); balance=eco.get_balance(uid)
    eco.set_username(uid,ctx.author.display_name)
    e=discord.Embed(title="💼  Рабочий день!",color=C["success"],timestamp=datetime.now())
    e.description=f"**{ctx.author.display_name}** заработал!\n```\n  +{earned:,} {COIN}\n  Баланс: {balance:,} {COIN}\n```"
    e.set_footer(text=f"✦ Следующая работа через {WORK_COOLDOWN//60} мин")
    msg=await ctx.send(embed=e); asyncio.create_task(_delete_after(msg,30))
    await _check_achievements(ctx.author)
    try: await ctx.message.delete()
    except: pass

@bot.command(name="работа",aliases=["job"])
async def cmd_free_job(ctx,job_name:str=None):
    if not job_name:
        uid=ctx.author.id; lines=[]
        for j in FREE_JOBS:
            can,remaining=eco.can_free_job(uid,j["id"])
            status="✅" if can else f"⏳ {int(remaining//60)}м"
            m2,s2=divmod(j["cd"],60); h_j,m_j=divmod(m2,60)
            cd_str=f"{h_j}ч {m_j}м" if h_j else f"{m_j}м"
            lines.append(f"{j['name']} {status}  |  `{j['min']}`–`{j['max']}` {COIN}  |  `{cd_str}`")
        e=discord.Embed(title="💼  Работы",description="\n".join(lines),color=C["work"],timestamp=datetime.now())
        e.add_field(name="📖 Использование",value="`!работа дворник|курьер|пицца|такси|рыбак|фриланс`",inline=False)
        msg=await ctx.send(embed=e); asyncio.create_task(_delete_after(msg,30))
        try: await ctx.message.delete()
        except: pass; return
    job_map={"дворник":"janitor","janitor":"janitor","курьер":"courier","courier":"courier",
             "пицца":"pizza","pizza":"pizza","такси":"taxi","taxi":"taxi",
             "рыбак":"fisherman","fisherman":"fisherman","фриланс":"programmer","программист":"programmer"}
    job_id=job_map.get(job_name.strip().lower())
    if not job_id:
        msg=await ctx.send(embed=emb("❌","Работа не найдена. Доступны: дворник/курьер/пицца/такси/рыбак/фриланс",C["error"]))
        asyncio.create_task(_delete_after(msg,8))
        try: await ctx.message.delete()
        except: pass; return
    uid=ctx.author.id; can,remaining=eco.can_free_job(uid,job_id)
    if not can:
        m2,s2=divmod(int(remaining),60)
        msg=await ctx.send(embed=emb("⏳",f"Через `{m2}м {s2:02d}с`",C["warn"]))
        asyncio.create_task(_delete_after(msg,8))
        try: await ctx.message.delete()
        except: pass; return
    job=next(j for j in FREE_JOBS if j["id"]==job_id)
    earn=eco.do_free_job(uid,job_id); eco.set_username(uid,ctx.author.display_name); bal=eco.get_balance(uid)
    story=random.choice(job["stories"]).format(earn=f"{earn:,}",coin=COIN)
    e=discord.Embed(title=f"{job['name']}  •  Смена!",color=C["work"],timestamp=datetime.now())
    e.description=f"> _{story}_\n```\n  +{earn:,} {COIN}  •  Баланс: {bal:,} {COIN}\n```"
    msg=await ctx.send(embed=e); asyncio.create_task(_delete_after(msg,30))
    try: await ctx.message.delete()
    except: pass

@bot.command(name="магазин",aliases=["shop"])
async def cmd_shop(ctx):
    msg=await ctx.send(embed=make_shop_embed()); asyncio.create_task(_delete_after(msg,120))
    try: await ctx.message.delete()
    except: pass

@bot.command(name="купить",aliases=["buy"])
async def cmd_buy(ctx,*,name:str=None):
    if not name:
        await ctx.send(embed=emb("❌","Пример: `!купить новичок`",C["error"]),delete_after=5)
        try: await ctx.message.delete()
        except: pass; return
    uid=ctx.author.id; name=name.strip().lower()
    inc_match=next((r for r in INCOME_ROLES if name in r["name"].lower() or name in r["id"].lower()),None)
    if inc_match:
        if eco.has_income_role(uid,inc_match["id"]):
            e=emb("ℹ️","Уже куплено! Пиши `!работать`.",C["info"])
        elif eco.get_balance(uid)<inc_match["price"]:
            e=emb("❌  Мало монет",f"Нужно `{inc_match['price']:,}` {COIN}, у тебя `{eco.get_balance(uid):,}`",C["error"])
        else:
            eco.buy_income_role(uid,inc_match["id"],inc_match["price"])
            e=emb("✅  Куплено!",f"**{inc_match['name']}** — пиши `!работать`!\nБаланс: `{eco.get_balance(uid):,}` {COIN}",C["success"])
        msg=await ctx.send(embed=e); asyncio.create_task(_delete_after(msg,20))
        try: await ctx.message.delete()
        except: pass; return
    cos_match=next((r for r in COSMETIC_ROLES if name in r["name"].lower()),None)
    if cos_match:
        if eco.has_cosmetic_role(uid,cos_match["discord_role"]):
            e=emb("ℹ️","Уже куплено! Управляй в `!профиль`.",C["info"])
        elif eco.get_balance(uid)<cos_match["price"]:
            e=emb("❌  Мало монет",f"Нужно `{cos_match['price']:,}` {COIN}",C["error"])
        else:
            eco.buy_cosmetic_role(uid,cos_match["discord_role"],cos_match["price"])
            role_obj=ctx.guild.get_role(cos_match["discord_role"])
            if role_obj:
                try: await ctx.author.add_roles(role_obj)
                except: pass
            e=emb("✅  Куплено!",f"**{cos_match['name']}** куплена!\nБаланс: `{eco.get_balance(uid):,}` {COIN}",C["success"])
        msg=await ctx.send(embed=e); asyncio.create_task(_delete_after(msg,20))
        try: await ctx.message.delete()
        except: pass; return
    msg=await ctx.send(embed=emb("❌","Роль не найдена. Смотри `!магазин`",C["error"]))
    asyncio.create_task(_delete_after(msg,8))
    try: await ctx.message.delete()
    except: pass

@bot.command(name="профиль",aliases=["profile"])
async def cmd_profile(ctx,member:discord.Member=None):
    target=member or ctx.author
    view=ProfileCosmeticView(target) if target.id==ctx.author.id else None
    e=make_profile_embed(target)
    if view and view.children: msg=await ctx.send(embed=e,view=view)
    else: msg=await ctx.send(embed=e)
    asyncio.create_task(_delete_after(msg,90))
    try: await ctx.message.delete()
    except: pass

@bot.command(name="топмонет",aliases=["richlist"])
async def cmd_top_money(ctx):
    top=eco.get_top(10)
    e=discord.Embed(title="💰  Топ богатейших",color=C["gold"],timestamp=datetime.now())
    if not top: e.description="Пока нет данных."
    else:
        lines=[]
        for rank,(uid,bal) in enumerate(top,1):
            m2=ctx.guild.get_member(uid)
            name=discord.utils.escape_markdown(m2.display_name if m2 else f"<@{uid}>")
            lines.append(f"{medal(rank)} **{name}** — `{bal:,}` {COIN}")
        e.description="\n".join(lines)
    msg=await ctx.send(embed=e); asyncio.create_task(_delete_after(msg,60))
    try: await ctx.message.delete()
    except: pass

# ═══════════════════════════════════════════════════════════
#  📊  СТАТИСТИКА / ОБЩИЕ
# ═══════════════════════════════════════════════════════════

@bot.command(name="mystats")
async def cmd_mystats(ctx,member:discord.Member=None):
    target=member or ctx.author
    msg=await ctx.send(embed=make_personal_stats_embed(target))
    asyncio.create_task(_delete_after(msg,60))
    try: await ctx.message.delete()
    except: pass

@bot.command(name="достижения",aliases=["achievements","ачивки"])
async def cmd_achievements(ctx,member:discord.Member=None):
    target=member or ctx.author; d=ust.get_user_data(target.id); achs=d.get("achievements",[])
    e=discord.Embed(title=f"🏆  Достижения — {target.display_name}",color=C["achiev"],timestamp=datetime.now())
    e.set_thumbnail(url=target.display_avatar.url)
    if not achs: e.description="Пока нет достижений. Будь активнее!"
    else:
        lines=[f"{ACHIEVEMENTS[aid]['emoji']} **{ACHIEVEMENTS[aid]['name']}** — {ACHIEVEMENTS[aid]['desc']}"
               for aid in achs if aid in ACHIEVEMENTS]
        e.description="\n".join(lines)
        e.set_footer(text=f"Всего: {len(achs)}/{len(ACHIEVEMENTS)}")
    msg=await ctx.send(embed=e); asyncio.create_task(_delete_after(msg,60))
    try: await ctx.message.delete()
    except: pass

@bot.command(name="leaderboard",aliases=["lb","топ"])
async def cmd_leaderboard(ctx):
    await ctx.send(embed=emb("⏳","Генерирую...",C["info"]),delete_after=5)
    try: await ctx.message.delete()
    except: pass
    await _post_stats_chart()

@bot.command(name="пинг",aliases=["ping"])
async def cmd_ping(ctx):
    ms=round(bot.latency*1000)
    msg=await ctx.send(embed=emb("🏓 Пинг",f"**{ms} мс**",C["success"] if ms<100 else C["warn"] if ms<200 else C["error"]))
    asyncio.create_task(_delete_after(msg,5))

# ═══════════════════════════════════════════════════════════
#  👑  КОМАНДЫ АДМИНИСТРАТОРА
# ═══════════════════════════════════════════════════════════

@bot.command(name="с")
@commands.has_permissions(manage_messages=True)
async def cmd_clear(ctx,amount:int=None):
    if not amount or not 1<=amount<=1000:
        await ctx.send(embed=emb("❌","Пример: `!с 50`",C["error"]),delete_after=5)
        try: await ctx.message.delete()
        except: pass; return
    try: await ctx.message.delete()
    except: pass
    deleted=await ctx.channel.purge(limit=amount)
    msg=await ctx.send(embed=emb("🗑️  Очищено",f"Удалено: **{len(deleted)}**",C["success"]))
    await asyncio.sleep(4)
    try: await msg.delete()
    except: pass

@bot.command(name="say")
@admin_only()
async def cmd_say(ctx,*,text:str):
    ch=bot.get_channel(AI_CHANNEL_ID)
    if not ch: await ctx.send(embed=emb("❌","Канал не найден!",C["error"]),delete_after=4); return
    await ch.send(embed=ai_embed(text),view=AIMessageView())
    await ctx.send(embed=emb("✅","Отправлено.",C["success"]),delete_after=4)
    try: await ctx.message.delete()
    except: pass

@bot.command(name="givemoney")
@admin_only()
async def cmd_givemoney(ctx,member:discord.Member=None,amount:int=None):
    if not member or not amount:
        await ctx.send(embed=emb("❌","Пример: `!givemoney @user 5000`",C["error"]),delete_after=5)
        try: await ctx.message.delete()
        except: pass; return
    eco.add_balance(member.id,amount)
    await ctx.send(embed=emb("✅",f"**{member}** получил `{amount:,}` {COIN}\nБаланс: `{eco.get_balance(member.id):,}`",C["success"]),delete_after=8)
    try: await ctx.message.delete()
    except: pass

@bot.command(name="reseteco")
@admin_only()
async def cmd_reseteco(ctx,user_id:str=None):
    if user_id:
        try: eco.reset_user(int(user_id))
        except: await ctx.send(embed=emb("❌","Укажи ID.",C["error"]),delete_after=5); return
    else: eco.reset_all()
    await ctx.send(embed=emb("✅","Сброшено.",C["success"]),delete_after=5)
    try: await ctx.message.delete()
    except: pass

@bot.command(name="resetstats")
@admin_only()
async def cmd_resetstats(ctx,user_id:str=None):
    if user_id:
        k=str(user_id)
        if k in ust._data: del ust._data[k]; ust.save()
    else: ust._data.clear(); ust.save()
    await ctx.send(embed=emb("✅","Статистика сброшена.",C["success"]),delete_after=5)
    try: await ctx.message.delete()
    except: pass

@bot.command(name="reverify")
@admin_only()
async def cmd_reverify(ctx):
    st.verify_msg=None; await _ensure_verify_posted()
    await ctx.send(embed=emb("✅","Верификация пересоздана.",C["success"]),delete_after=5)
    try: await ctx.message.delete()
    except: pass

@bot.command(name="reticket")
@admin_only()
async def cmd_reticket(ctx):
    st.ticket_msg=None; await _ensure_ticket_posted()
    await ctx.send(embed=emb("✅","Тикет-панель обновлена.",C["success"]),delete_after=5)
    try: await ctx.message.delete()
    except: pass

@bot.command(name="postnews")
@admin_only()
async def cmd_postnews(ctx,*,custom_topic:str=None):
    try: await ctx.message.delete()
    except: pass
    await ctx.send(embed=emb("⏳","Генерирую...",""),delete_after=5)
    ch=bot.get_channel(NEWS_CHANNEL_ID)
    if not ch: return
    topic=custom_topic or random.choice(NEWS_TOPICS); text=await ai.generate_news(topic)
    st.news_counter+=1; st.save()
    e=discord.Embed(color=C["news"],timestamp=datetime.now())
    e.title=f"📰  Новости CodeParis #{st.news_counter}"; e.description=text
    e.set_footer(text="✦ Vemby  •  Авто-новости"); await ch.send(embed=e)

@bot.command(name="autonews")
@admin_only()
async def cmd_autonews(ctx,action:str=None,value:str=None):
    try: await ctx.message.delete()
    except: pass
    if action=="on": st.autonews_on=True; st.save()
    elif action=="off": st.autonews_on=False; st.save()
    elif action=="interval" and value:
        try:
            h=int(value)
            if 1<=h<=48: st.news_hours=h; st.save()
        except: pass
    status="🟢 Включены" if st.autonews_on else "🔴 Выключены"
    await ctx.send(embed=emb("📰",f"{status}  •  интервал `{st.news_hours}ч`",C["news"]),delete_after=8)

@bot.command(name="welcome-toggle",aliases=["приветствия"])
@admin_only()
async def cmd_welcome_toggle(ctx):
    st.welcome_enabled=not st.welcome_enabled; st.save()
    status="🟢 Включены" if st.welcome_enabled else "🔴 Выключены"
    await ctx.send(embed=emb("👋",f"Приветствия: {status}",C["success"]),delete_after=5)
    try: await ctx.message.delete()
    except: pass

@bot.command(name="help")
@admin_only()
async def cmd_help(ctx):
    e=discord.Embed(title="✦  Команды — CodeParis v6.0",color=C["panel"],timestamp=datetime.now())
    e.add_field(name="🛡️  МОДЕРАЦИЯ",
                value="`!бан @u [причина]`  `!кик @u [причина]`\n`!мут @u [10m] [причина]`  `!размут @u`\n`!варн @u [причина]`  `!снятьварн @u`  `!с <N>`",inline=False)
    e.add_field(name="🎭  ТРОЛЛИ",
                value="`!тролль @u [роль] [режим]`  `!тролль-стоп @u`  `!тролль-список`\n`!роль-тролль @u <роль>`\nРоли: клоун/рыба/уточка/картошка/скелет  •  Режимы: авто/ручной/гибрид",inline=False)
    e.add_field(name="🛡️  АВТО-МОД",
                value="`!automod on|off|add <слово>|del <слово>`",inline=False)
    e.add_field(name="💰  ЭКОНОМИКА",
                value="`!баланс`  `!работать`  `!работа <тип>`  `!магазин`  `!купить`  `!профиль`  `!топмонет`\n`!givemoney @u <N>`  `!reseteco [id]`",inline=False)
    e.add_field(name="📊  СТАТИСТИКА",
                value="`!mystats [@u]`  `!достижения [@u]`  `!lb`  `!пинг`  `!resetstats [id]`",inline=False)
    e.add_field(name="👑  УПРАВЛЕНИЕ",
                value="`!say <текст>`  `!postnews [тема]`  `!autonews on|off|interval <ч>`\n`!reverify`  `!reticket`  `!welcome-toggle`",inline=False)
    e.set_footer(text="✦ CodeParis Admin Panel  v6.0")
    await ctx.send(embed=e,delete_after=60)
    try: await ctx.message.delete()
    except: pass

# ═══════════════════════════════════════════════════════════
#  🚀  ЗАПУСК
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    if not TOKEN:
        print("❌ BOT_TOKEN не найден! Укажи в Railway → Variables")
        sys.exit(1)
    print(f"✅ Токен: {TOKEN[:10]}...")
    print(f"✅ GROQ:  {'найден' if GROQ_API_KEY else '❌ НЕ ЗАДАН'}")
    print(f"✅ DATA:  {DATA_DIR}")
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("❌ Неверный токен!"); sys.exit(1)
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}"); sys.exit(1)
