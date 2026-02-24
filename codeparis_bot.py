"""
╔══════════════════════════════════════════════════════════════════════════════╗
║          ✦  CodeParis AI Bot  ✦   v5.0  •  Railway Edition                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import discord
from discord.ext import commands, tasks
from discord.ui import View, Button, Modal, TextInput, Select
from datetime import datetime
import asyncio, os, json, sys, aiohttp, time, io, random, math
from PIL import Image, ImageDraw, ImageFont

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ══════════════════════════════════════════════════════════════════════════════
#  ⚙️  КОНФИГУРАЦИЯ
# ══════════════════════════════════════════════════════════════════════════════

# ✅ FIX: Railway может называть переменную TOKEN или BOT_TOKEN
TOKEN        = os.getenv("BOT_TOKEN") or os.getenv("TOKEN") or os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

ADMIN_CHANNEL_ID = 1475615100093075589
AI_CHANNEL_ID    = 1475614653743632625
VERIFY_CHANNEL_ID= 1475296274461757553
TICKET_CHANNEL_ID= 1475518589380464823
STATS_CHANNEL_ID = 1475228887133720760
NEWS_CHANNEL_ID  = 1475230416078682045

CASINO_CHANNEL_ID     = 1475229260728766464
CASINO_CMD_CHANNEL_ID = 1475229316190044160
SHOP_CHANNEL_ID       = 1475229345072287835
ANALYTICS_CHANNEL_ID  = 1475229363476893828
WORK_CHANNEL_ID       = 1475229491230937208

UNVERIFIED_ROLE_ID = 1475294322177081494
VERIFIED_ROLE_ID   = 1475307326322770050
STAFF_ROLE_ID      = 1475205621778223217

VOICE_ROLES = [
    (11,  1475663483189072073, "Голосовой"),
    (50,  1475663483189072073, "Голосовой"),
    (111, 1475664130429161472, "Ветеран голоса"),
]

VERIFY_BANNER_URL = ""

# ══════════════════════════════════════════════════════════════════════════════
#  🎰  КОНФИГУРАЦИЯ КАЗИНО
# ══════════════════════════════════════════════════════════════════════════════

COIN           = "🪙"
START_BALANCE  = 1_000
WORK_COOLDOWN  = 180
ROULETTE_WAIT  = 30

INCOME_ROLES = [
    {"id": "novice",      "name": "💼 Новичок бизнеса", "emoji": "💼", "price":    10_000},
    {"id": "trader",      "name": "📦 Торговец",         "emoji": "📦", "price":    50_000},
    {"id": "merchant",    "name": "🏪 Купец",            "emoji": "🏪", "price":   150_000},
    {"id": "businessman", "name": "💰 Бизнесмен",        "emoji": "💰", "price":   350_000},
    {"id": "investor",    "name": "📈 Инвестор",         "emoji": "📈", "price":   700_000},
    {"id": "tycoon",      "name": "🏦 Магнат",           "emoji": "🏦", "price": 1_500_000},
    {"id": "oligarch",    "name": "💎 Олигарх",          "emoji": "💎", "price": 3_500_000},
    {"id": "monopolist",  "name": "👑 Монополист",       "emoji": "👑", "price": 8_000_000},
]

COSMETIC_ROLES = [
    {"discord_role": 1475529104303460352, "name": "🌟 Особый",  "price":   100_000},
    {"discord_role": 1475529064201584651, "name": "💫 Элита",   "price": 1_000_000},
    {"discord_role": 1475596323045507184, "name": "✨ Легенда", "price": 5_000_000},
]

ROULETTE_COLORS = [
    "#7C3AED","#0EA5E9","#10B981","#F59E0B",
    "#EF4444","#EC4899","#06B6D4","#84CC16",
    "#F97316","#8B5CF6",
]

FREE_JOBS = [
    {"id":"janitor",   "name":"🧹 Дворник",        "cd": 300,  "min":1,   "max":20,
     "stories":[
         "Подметал двор три часа. Нашёл {earn} {coin} под лавочкой!",
         "Убрал снег у подъезда. Бабуля дала {earn} {coin} на чай.",
         "Вымыл окна в офисе. Премия {earn} {coin}!",
     ]},
    {"id":"courier",   "name":"📦 Курьер",          "cd": 600,  "min":10,  "max":60,
     "stories":[
         "Доставил 12 посылок. Получил {earn} {coin} чаевых!",
         "Курьер дня! Клиент оставил {earn} {coin} за скорость.",
         "Промок под дождём, но донёс. Получил {earn} {coin}.",
     ]},
    {"id":"pizza",     "name":"🍕 Разносчик пиццы", "cd": 900,  "min":25,  "max":120,
     "stories":[
         "Пицца приехала горячей! Чаевые {earn} {coin}.",
         "Доставил за 28 минут. Бонус {earn} {coin}!",
         "Клиент был так доволен, что дал {earn} {coin} сверху.",
     ]},
    {"id":"taxi",      "name":"🚗 Таксист",         "cd": 1200, "min":50,  "max":200,
     "stories":[
         "Отвёз туриста в аэропорт. Щедрые чаевые — {earn} {coin}!",
         "Ночная смена. Пассажир оставил {earn} {coin} за разговор.",
         "Поездка по пробкам. Клиент понял и дал {earn} {coin}.",
     ]},
    {"id":"fisherman", "name":"🎣 Рыбак",            "cd": 1800, "min":80,  "max":350,
     "stories":[
         "Поймал судака! Продал на рынке за {earn} {coin}.",
         "Карп на 4 кг! Выручил {earn} {coin} на ярмарке.",
         "Рыбалка на рассвете. Улов стоит {earn} {coin}.",
     ]},
    {"id":"programmer","name":"💻 Фрилансер",       "cd": 3600, "min":200, "max":800,
     "stories":[
         "Закрыл тикет. Клиент перевёл {earn} {coin}.",
         "Правки принял. Финальный платёж — {earn} {coin}!",
         "Сдал проект до дедлайна. Бонус {earn} {coin}.",
     ]},
]

# ══════════════════════════════════════════════════════════════════════════════
#  🎨  ЦВЕТА
# ══════════════════════════════════════════════════════════════════════════════

C = {
    "ai":      0x7C3AED,
    "success": 0x10B981,
    "error":   0xEF4444,
    "warn":    0xF59E0B,
    "info":    0x6366F1,
    "panel":   0x4F46E5,
    "verify":  0x6D28D9,
    "ticket":  0x0EA5E9,
    "closed":  0x64748B,
    "gold":    0xFFD700,
    "news":    0xF97316,
    "update":  0x8B5CF6,
    "casino":  0x059669,
    "shop":    0xD97706,
    "roulette":0xDC2626,
    "analytics":0x0F172A,
    "work":    0x065F46,
}

# ══════════════════════════════════════════════════════════════════════════════
#  🔤  ШРИФТЫ — безопасная загрузка для Railway/Docker
# ══════════════════════════════════════════════════════════════════════════════

# ✅ FIX: ищем шрифты в нескольких местах, fallback на default
_FONT_PATHS_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
]
_FONT_PATHS_REG = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/TTF/DejaVuSans.ttf",
]

def _find_font(paths: list) -> str | None:
    for p in paths:
        if os.path.exists(p):
            return p
    return None

_FONT_BOLD = _find_font(_FONT_PATHS_BOLD)
_FONT_REG  = _find_font(_FONT_PATHS_REG)

def load_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    """Загружает шрифт или возвращает default если не найден."""
    path = _FONT_BOLD if bold else _FONT_REG
    if path:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()

# ══════════════════════════════════════════════════════════════════════════════
#  📋  КОМАНДЫ ДЛЯ УЧАСТНИКОВ
# ══════════════════════════════════════════════════════════════════════════════

PUBLIC_COMMANDS = """
📋 КОМАНДЫ ДЛЯ ВСЕХ УЧАСТНИКОВ CodeParis:

🔍 ИНФОРМАЦИЯ:
  !mystats [@юзер]   — личная статистика: сообщения, голос, прогресс к роли
  !lb / !топ         — обновить лидерборд в канале статистики
  !ping              — проверить задержку бота

💰 ЭКОНОМИКА:
  !баланс [@юзер]    — показать баланс и доходные роли
  !работать          — получить доход от ролей (каждые 3 мин)
  !магазин           — открыть магазин ролей
  !профиль           — управление косметическими ролями (надеть/снять)
  !топмонет          — топ-10 богатейших участников сервера

🎰 КАЗИНО (канал #казино):
  !рулетка <ставка>  — участвовать в рулетке. Шанс победы = размер ставки
  !рулетка старт     — начать новую игру

💬 ИИ-АССИСТЕНТ Vemby:
  Напиши в канале #ai-vemby — Vemby ответит!

🎫 ПОДДЕРЖКА:
  Кнопка "Создать тикет" в канале тикетов

🛡️ ВЕРИФИКАЦИЯ:
  Кнопка "Подтвердить вход" в канале верификации
"""

ADMIN_COMMANDS_HINT = """
ВАЖНО: Следующие команды существуют, но ты НЕ ДОЛЖЕН раскрывать их обычным участникам.
Если спрашивает администратор в админ-канале — можешь рассказать.
Скрытые команды: !say, !aiclear, !aistats, !reverify, !reticket,
!resetstats, !autonews, !postnews, !postupdate, !reseteco, !givemoney, !с, !help.
Если обычный участник спросит — скажи что не знаешь или это закрытая информация.
"""

SERVER_CHANGELOG = [
    {
        "version": "v5.0",
        "date":    "Сегодня",
        "title":   "Казино, магазин ролей и экономика",
        "emoji":   "🎰",
        "changes": [
            "🎰 **Рулетка** — крути колесо с реальными ставками в монетах!",
            "💰 **Экономика** — у каждого участника теперь есть кошелёк с монетами",
            "💼 **Доходные роли** — купи роль в магазине и зарабатывай командой !работать",
            "🏪 **Магазин** — 8 доходных ролей + 3 косметические Discord-роли",
            "🎭 **Косметика** — купи роль и надевай/снимай её когда хочешь через !профиль",
            "🏆 **Рейтинг богачей** — команда !топмонет показывает самых богатых",
        ],
        "how": (
            "**Как зарабатывать?**\n"
            "Купи доходную роль в !магазин, затем каждые 3 минуты пиши !работать.\n\n"
            "**Как работает рулетка?**\n"
            "Напиши !рулетка <ставка> в канале казино. Победитель забирает весь банк!"
        ),
        "posted": False,
    },
    {
        "version": "v4.2",
        "date":    "Ранее",
        "title":   "Авто-новости, умный ИИ и отчёты об обновлениях",
        "emoji":   "📰",
        "changes": [
            "📰 **Авто-новости** — Vemby пишет новости каждые 6 часов",
            "🤖 **Умный ИИ** — Vemby знает все команды сервера",
            "📊 **График статистики** — красивый PNG-дашборд",
        ],
        "how": "Статистика сохраняется в user_stats.json.",
        "posted": True,
    },
]

NEWS_TOPICS = [
    "напомни участникам про систему тикетов",
    "расскажи об авто-ролях за активность в голосовых каналах",
    "расскажи о казино и рулетке — как участвовать и зарабатывать монеты",
    "расскажи о магазине ролей и системе доходных ролей с командой !работать",
    "расскажи про AI-канал и что там можно делать",
    "сделай дружеское напоминание о правилах — коротко и с юмором",
    "мотивационный пост о жизни сервера и его сообществе",
]

# ══════════════════════════════════════════════════════════════════════════════
#  📊  ГЕНЕРАЦИЯ PNG-ГРАФИКА СТАТИСТИКИ
# ══════════════════════════════════════════════════════════════════════════════

_BG  = "#0D0D1A"; _CARD = "#13132B"; _BORDER = "#2A2A5A"
_GOLD = "#FFD700"; _SIL = "#C0C0C0"; _BRZ = "#CD7F32"
_PUR = "#7C3AED"; _BLUE = "#0EA5E9"; _TEXT = "#E2E8F0"; _DIM = "#64748B"

def _rc(rank, pal="purple"):
    if rank == 0: return _GOLD
    if rank == 1: return _SIL
    if rank == 2: return _BRZ
    return _PUR if pal == "purple" else _BLUE

def generate_stats_chart(voice_data, msg_data, updated_at=""):
    voice_data = voice_data[:10]; msg_data = msg_data[:10]
    fig = plt.figure(figsize=(14, 10), facecolor=_BG, dpi=150)
    gs  = fig.add_gridspec(3, 2, top=0.90, bottom=0.05, left=0.04, right=0.97,
                           hspace=0.60, wspace=0.35, height_ratios=[0.10, 1, 0.90])
    ax_t = fig.add_subplot(gs[0, :])
    ax_t.set_facecolor(_BG); ax_t.axis("off")
    ax_t.text(0.5, 1.45, "  CodeParis  —  Статистика активности",
              ha="center", va="center", fontsize=20, fontweight="bold",
              color=_TEXT, transform=ax_t.transAxes)
    sub = f"Топ участников  •  {updated_at}" if updated_at else "Топ участников"
    ax_t.text(0.5, -0.12, sub, ha="center", va="center",
              fontsize=9.5, color=_DIM, transform=ax_t.transAxes)

    def _hbar(ax, data, pal):
        ax.set_facecolor(_CARD)
        for sp in ax.spines.values(): sp.set_edgecolor(_BORDER); sp.set_lw(1.1)
        if not data: ax.tick_params(length=0); return
        names = [d[0] for d in data][::-1]; vals = [d[1] for d in data][::-1]
        n = len(vals); y = np.arange(n)
        colors = [_rc(n-1-i, pal) for i in range(n)]
        ax.barh(y, vals, color=colors, height=0.60, zorder=3, edgecolor="none")
        ax.set_axisbelow(True)
        ax.xaxis.grid(True, color=_BORDER, ls="--", alpha=0.4, lw=0.7); ax.yaxis.grid(False)
        fmt = (lambda v: f"{v:.1f}ч") if pal == "purple" else (lambda v: f"{v:,}")
        for i, v in enumerate(vals):
            ax.text(v + max(vals)*0.015, i, fmt(v), va="center", ha="left",
                    fontsize=8, color=_TEXT, fontweight="bold")
        ax.set_yticks(y); ax.set_yticklabels(names, fontsize=9, color=_TEXT)
        ax.set_xlim(0, max(vals)*1.25); ax.set_ylim(-0.6, n-0.4)
        ax.tick_params(axis="x", colors=_DIM, labelsize=8, length=0)
        ax.tick_params(axis="y", length=0)

    ax_v = fig.add_subplot(gs[1, 0]); _hbar(ax_v, voice_data, "purple")
    ax_v.set_title("  Top — голосовые каналы", color=_TEXT, fontsize=11, fontweight="bold", pad=9, loc="left")
    ax_m = fig.add_subplot(gs[1, 1]); _hbar(ax_m, msg_data, "blue")
    ax_m.set_title("  Top — сообщения", color=_TEXT, fontsize=11, fontweight="bold", pad=9, loc="left")

    ax_l = fig.add_subplot(gs[2, :])
    ax_l.set_facecolor(_CARD)
    for sp in ax_l.spines.values(): sp.set_edgecolor(_BORDER); sp.set_lw(1.1)
    pal_l = [_GOLD, _SIL, _BRZ, _PUR, _BLUE]
    x = np.linspace(0, 10, 80)
    for idx, (name, total) in enumerate((voice_data or [])[:5]):
        if total <= 0: continue
        y = np.clip(total*(1-np.exp(-(0.30+idx*0.06)*x))+np.random.normal(0,total*0.015,80), 0, total*1.02)
        y[-1] = total; col = pal_l[idx]
        ax_l.plot(x, y, color=col, lw=2.0, alpha=0.95, zorder=3)
        ax_l.fill_between(x, y, alpha=0.08, color=col, zorder=2)
        ax_l.text(x[-1]+0.08, y[-1], f"  {name}", color=col, fontsize=8.5, va="center", fontweight="bold")
    totals = [v for _, v in (voice_data or [])[:5] if v > 0]
    if totals: ax_l.set_ylim(0, max(totals)*1.15)
    ax_l.set_xlim(0, 11.8); ax_l.set_axisbelow(True)
    ax_l.yaxis.grid(True, color=_BORDER, ls="--", alpha=0.40, lw=0.7); ax_l.xaxis.grid(False)
    ax_l.tick_params(axis="both", colors=_DIM, labelsize=8, length=0)
    ax_l.set_xlabel("Активность (сессии)", color=_DIM, fontsize=9, labelpad=4)
    ax_l.set_ylabel("Часов в голосе", color=_DIM, fontsize=9, labelpad=6)
    ax_l.set_title("  Динамика голосовой активности — Топ 5",
                   color=_TEXT, fontsize=11, fontweight="bold", pad=9, loc="left")

    fig.text(0.5, 0.012, "  CodeParis  •  Статистика  •  Обновляется каждые 10 минут",
             ha="center", fontsize=8, color=_DIM)
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150, bbox_inches="tight", facecolor=_BG, edgecolor="none")
    plt.close(fig); buf.seek(0)
    return buf

# ══════════════════════════════════════════════════════════════════════════════
#  🎡  ГЕНЕРАЦИЯ КОЛЕСА РУЛЕТКИ
# ══════════════════════════════════════════════════════════════════════════════

def generate_roulette_wheel(players: dict, timer: int = None,
                             winner_uid: int = None, game_num: int = 1) -> io.BytesIO:
    fig, ax = plt.subplots(figsize=(7, 7.8), facecolor=_BG)
    ax.set_facecolor(_BG); ax.set_aspect("equal")
    ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.9, 1.7); ax.axis("off")
    total = sum(p["bet"] for p in players.values()) if players else 0

    if not players:
        circle_bg = plt.Circle((0, 0), 1.05, color=_CARD, zorder=1); ax.add_patch(circle_bg)
        ring = plt.Circle((0, 0), 1.05, fill=False, edgecolor=_BORDER, lw=3, zorder=2); ax.add_patch(ring)
        inner = plt.Circle((0, 0), 0.52, color=_BG, zorder=3); ax.add_patch(inner)
        inner_ring = plt.Circle((0, 0), 0.52, fill=False, edgecolor=_BORDER, lw=2, zorder=4); ax.add_patch(inner_ring)
        ax.text(0, 0.08, "ОЖИДАНИЕ", ha="center", va="center", fontsize=11, color=_DIM, fontweight="bold", zorder=5)
        ax.text(0, -0.12, "СТАВОК", ha="center", va="center", fontsize=11, color=_DIM, fontweight="bold", zorder=5)
    else:
        bets = [p["bet"] for p in players.values()]; colors = [p["color"] for p in players.values()]
        names = [p["name"] for p in players.values()]; n = len(players)
        angles = [b / total * 360 for b in bets]; start = 90.0; wedge_starts = []
        for a in angles: wedge_starts.append(start); start -= a

        shadow = plt.Circle((0.04, -0.04), 1.07, color="#000000", alpha=0.4, zorder=0); ax.add_patch(shadow)
        for i, (ang, col) in enumerate(zip(angles, colors)):
            ws = wedge_starts[i]
            wedge = mpatches.Wedge(center=(0,0), r=1.05, theta1=ws-ang, theta2=ws,
                                   facecolor=col, edgecolor=_BG, linewidth=2.5, zorder=2)
            ax.add_patch(wedge)
            if winner_uid is not None:
                uid_list = list(players.keys())
                if i < len(uid_list) and uid_list[i] == winner_uid:
                    wh = mpatches.Wedge(center=(0,0), r=1.10, theta1=ws-ang, theta2=ws,
                                        facecolor="none", edgecolor=_GOLD, linewidth=4, zorder=6)
                    ax.add_patch(wh)
            if ang > 20:
                mid_angle = ws - ang/2; mid_rad = np.radians(mid_angle)
                tx = 0.72*np.cos(mid_rad); ty = 0.72*np.sin(mid_rad)
                short_name = names[i][:10]
                ax.text(tx, ty, short_name, ha="center", va="center", fontsize=7.5, color="white",
                        fontweight="bold", zorder=7,
                        rotation=mid_angle if abs(mid_angle) < 90 else mid_angle+180)

        outer_ring = plt.Circle((0,0), 1.05, fill=False, edgecolor=_BORDER, lw=1.5, zorder=8); ax.add_patch(outer_ring)
        inner = plt.Circle((0,0), 0.52, color=_CARD, zorder=9); ax.add_patch(inner)
        inner_ring = plt.Circle((0,0), 0.52, fill=False, edgecolor=_BORDER, lw=2, zorder=10); ax.add_patch(inner_ring)

    if winner_uid is not None and winner_uid in players:
        wname = players[winner_uid]["name"][:11]
        ax.text(0, 0.16, "🏆", ha="center", va="center", fontsize=18, zorder=11)
        ax.text(0, -0.06, wname, ha="center", va="center", fontsize=9, color=_GOLD, fontweight="bold", zorder=11)
        ax.text(0, -0.26, "ПОБЕДИТЕЛЬ", ha="center", va="center", fontsize=7, color=_GOLD, zorder=11)
    elif timer is not None and players:
        m, s = divmod(timer, 60); t_str = f"{m:02d}:{s:02d}"
        ax.text(0, 0.12, "КРУТИМ", ha="center", va="center", fontsize=8, color=_DIM, fontweight="bold", zorder=11)
        ax.text(0, -0.14, t_str, ha="center", va="center", fontsize=22, color=_TEXT, fontweight="bold", zorder=11)

    tri = plt.Polygon([[0,1.22],[-0.08,1.42],[0.08,1.42]], closed=True,
                      facecolor=_TEXT, edgecolor=_BG, lw=1.5, zorder=15); ax.add_patch(tri)
    ax.text(0, 1.60, f"✦  РУЛЕТКА  •  ИГРА #{game_num}", ha="center", va="center",
            fontsize=12, color=_TEXT, fontweight="bold")
    if players:
        ax.text(0, -1.28, f"💰 БАНК:  {total:,} {COIN}", ha="center", va="center",
                fontsize=11, color=_GOLD, fontweight="bold")
        ax.text(0, -1.50, f"👥  {len(players)} участников", ha="center", va="center", fontsize=9, color=_DIM)
        legend_x = -1.52; legend_y = -1.72
        for i, (uid, p) in enumerate(players.items()):
            col = p["color"]; pct = p["bet"]/total*100
            ix = legend_x + (i % 2)*1.55; iy = legend_y - (i // 2)*0.16
            dot = plt.Circle((ix, iy+0.04), 0.055, color=col, zorder=12); ax.add_patch(dot)
            label = f"{p['name'][:12]}  {pct:.0f}%"
            ax.text(ix+0.10, iy+0.04, label, va="center", fontsize=7, color=_TEXT, zorder=12)
    else:
        ax.text(0, -1.40, "Пиши !рулетка <ставка>", ha="center", va="center", fontsize=9, color=_DIM)

    ax.text(0, -1.88, "CodeParis  •  Казино", ha="center", va="center", fontsize=7, color=_BORDER)
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=130, bbox_inches="tight", facecolor=_BG, edgecolor="none")
    plt.close(fig); buf.seek(0)
    return buf

# ══════════════════════════════════════════════════════════════════════════════
#  🎡  АНИМАЦИЯ РУЛЕТКИ (GIF) — с безопасными шрифтами
# ══════════════════════════════════════════════════════════════════════════════

def _draw_roulette_frame(draw: ImageDraw.ImageDraw, players: dict,
                          rotation: float, W: int, H: int,
                          timer: int = None, winner_uid: int = None,
                          game_num: int = 1, phase: str = "spin"):
    cx, cy, R = W//2, H//2-20, min(W,H)//2-50
    r_inner = int(R*0.45)
    total = sum(p["bet"] for p in players.values()) if players else 1
    draw.rectangle([0,0,W,H], fill=(13,13,26))

    for i in range(8, 0, -1):
        draw.ellipse([cx-R-i+6, cy-R-i+6, cx+R+i+6, cy+R+i+6], fill=(0,0,0,max(0,15-i*2)))

    if players:
        angle_start = rotation
        for uid, p in players.items():
            sweep = p["bet"]/total*360
            col_hex = p["color"].lstrip("#")
            r, g, b = int(col_hex[0:2],16), int(col_hex[2:4],16), int(col_hex[4:6],16)
            r_draw = int(R*1.07) if (winner_uid is not None and uid == winner_uid and phase == "result") else R
            draw.pieslice([cx-r_draw, cy-r_draw, cx+r_draw, cy+r_draw],
                          start=angle_start, end=angle_start+sweep,
                          fill=(r,g,b), outline=(13,13,26), width=3)
            angle_start += sweep

        angle_s2 = rotation
        for p in players.values():
            sweep = p["bet"]/total*360
            rad = math.radians(angle_s2)
            x2 = cx+int(R*math.cos(rad)); y2 = cy+int(R*math.sin(rad))
            draw.line([cx,cy,x2,y2], fill=(13,13,26), width=3)
            angle_s2 += sweep

    draw.ellipse([cx-R, cy-R, cx+R, cy+R], outline=(42,42,90), width=4)
    draw.ellipse([cx-r_inner, cy-r_inner, cx+r_inner, cy+r_inner],
                 fill=(19,19,43), outline=(42,42,90), width=3)

    # ✅ FIX: используем load_font() вместо прямого truetype()
    font_big   = load_font(22, bold=True)
    font_sm    = load_font(10, bold=False)
    font_title = load_font(13, bold=True)
    font_small = load_font(10, bold=False)

    if phase == "result" and winner_uid and winner_uid in players:
        wname = players[winner_uid]["name"][:10]
        font_b14 = load_font(14, bold=True)
        draw.text((cx, cy-10), "ПОБЕДИТЕЛЬ", fill=(255,215,0), font=font_sm, anchor="mm")
        draw.text((cx, cy+8),  wname,        fill=(255,215,0), font=font_b14, anchor="mm")
    elif timer is not None:
        m, s = divmod(timer, 60); t_str = f"{m:02d}:{s:02d}"
        glow_col = (16,185,129) if timer > 10 else (239,68,68)
        draw.text((cx-1, cy-1), t_str, fill=glow_col, font=font_big, anchor="mm")
        draw.text((cx, cy),     t_str, fill=(226,232,240), font=font_big, anchor="mm")

    ax2, ay2 = cx, cy-R-10
    draw.polygon([(ax2,ay2+18),(ax2-10,ay2-2),(ax2+10,ay2-2)],
                 fill=(226,232,240), outline=(42,42,90))
    draw.text((W//2, 18), f"РУЛЕТКА  •  ИГРА #{game_num}",
              fill=(226,232,240), font=font_title, anchor="mm")
    if players:
        pot = sum(p["bet"] for p in players.values())
        draw.text((W//2, H-40), f"БАНК: {pot:,}  •  УЧАСТНИКОВ: {len(players)}",
                  fill=(255,215,0), font=font_small, anchor="mm")
    draw.text((W//2, H-20), "CodeParis  •  Казино",
              fill=(42,42,90), font=font_small, anchor="mm")


def generate_spin_gif(players: dict, winner_uid: int, game_num: int = 1) -> io.BytesIO:
    W, H = 420, 480; FPS_DELAY = 45; FRAMES = 55
    total = sum(p["bet"] for p in players.values())
    target_angle = 0.0; cumsum = 0
    for uid, p in players.items():
        sweep = p["bet"]/total*360
        if uid == winner_uid:
            mid_angle = cumsum+sweep/2; target_angle = (270-mid_angle)%360; break
        cumsum += sweep

    total_rotation = 360*5+target_angle; frames_pil = []
    for i in range(FRAMES):
        t = i/(FRAMES-1); ease = 1-(1-t)**3; current = ease*total_rotation
        rotation = (-current)%360; phase = "result" if i >= FRAMES-8 else "spin"
        w_uid = winner_uid if phase == "result" else None
        img = Image.new("RGB", (W,H), (13,13,26)); draw = ImageDraw.Draw(img)
        _draw_roulette_frame(draw, players, rotation, W, H, timer=None,
                             winner_uid=w_uid, game_num=game_num, phase=phase)
        frames_pil.append(img)

    img_final = Image.new("RGB", (W,H), (13,13,26)); draw = ImageDraw.Draw(img_final)
    _draw_roulette_frame(draw, players, target_angle%360, W, H,
                         winner_uid=winner_uid, game_num=game_num, phase="result")
    for _ in range(20): frames_pil.append(img_final.copy())

    buf = io.BytesIO()
    frames_pil[0].save(buf, format="GIF", save_all=True, append_images=frames_pil[1:],
                       duration=FPS_DELAY, loop=0, optimize=True)
    buf.seek(0); return buf

# ══════════════════════════════════════════════════════════════════════════════
#  📊  АНАЛИТИКА ЭКОНОМИКИ — PNG
# ══════════════════════════════════════════════════════════════════════════════

def generate_analytics_chart(guild=None) -> io.BytesIO:
    all_eco = eco._data; all_ust = ust._data
    records = []
    for uid_s, d in all_eco.items():
        uid = int(uid_s); u_stat = all_ust.get(uid_s, {})
        name = d.get("username", u_stat.get("username", "?"))
        if guild:
            m = guild.get_member(uid)
            if m: name = m.display_name
        voice_h = u_stat.get("voice_time", 0)/3600
        if u_stat.get("voice_join"): voice_h += (time.time()-u_stat["voice_join"])/3600
        records.append({
            "uid": uid, "name": name[:14], "balance": d.get("balance",0),
            "earned": d.get("total_earned",0), "spent": d.get("total_spent",0),
            "wins": d.get("casino_wins",0), "losses": d.get("casino_losses",0),
            "won": d.get("casino_won",0), "lost": d.get("casino_lost",0),
            "msgs": u_stat.get("messages",0), "voice_h": voice_h,
            "inc_roles": len(d.get("income_roles",[])), "cos_roles": len(d.get("cosmetic_roles",[])),
        })

    if not records:
        fig, ax = plt.subplots(facecolor=_BG)
        ax.text(0.5, 0.5, "Нет данных", ha="center", va="center", color=_TEXT, fontsize=16)
        ax.axis("off"); ax.set_facecolor(_BG)
        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=100, facecolor=_BG)
        plt.close(); buf.seek(0); return buf

    records.sort(key=lambda x: x["balance"], reverse=True); top10 = records[:10]
    fig = plt.figure(figsize=(18, 22), facecolor=_BG, dpi=130)
    gs  = fig.add_gridspec(5, 3, top=0.94, bottom=0.03, left=0.05, right=0.97,
                           hspace=0.65, wspace=0.38, height_ratios=[0.08,1,1,1,0.9])

    ax_t = fig.add_subplot(gs[0,:]); ax_t.set_facecolor(_BG); ax_t.axis("off")
    ax_t.text(0.5, 0.75, "  CodeParis  —  Аналитика экономики",
              ha="center", va="center", fontsize=22, fontweight="bold",
              color=_TEXT, transform=ax_t.transAxes)
    ts = datetime.now().strftime("%d.%m.%Y  %H:%M")
    ax_t.text(0.5, -0.25, f"Полный анализ  •  {ts}  •  {len(records)} участников",
              ha="center", va="center", fontsize=10, color=_DIM, transform=ax_t.transAxes)
    ax_t.axhline(0.0, xmin=0.04, xmax=0.96, color=_BORDER, lw=1)

    def styled_ax(ax):
        ax.set_facecolor(_CARD)
        for sp in ax.spines.values(): sp.set_edgecolor(_BORDER); sp.set_lw(1)
        ax.tick_params(colors=_DIM, labelsize=8, length=0); ax.set_axisbelow(True)

    def hbar(ax, data_pairs, title, color_pal="purple", fmt_fn=None):
        styled_ax(ax)
        if not data_pairs:
            ax.text(0.5, 0.5, "Нет данных", ha="center", va="center",
                    color=_DIM, transform=ax.transAxes); return
        names = [d[0] for d in data_pairs][::-1]; vals = [d[1] for d in data_pairs][::-1]
        n = len(vals); y = np.arange(n)
        pal = [_GOLD if i==n-1 else _SIL if i==n-2 else _BRZ if i==n-3
               else _PUR if color_pal=="purple" else _BLUE for i in range(n)]
        ax.barh(y, vals, color=pal, height=0.65, zorder=3)
        ax.xaxis.grid(True, color=_BORDER, ls="--", alpha=0.3, lw=0.6)
        for i, v in enumerate(vals):
            lbl = fmt_fn(v) if fmt_fn else f"{v:,.0f}"
            ax.text(v+max(vals)*0.01, i, lbl, va="center", fontsize=7.5, color=_TEXT, fontweight="bold")
        ax.set_yticks(y); ax.set_yticklabels(names, fontsize=8, color=_TEXT)
        ax.set_xlim(0, max(vals)*1.28 if vals else 1); ax.set_ylim(-0.6, n-0.4)
        ax.set_title(title, color=_TEXT, fontsize=10, fontweight="bold", pad=8, loc="left")

    top_bal  = [(r["name"], r["balance"])  for r in top10]
    top_earn = sorted(records, key=lambda x: x["earned"], reverse=True)[:8]
    top_spend= sorted(records, key=lambda x: x["spent"],  reverse=True)[:8]

    hbar(fig.add_subplot(gs[1,0]), top_bal,   "  💰 Топ по балансу",   "purple", lambda v: f"{v:,.0f}")
    hbar(fig.add_subplot(gs[1,1]), [(r["name"],r["earned"]) for r in top_earn], "  📈 Топ по заработку","blue", lambda v: f"{v:,.0f}")
    hbar(fig.add_subplot(gs[1,2]), [(r["name"],r["spent"])  for r in top_spend],"  🛒 Топ по тратам",  "purple",lambda v: f"{v:,.0f}")

    top_caswins = sorted(records, key=lambda x: x["wins"], reverse=True)[:8]
    top_caswon  = sorted(records, key=lambda x: x["won"],  reverse=True)[:8]
    hbar(fig.add_subplot(gs[2,0]), [(r["name"],r["wins"]) for r in top_caswins],"  🏆 Казино — побед","blue", lambda v: f"{int(v)}")
    hbar(fig.add_subplot(gs[2,1]), [(r["name"],r["won"])  for r in top_caswon], "  💸 Казино — выиграно","purple",lambda v: f"{v:,.0f}")

    ax_sc = fig.add_subplot(gs[2,2]); styled_ax(ax_sc)
    if len(records) >= 2:
        xs = [r["voice_h"] for r in records]; ys = [r["balance"] for r in records]
        sizes = [max(20, r["msgs"]/5) for r in records]
        ax_sc.scatter(xs, ys, s=sizes, alpha=0.75, c=list(range(len(records))), cmap="plasma", zorder=3)
        for r in sorted(records, key=lambda x: x["balance"], reverse=True)[:5]:
            ax_sc.annotate(r["name"], (r["voice_h"], r["balance"]),
                           textcoords="offset points", xytext=(4,4), fontsize=7, color=_TEXT, alpha=0.9)
        ax_sc.xaxis.grid(True, color=_BORDER, ls="--", alpha=0.3, lw=0.6)
        ax_sc.yaxis.grid(True, color=_BORDER, ls="--", alpha=0.3, lw=0.6)
        ax_sc.set_xlabel("Часов в голосе", color=_DIM, fontsize=8)
        ax_sc.set_ylabel("Баланс", color=_DIM, fontsize=8)
    ax_sc.set_title("  🔗 Голос vs Баланс", color=_TEXT, fontsize=9, fontweight="bold", pad=8, loc="left")

    ax_pie = fig.add_subplot(gs[3,0]); ax_pie.set_facecolor(_CARD)
    if records:
        pie_names = [r["name"] for r in top10]; pie_vals = [r["balance"] for r in top10]
        rest_sum = sum(r["balance"] for r in records[10:])
        if rest_sum > 0: pie_names.append("Остальные"); pie_vals.append(rest_sum)
        pie_cols = ROULETTE_COLORS[:len(pie_vals)]
        wedges, texts, autotexts = ax_pie.pie(
            pie_vals, labels=None, autopct="%1.0f%%", colors=pie_cols, startangle=90,
            pctdistance=0.75, wedgeprops={"linewidth":1.5,"edgecolor":_BG})
        for at in autotexts: at.set_color(_TEXT); at.set_fontsize(7)
        ax_pie.legend(wedges, pie_names, loc="lower left", fontsize=6.5, framealpha=0.3,
                      labelcolor=_TEXT, facecolor=_CARD, edgecolor=_BORDER)
    ax_pie.set_title("  🥧 Распределение монет", color=_TEXT, fontsize=10, fontweight="bold", pad=8, loc="left")

    ax_inc = fig.add_subplot(gs[3,1]); styled_ax(ax_inc)
    role_counts = {r["id"]: 0 for r in INCOME_ROLES}
    for rec in records:
        for rid in all_eco.get(str(rec["uid"]),{}).get("income_roles",[]):
            if rid in role_counts: role_counts[rid] += 1
    rc_items = [(INCOME_ROLES[i]["name"], role_counts[r["id"]]) for i,r in enumerate(INCOME_ROLES) if role_counts[r["id"]] > 0]
    if rc_items:
        names_r=[x[0] for x in rc_items]; vals_r=[x[1] for x in rc_items]; y_r=np.arange(len(vals_r))
        cols_r=[ROULETTE_COLORS[i%len(ROULETTE_COLORS)] for i in range(len(vals_r))]
        ax_inc.barh(y_r, vals_r, color=cols_r, height=0.6, zorder=3)
        ax_inc.xaxis.grid(True, color=_BORDER, ls="--", alpha=0.3, lw=0.6)
        for i,v in enumerate(vals_r): ax_inc.text(v+0.05, i, str(v), va="center", fontsize=8, color=_TEXT)
        ax_inc.set_yticks(y_r); ax_inc.set_yticklabels(names_r, fontsize=7.5, color=_TEXT)
        ax_inc.set_xlim(0, max(vals_r)*1.4 if vals_r else 1); ax_inc.set_ylim(-0.6, len(vals_r)-0.4)
    ax_inc.set_title("  💼 Популярность ролей", color=_TEXT, fontsize=10, fontweight="bold", pad=8, loc="left")

    ax_wr = fig.add_subplot(gs[3,2]); styled_ax(ax_wr)
    wr_data = [(r["name"], r["wins"]/(r["wins"]+r["losses"])*100 if (r["wins"]+r["losses"])>0 else 0,
                r["wins"]+r["losses"]) for r in records if (r["wins"]+r["losses"])>=2]
    wr_data.sort(key=lambda x: x[1], reverse=True); wr_data = wr_data[:8]
    if wr_data:
        names_w=[d[0] for d in wr_data][::-1]; vals_w=[d[1] for d in wr_data][::-1]; games_w=[d[2] for d in wr_data][::-1]
        y_w=np.arange(len(vals_w)); cols_w=[(0.16,0.73,0.51) if v>=50 else (0.94,0.27,0.27) for v in vals_w]
        ax_wr.barh(y_w, vals_w, color=cols_w, height=0.6, zorder=3)
        ax_wr.axvline(50, color=_GOLD, ls="--", lw=1.5, alpha=0.7, zorder=4)
        ax_wr.xaxis.grid(True, color=_BORDER, ls="--", alpha=0.3, lw=0.6)
        for i,(v,g) in enumerate(zip(vals_w, games_w)):
            ax_wr.text(v+1, i, f"{v:.0f}% ({g}игр)", va="center", fontsize=7.5, color=_TEXT)
        ax_wr.set_yticks(y_w); ax_wr.set_yticklabels(names_w, fontsize=8, color=_TEXT); ax_wr.set_xlim(0,115)
    ax_wr.set_title("  🎰 Винрейт казино", color=_TEXT, fontsize=10, fontweight="bold", pad=8, loc="left")

    ax_tbl = fig.add_subplot(gs[4,:]); ax_tbl.set_facecolor(_CARD)
    for sp in ax_tbl.spines.values(): sp.set_edgecolor(_BORDER)
    ax_tbl.axis("off")
    ax_tbl.set_title("  📋 Сводная таблица — Топ 10", color=_TEXT, fontsize=10, fontweight="bold", pad=8, loc="left")
    total_coins=sum(r["balance"] for r in records); total_earn=sum(r["earned"] for r in records)
    total_spent=sum(r["spent"] for r in records); total_games=sum(r["wins"]+r["losses"] for r in records)
    avg_bal = total_coins/len(records) if records else 0
    col_labels=["#","Участник","Баланс","Заработано","Потрачено","W/L казино","Голос","Сообщ.","Роли"]
    table_data=[]
    for i,r in enumerate(top10,1):
        wl = f"{r['wins']}/{r['losses']}" if (r["wins"]+r["losses"]) else "—"
        table_data.append([str(i),r["name"],f"{r['balance']:,}",f"{r['earned']:,}",f"{r['spent']:,}",
                           wl,f"{r['voice_h']:.1f}ч",str(r["msgs"]),str(r["inc_roles"])])
    table = ax_tbl.table(cellText=table_data, colLabels=col_labels, cellLoc="center", loc="center", bbox=[0,0.0,1,1.0])
    table.auto_set_font_size(False); table.set_fontsize(8)
    for (row,col),cell in table.get_celld().items():
        cell.set_facecolor(_CARD if row%2==0 else "#1a1a35")
        cell.set_text_props(color=_GOLD if row==0 else _TEXT); cell.set_edgecolor(_BORDER)

    stats_line=(f"Монет в обороте: {total_coins:,}  •  Выдано: {total_earn:,}  •  "
                f"Потрачено: {total_spent:,}  •  Игр: {total_games}  •  Средний баланс: {avg_bal:,.0f}")
    fig.text(0.5, 0.012, stats_line, ha="center", fontsize=8, color=_DIM)
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=130, bbox_inches="tight", facecolor=_BG, edgecolor="none")
    plt.close(fig); buf.seek(0); return buf

# ══════════════════════════════════════════════════════════════════════════════
#  🧠  GROQ AI
# ══════════════════════════════════════════════════════════════════════════════

VEMBY_SYSTEM = f"""Ты — AI-ассистент Discord-сервера CodeParis по имени Vemby.
Общаешься на русском, живо, дружелюбно, с лёгким юмором.
Используй Discord-форматирование: **жирный**, `код`, > цитата. Эмодзи — умеренно.

━━━ СТРУКТУРА СЕРВЕРА CODEPARIS ━━━
📋 INFO     — #welcome, #rules, #news, #status, #ticket
💬 COMMUNITY — #chat, #media, #flood, #memes, #social
🎮 GAME     — #help, #casino, #shop, #top, #work
💡 IDEA     — #ideas, #votes, #bugs, #feed
🔊 VOICE    — create, chill, stream, music, voice
🤖 AI       — #ai-vemby, #help-ai
🔐 ВХОД    — #verif (кнопка верификации)

━━━ КОМАНДЫ ДЛЯ УЧАСТНИКОВ ━━━
{PUBLIC_COMMANDS}

━━━ ВАЖНО — СЕКРЕТНЫЕ КОМАНДЫ ━━━
{ADMIN_COMMANDS_HINT}
"""

class AIEngine:
    GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
    MODEL    = "llama-3.3-70b-versatile"

    def __init__(self):
        self.history: dict[int, list] = {}

    async def _call(self, messages: list, max_tokens: int = 600, temp: float = 0.75) -> str:
        if not GROQ_API_KEY:
            return "⚠️ GROQ_API_KEY не задан в переменных среды."
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        payload = {"model": self.MODEL, "messages": messages, "max_tokens": max_tokens, "temperature": temp}
        try:
            async with aiohttp.ClientSession() as s:
                async with s.post(self.GROQ_URL, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as r:
                    if r.status == 200:
                        data = await r.json()
                        return data["choices"][0]["message"]["content"]
                    return f"⚠️ Ошибка API ({r.status})"
        except asyncio.TimeoutError:
            return "⚠️ Groq AI не ответил вовремя, попробуй ещё раз."
        except Exception as e:
            return f"⚠️ {str(e)[:80]}"

    async def get_response(self, user_id: int, message: str) -> str:
        self.history.setdefault(user_id, [])
        self.history[user_id].append({"role": "user", "content": message})
        self.history[user_id] = self.history[user_id][-12:]
        msgs = [{"role": "system", "content": VEMBY_SYSTEM}] + self.history[user_id]
        reply = await self._call(msgs)
        self.history[user_id].append({"role": "assistant", "content": reply})
        return reply

    async def generate_news(self, topic: str) -> str:
        prompt = (f"Напиши интересную короткую новость (3-5 абзацев) для Discord-сервера CodeParis "
                  f"на тему: {topic}. Стиль: живой, дружелюбный, с эмодзи. "
                  f"Используй Discord-форматирование. Не пиши заголовок — только текст новости.")
        msgs = [{"role":"system","content":VEMBY_SYSTEM},{"role":"user","content":prompt}]
        return await self._call(msgs, max_tokens=500, temp=0.85)

    async def generate_update_news(self, update: dict) -> str:
        changes_text = "\n".join(update["changes"])
        prompt = (f"Напиши захватывающий анонс обновления {update['version']} для Discord-сервера CodeParis.\n"
                  f"Название: {update['title']}\nЧто добавили:\n{changes_text}\n"
                  f"Как работает: {update['how']}\n\nСтиль: живой, с эмодзи, 3-4 абзаца. Пиши от лица Vemby.")
        msgs = [{"role":"system","content":VEMBY_SYSTEM},{"role":"user","content":prompt}]
        return await self._call(msgs, max_tokens=600, temp=0.80)

    def clear(self, uid): self.history.pop(uid, None)
    def clear_all(self): self.history.clear()

ai = AIEngine()

# ══════════════════════════════════════════════════════════════════════════════
#  💰  ЭКОНОМИКА
# ══════════════════════════════════════════════════════════════════════════════

class Economy:
    # ✅ FIX: DATA_DIR для Railway — используем /tmp если нет прав на запись в текущую папку
    DATA_DIR = os.getenv("DATA_DIR", ".")
    FILE = os.path.join(DATA_DIR, "economy.json")

    def __init__(self):
        self._data: dict[str, dict] = {}
        self._load()

    def _load(self):
        try:
            if os.path.exists(self.FILE):
                with open(self.FILE, encoding="utf-8") as f:
                    self._data = json.load(f)
        except Exception as e:
            print(f"⚠️ Economy load error: {e}")
            self._data = {}

    def save(self):
        try:
            os.makedirs(os.path.dirname(self.FILE) if os.path.dirname(self.FILE) else ".", exist_ok=True)
            with open(self.FILE, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ Economy save error: {e}")

    def _get(self, uid: int) -> dict:
        k = str(uid)
        if k not in self._data:
            self._data[k] = {
                "balance": START_BALANCE, "income_roles": [], "cosmetic_roles": [],
                "last_work": 0, "last_free_job": {}, "total_earned": START_BALANCE,
                "total_spent": 0, "casino_wins": 0, "casino_losses": 0,
                "casino_won": 0, "casino_lost": 0, "username": "Unknown",
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
    def has_income_role(self, uid: int, role_id: str) -> bool: return role_id in self._get(uid)["income_roles"]
    def buy_income_role(self, uid: int, role_id: str, price: int) -> bool:
        d = self._get(uid)
        if d["balance"] < price or role_id in d["income_roles"]: return False
        d["balance"] -= price; d["total_spent"] += price; d["income_roles"].append(role_id)
        self.save(); return True
    def get_income_roles(self, uid: int) -> list: return self._get(uid).get("income_roles", [])
    def has_cosmetic_role(self, uid: int, role_id: int) -> bool: return role_id in self._get(uid).get("cosmetic_roles", [])
    def buy_cosmetic_role(self, uid: int, role_id: int, price: int) -> bool:
        d = self._get(uid)
        if d["balance"] < price or role_id in d.get("cosmetic_roles", []): return False
        d["balance"] -= price; d["total_spent"] += price
        d.setdefault("cosmetic_roles", []).append(role_id); self.save(); return True
    def get_cosmetic_roles(self, uid: int) -> list: return self._get(uid).get("cosmetic_roles", [])
    def can_work(self, uid: int) -> tuple:
        d = self._get(uid); elapsed = time.time()-d.get("last_work",0)
        if elapsed < WORK_COOLDOWN: return False, WORK_COOLDOWN-elapsed
        return True, 0.0
    def do_work(self, uid: int) -> int:
        d = self._get(uid); owned = d.get("income_roles", [])
        if not owned: return 0
        total = 0
        for rid in owned:
            role = next((r for r in INCOME_ROLES if r["id"]==rid), None)
            if role:
                pct = random.uniform(0.01, 0.05); earned = int(role["price"]*pct); total += earned
        d["balance"] += total; d["total_earned"] += total; d["last_work"] = time.time()
        self.save(); return total
    def can_free_job(self, uid: int, job_id: str) -> tuple:
        d = self._get(uid); last = d.get("last_free_job",{}).get(job_id,0)
        job = next((j for j in FREE_JOBS if j["id"]==job_id), None)
        if not job: return False, 0
        elapsed = time.time()-last
        if elapsed < job["cd"]: return False, job["cd"]-elapsed
        return True, 0.0
    def do_free_job(self, uid: int, job_id: str) -> int:
        job = next((j for j in FREE_JOBS if j["id"]==job_id), None)
        if not job: return 0
        d = self._get(uid); earn = random.randint(job["min"], job["max"])
        d["balance"] += earn; d["total_earned"] += earn
        d.setdefault("last_free_job",{})[job_id] = time.time(); self.save(); return earn
    def set_username(self, uid: int, name: str):
        d = self._get(uid); d["username"] = name; self.save()
    def casino_win(self, uid: int, amount: int):
        d = self._get(uid); d["balance"] += amount; d["total_earned"] += amount
        d["casino_wins"] += 1; d["casino_won"] += amount; self.save()
    def casino_lose(self, uid: int, amount: int):
        d = self._get(uid); d["casino_losses"] += 1; d["casino_lost"] += amount; self.save()
    def get_top(self, n: int = 10) -> list:
        result = [(int(uid), d.get("balance",0)) for uid,d in self._data.items()]
        return sorted(result, key=lambda x: x[1], reverse=True)[:n]
    def get_user_data(self, uid: int) -> dict: return dict(self._get(uid))
    def reset_user(self, uid: int):
        k = str(uid)
        if k in self._data: del self._data[k]; self.save()
    def reset_all(self): self._data.clear(); self.save()

eco = Economy()

# ══════════════════════════════════════════════════════════════════════════════
#  🎡  РУЛЕТКА — СОСТОЯНИЕ ИГРЫ
# ══════════════════════════════════════════════════════════════════════════════

class RouletteGame:
    def __init__(self):
        self.active = False; self.players: dict[int,dict] = {}
        self.message = None; self.start_t = 0.0; self.game_num = 0; self._color_idx = 0

    def next_color(self) -> str:
        c = ROULETTE_COLORS[self._color_idx % len(ROULETTE_COLORS)]; self._color_idx += 1; return c

    def add_player(self, uid: int, name: str, bet: int):
        self.players[uid] = {"name": name, "bet": bet, "color": self.next_color()}

    def total_pot(self) -> int: return sum(p["bet"] for p in self.players.values())

    def spin(self) -> tuple:
        total = self.total_pot()
        if not total or not self.players: return None, None
        r = random.randint(1, total); cumsum = 0
        for uid, data in self.players.items():
            cumsum += data["bet"]
            if r <= cumsum: return uid, data
        uid = list(self.players.keys())[-1]
        return uid, self.players[uid]

    def reset(self):
        self.active = False; self.players = {}; self.message = None; self._color_idx = 0

roulette = RouletteGame()

# ══════════════════════════════════════════════════════════════════════════════
#  📊  СТАТИСТИКА ПОЛЬЗОВАТЕЛЕЙ
# ══════════════════════════════════════════════════════════════════════════════

class UserStats:
    DATA_DIR = os.getenv("DATA_DIR", ".")
    FILE = os.path.join(DATA_DIR, "user_stats.json")

    def __init__(self):
        self._data: dict[str,dict] = {}; self._load()

    def _load(self):
        try:
            if os.path.exists(self.FILE):
                with open(self.FILE, encoding="utf-8") as f:
                    self._data = json.load(f)
        except Exception as e:
            print(f"⚠️ UserStats load error: {e}"); self._data = {}

    def save(self):
        try:
            os.makedirs(os.path.dirname(self.FILE) if os.path.dirname(self.FILE) else ".", exist_ok=True)
            with open(self.FILE, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ UserStats save error: {e}")

    def _get(self, uid: int) -> dict:
        k = str(uid)
        if k not in self._data:
            self._data[k] = {"messages":0,"voice_time":0,"voice_join":None,"last_seen":None,"roles_given":[],"username":"Unknown"}
        return self._data[k]

    def add_message(self, user: discord.Member):
        d = self._get(user.id); d["messages"] += 1; d["last_seen"] = datetime.now().isoformat()
        d["username"] = user.display_name; self.save()

    def voice_join(self, user: discord.Member):
        d = self._get(user.id); d["voice_join"] = time.time(); d["username"] = user.display_name; self.save()

    def voice_leave(self, user: discord.Member) -> float:
        d = self._get(user.id)
        if d["voice_join"] is None: return 0.0
        elapsed = time.time()-d["voice_join"]; d["voice_time"] += elapsed; d["voice_join"] = None
        d["last_seen"] = datetime.now().isoformat(); d["username"] = user.display_name; self.save(); return elapsed

    def get_voice_hours(self, uid: int) -> float:
        d = self._get(uid); sec = d["voice_time"]
        if d["voice_join"]: sec += time.time()-d["voice_join"]
        return sec/3600

    def add_role_given(self, uid: int, rid: int):
        d = self._get(uid)
        if rid not in d["roles_given"]: d["roles_given"].append(rid); self.save()

    def has_role_given(self, uid: int, rid: int) -> bool: return rid in self._get(uid).get("roles_given",[])

    def get_all(self) -> list:
        result = []
        for uid, d in self._data.items():
            try:
                sec = d.get("voice_time",0)
                if d.get("voice_join"): sec += time.time()-d["voice_join"]
                result.append({"user_id":int(uid),"username":d.get("username","?"),
                                "messages":d.get("messages",0),"voice_sec":sec})
            except Exception: pass
        return result

    def get_user_data(self, uid: int) -> dict:
        d = self._get(uid); sec = d.get("voice_time",0)
        if d.get("voice_join"): sec += time.time()-d["voice_join"]
        return {"messages":d.get("messages",0),"voice_sec":sec,"voice_join":d.get("voice_join"),
                "username":d.get("username","?"),"last_seen":d.get("last_seen")}

ust = UserStats()

# ══════════════════════════════════════════════════════════════════════════════
#  💾  СОСТОЯНИЕ
# ══════════════════════════════════════════════════════════════════════════════

class State:
    DATA_DIR = os.getenv("DATA_DIR", ".")
    FILE = os.path.join(DATA_DIR, "state.json")

    def __init__(self):
        self.ai_mode=False; self.verify_msg=None; self.ticket_msg=None
        self.stats_msg=None; self.shop_msg=None; self.autonews_on=True
        self.news_hours=6; self.news_counter=0
        self.stats={"ai_responses":0,"admin_forwards":0,"verified":0,"tickets":0,"start":datetime.now().isoformat()}
        self._load()

    def _load(self):
        try:
            if os.path.exists(self.FILE):
                d = json.load(open(self.FILE, encoding="utf-8"))
                self.ai_mode=d.get("ai_mode",False); self.verify_msg=d.get("verify_msg")
                self.ticket_msg=d.get("ticket_msg"); self.stats_msg=d.get("stats_msg")
                self.shop_msg=d.get("shop_msg"); self.autonews_on=d.get("autonews_on",True)
                self.news_hours=d.get("news_hours",6); self.news_counter=d.get("news_counter",0)
                self.stats=d.get("stats",self.stats)
        except Exception: pass

    def save(self):
        try:
            json.dump({"ai_mode":self.ai_mode,"verify_msg":self.verify_msg,"ticket_msg":self.ticket_msg,
                       "stats_msg":self.stats_msg,"shop_msg":self.shop_msg,"autonews_on":self.autonews_on,
                       "news_hours":self.news_hours,"news_counter":self.news_counter,"stats":self.stats},
                      open(self.FILE,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
        except Exception as e: print(f"⚠️ State save: {e}")

    def set(self, v: bool): self.ai_mode = v; self.save()

st = State()

# ══════════════════════════════════════════════════════════════════════════════
#  🛠️  УТИЛИТЫ
# ══════════════════════════════════════════════════════════════════════════════

def emb(title="", desc="", color=C["ai"], footer=None, image=None) -> discord.Embed:
    e = discord.Embed(title=title, description=desc, color=color, timestamp=datetime.now())
    if footer: e.set_footer(text=footer)
    if image: e.set_image(url=image)
    return e

def ai_embed(text: str) -> discord.Embed:
    return emb(desc=text, color=C["ai"], footer="✦ Vemby  •  AI-ассистент CodeParis")

async def _delete_after(msg: discord.Message, delay: int):
    await asyncio.sleep(delay)
    try: await msg.delete()
    except Exception: pass

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

def _leaderboard_data(guild):
    all_u = ust.get_all()
    if not all_u: return [], []
    if guild:
        for u in all_u:
            m = guild.get_member(u["user_id"])
            if m: u["username"] = m.display_name
    bv = sorted([u for u in all_u if u["voice_sec"]>=60], key=lambda u: u["voice_sec"], reverse=True)[:10]
    bm = sorted([u for u in all_u if u["messages"]>=1], key=lambda u: u["messages"], reverse=True)[:10]
    return [(u["username"],u["voice_sec"]/3600) for u in bv], [(u["username"],u["messages"]) for u in bm]

# ══════════════════════════════════════════════════════════════════════════════
#  📰  НОВОСТИ
# ══════════════════════════════════════════════════════════════════════════════

async def post_auto_news():
    ch = bot.get_channel(NEWS_CHANNEL_ID)
    if not ch: return
    topic = random.choice(NEWS_TOPICS); text = await ai.generate_news(topic)
    if not text: return
    st.news_counter += 1; st.save()
    e = discord.Embed(color=C["news"], timestamp=datetime.now())
    e.title = f"📰  Новости CodeParis  #{st.news_counter}"
    e.description = text; e.set_footer(text="✦ Vemby  •  Авто-новости CodeParis")
    await ch.send(embed=e)

async def post_update_report(update: dict):
    ch = bot.get_channel(NEWS_CHANNEL_ID)
    if not ch: return
    ai_text = await ai.generate_update_news(update)
    e = discord.Embed(color=C["update"], timestamp=datetime.now())
    e.title = f"{update['emoji']}  Обновление {update['version']} — {update['title']}"
    e.description = ("```\n▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔\n```\n" + ai_text +
                     "\n```\n▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔\n```")
    e.add_field(name="📋  Список изменений", value="\n".join(update["changes"]), inline=False)
    e.add_field(name="⚙️  Как это работает", value=update["how"], inline=False)
    e.set_footer(text=f"✦ CodeParis  •  Обновление {update['version']}  •  {update['date']}")
    await ch.send(embed=e)
    update["posted"] = True

async def check_and_post_updates():
    for update in SERVER_CHANGELOG:
        if not update.get("posted", False):
            await post_update_report(update); await asyncio.sleep(2)

# ══════════════════════════════════════════════════════════════════════════════
#  🏆  ЛИДЕРБОРД / ЭМБЕДЫ
# ══════════════════════════════════════════════════════════════════════════════

def make_leaderboard_embed(guild=None, vd=None, md=None) -> discord.Embed:
    if vd is None or md is None: vd, md = _leaderboard_data(guild)
    e = discord.Embed(color=C["gold"], timestamp=datetime.now())
    e.title = "🏆  Топ активных — CodeParis"
    if not vd and not md:
        e.description = "Пока нет данных. Общайтесь и заходите в голосовые каналы!"
        e.set_footer(text="✦ CodeParis  •  Статистика активности"); return e
    if vd:
        e.add_field(name="🎙️  Голосовые каналы",
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
    rows = sorted({(h,rid) for h,rid,_ in VOICE_ROLES}, key=lambda x: x[0])
    e.add_field(name="🎭  Авто-роли",
                value="\n".join(f"⏱️ `{h}ч` → <@&{rid}>" for h,rid in rows) or "—", inline=False)
    e.set_footer(text="✦ CodeParis  •  Обновляется каждые 10 минут"); return e

def make_personal_stats_embed(member: discord.Member) -> discord.Embed:
    d = ust.get_user_data(member.id); vh = d["voice_sec"]/3600; next_txt = None
    for h,rid,_ in sorted(VOICE_ROLES, key=lambda x: x[0]):
        if vh < h: next_txt = f"До <@&{rid}> → `{fmt_time_short((h-vh)*3600)}`"; break
    max_h = max(h for h,_,_ in VOICE_ROLES) if VOICE_ROLES else 111
    pct = min(vh/max_h,1.0); bar = "█"*int(pct*10)+"░"*(10-int(pct*10))
    e = discord.Embed(color=C["info"], timestamp=datetime.now())
    e.title = f"📊  Статистика · {member.display_name}"
    e.set_thumbnail(url=member.display_avatar.url)
    e.add_field(name="💬  Сообщений", value=f"`{d['messages']:,}`", inline=True)
    e.add_field(name="🎙️  Голос",     value=f"`{fmt_time(d['voice_sec'])}`", inline=True)
    e.add_field(name="📡  В эфире",   value="🟢 Да" if d["voice_join"] else "⚫ Нет", inline=True)
    e.add_field(name=f"📈  Прогресс ({vh:.1f}ч / {max_h}ч)", value=f"`[{bar}]` {pct*100:.0f}%", inline=False)
    if next_txt: e.add_field(name="🎯  Следующая награда", value=next_txt, inline=False)
    if d["last_seen"]:
        try:
            ts = int(datetime.fromisoformat(d["last_seen"]).timestamp())
            e.add_field(name="🕐  Был активен", value=f"<t:{ts}:R>", inline=False)
        except: pass
    e.set_footer(text="✦ CodeParis  •  Личная статистика"); return e

def make_shop_embed() -> discord.Embed:
    e = discord.Embed(title="🏪  Магазин CodeParis", color=C["shop"], timestamp=datetime.now())
    e.description = (f"Трать монеты {COIN} с умом!\n"
                     f"**Доходные роли** → зарабатывай командой `!работать` каждые 3 мин\n"
                     f"**Косметика** → носи Discord-роль и снимай её через `!профиль`")
    lines = []
    for r in INCOME_ROLES:
        lo=int(r["price"]*0.01); hi=int(r["price"]*0.05)
        lines.append(f"{r['emoji']} **{r['name']}**\n  💰 Цена: `{r['price']:,}` {COIN}  •  Доход: `{lo:,}`–`{hi:,}` {COIN}/работу")
    e.add_field(name="💼  Доходные роли", value="\n".join(lines), inline=False)
    clines = []
    for r in COSMETIC_ROLES:
        clines.append(f"<@&{r['discord_role']}> {r['name']}\n  💰 Цена: `{r['price']:,}` {COIN}  •  Надеть/снять в `!профиль`")
    e.add_field(name="🎭  Косметические роли", value="\n".join(clines), inline=False)
    e.add_field(name="📖  Как купить?",
                value="`!купить <название>` — купить роль\n`!баланс` — проверить монеты\n`!работать` — заработать\n`!профиль` — косметика",
                inline=False)
    e.set_footer(text="✦ CodeParis  •  Магазин  •  Удачных покупок!"); return e

def make_profile_embed(member: discord.Member) -> discord.Embed:
    d = eco.get_user_data(member.id)
    e = discord.Embed(title=f"👤  Профиль — {member.display_name}", color=C["info"], timestamp=datetime.now())
    e.set_thumbnail(url=member.display_avatar.url)
    e.add_field(name=f"💰  Баланс",    value=f"`{d['balance']:,}` {COIN}", inline=True)
    e.add_field(name="💹  Заработано", value=f"`{d['total_earned']:,}` {COIN}", inline=True)
    e.add_field(name="🛒  Потрачено",  value=f"`{d['total_spent']:,}` {COIN}", inline=True)
    owned_inc = d.get("income_roles",[])
    if owned_inc:
        inc_lines = []
        for r in INCOME_ROLES:
            if r["id"] in owned_inc:
                lo=int(r["price"]*0.01); hi=int(r["price"]*0.05)
                inc_lines.append(f"{r['emoji']} **{r['name']}** — `{lo:,}`–`{hi:,}` {COIN}/работу")
        e.add_field(name="💼  Доходные роли", value="\n".join(inc_lines), inline=False)
    else:
        e.add_field(name="💼  Доходные роли", value="Нет. Купи в `!магазин`!", inline=False)
    owned_cos = d.get("cosmetic_roles",[])
    if owned_cos:
        cos_lines = []
        for r in COSMETIC_ROLES:
            if r["discord_role"] in owned_cos:
                has = member.get_role(r["discord_role"]) is not None
                status = "🟢 Надета" if has else "⚫ Снята"
                cos_lines.append(f"<@&{r['discord_role']}> {r['name']} — {status}")
        e.add_field(name="🎭  Косметические роли", value="\n".join(cos_lines), inline=False)
    wins=d.get("casino_wins",0); losses=d.get("casino_losses",0)
    if wins or losses:
        total_g=wins+losses; wr=f"{wins/total_g*100:.0f}%" if total_g else "—"
        e.add_field(name="🎰  Казино",
                    value=(f"🏆 Побед: `{wins}` | Поражений: `{losses}`\nВинрейт: `{wr}` | "
                           f"Выиграно: `{d.get('casino_won',0):,}` {COIN} | Проиграно: `{d.get('casino_lost',0):,}` {COIN}"),
                    inline=False)
    can, remaining = eco.can_work(member.id)
    if can: e.add_field(name="💼  Работа", value="✅ Можно работать прямо сейчас!", inline=False)
    else:
        m2,s2=divmod(int(remaining),60); e.add_field(name="💼  Работа", value=f"⏳ Следующая работа через `{m2}м {s2:02d}с`", inline=False)
    e.set_footer(text="✦ CodeParis  •  Профиль"); return e

def make_roulette_embed(players: dict, timer: int=None, winner_uid: int=None,
                         game_num: int=1, finished: bool=False) -> discord.Embed:
    total = sum(p["bet"] for p in players.values()) if players else 0
    color = C["gold"] if finished else C["roulette"]
    e = discord.Embed(color=color, timestamp=datetime.now())
    if finished and winner_uid is not None:
        w = players.get(winner_uid)
        if w:
            e.title=f"🎡  Рулетка #{game_num}  •  Результат!"
            e.description=(f"**🏆 Победитель: {w['name']}**\n\n"
                           f"```\nСтавка: {w['bet']:,} {COIN}\nБанк:   {total:,} {COIN}\nШанс:   {w['bet']/total*100:.1f}%\n```")
    else:
        e.title=f"🎡  Рулетка  •  Игра #{game_num}"
        if players:
            if timer is not None:
                m2,s2=divmod(timer,60)
                e.description=(f"⏱️ До розыгрыша: `{m2:02d}:{s2:02d}`\n💰 Банк: `{total:,}` {COIN}\n👥 Участников: `{len(players)}`")
            else:
                e.description=f"Ставки принимаются!\n💰 Банк: `{total:,}` {COIN}"
        else:
            e.description="Ожидание участников...\nПиши `!рулетка <ставка>` чтобы войти!"
    if players:
        lines=[]
        for uid,p in players.items():
            pct=p["bet"]/total*100 if total else 0
            flag="🏆 " if (finished and uid==winner_uid) else ""
            lines.append(f"{flag}**{p['name']}** — `{p['bet']:,}` {COIN} (`{pct:.1f}%`)")
        e.add_field(name="📋 Ставки", value="\n".join(lines), inline=False)
    e.set_footer(text=f"✦ CodeParis  •  Казино  •  Игра #{game_num}"); return e

# ══════════════════════════════════════════════════════════════════════════════
#  🛠️  ПАНЕЛЬНЫЕ ЭМБЕДЫ
# ══════════════════════════════════════════════════════════════════════════════

def make_verify_embed():
    e = discord.Embed(color=C["verify"], timestamp=datetime.now())
    e.title = "✦  Добро пожаловать на CodeParis"
    e.description = ("```\n▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔\n```\n"
                     "Мы рады видеть тебя здесь **♡**\n\nНажми **Подтвердить вход** — и все каналы открыты.\n\n"
                     "```\n  🔒  Зачем верификация?\n\n  Мы защищаем сообщество от спам-ботов.\n  Один клик — и все каналы открыты.\n```\n"
                     "```\n▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔\n```")
    e.add_field(name="📋  Что тебя ждёт?",
                value="› 💬 Общение\n› 🎮 Игровая система\n› 🔊 Голосовые каналы\n› 🤖 AI Vemby\n› 🎰 Казино", inline=True)
    e.add_field(name="⚡  Проблема?", value="Нажми **Ошибка / Тикет**\nи администрация поможет.", inline=True)
    if VERIFY_BANNER_URL: e.set_image(url=VERIFY_BANNER_URL)
    e.set_footer(text="✦ CodeParis  •  Нажми кнопку чтобы войти"); return e

def make_ticket_embed():
    e = discord.Embed(color=C["ticket"], timestamp=datetime.now())
    e.title = "🎫  Служба поддержки CodeParis"
    e.description = ("```\n▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔\n```\n"
                     "Нажми **Создать тикет** — заполни форму,\nи администрация ответит в личной ветке.\n"
                     "```\n▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔\n```")
    e.add_field(name="⏱️  Время ответа", value="В течение нескольких часов.", inline=True)
    e.add_field(name="📌  Правила",      value="Один тикет — одна проблема.", inline=True)
    e.set_footer(text="✦ CodeParis  •  Поддержка 24/7"); return e

def make_panel_embed():
    s = "🟢  АКТИВЕН" if st.ai_mode else "🔴  ВЫКЛЮЧЕН"
    cl = C["success"] if st.ai_mode else C["error"]
    an = "🟢 ВКЛ" if st.autonews_on else "🔴 ВЫКЛ"
    e = discord.Embed(title="✦  Панель управления · CodeParis", color=cl, timestamp=datetime.now())
    e.description = (f"**Статус ИИ:** {s}\n**Авто-новости:** {an}  (каждые `{st.news_hours}ч`)\n"
                     f"**Новостей опубликовано:** `{st.news_counter}`\n\n"
                     f"```\n  AI ответов        {st.stats['ai_responses']}\n"
                     f"  Пересылок         {st.stats['admin_forwards']}\n"
                     f"  Верифицировано    {st.stats.get('verified',0)}\n"
                     f"  Тикетов           {st.stats.get('tickets',0)}\n```")
    e.set_footer(text="✦ Admin Panel  •  Кнопки работают вечно"); return e

# ══════════════════════════════════════════════════════════════════════════════
#  🎫  ФОРМА ТИКЕТА
# ══════════════════════════════════════════════════════════════════════════════

class TicketModal(Modal, title="📝  Новый тикет — CodeParis"):
    name    = TextInput(label="Твоё имя / никнейм", placeholder="Алекс или Paris#1234", min_length=2, max_length=50, required=True)
    problem = TextInput(label="Описание проблемы", placeholder="Подробно опиши что произошло...",
                        style=discord.TextStyle.paragraph, min_length=10, max_length=1000, required=True)

    async def on_submit(self, interaction: discord.Interaction):
        member=interaction.user; guild=interaction.guild; channel=guild.get_channel(TICKET_CHANNEL_ID)
        if not channel:
            await interaction.response.send_message(embed=emb("❌","Канал тикетов не найден!",C["error"]),ephemeral=True); return
        ticket_num=st.stats.get("tickets",0)+1
        try:
            thread=await channel.create_thread(name=f"ticket-{ticket_num:04d}-{member.display_name}",
                                               type=discord.ChannelType.private_thread,
                                               reason=f"Тикет от {member}", invitable=False)
        except discord.Forbidden:
            await interaction.response.send_message(embed=emb("❌","Боту не хватает прав!",C["error"]),ephemeral=True); return
        await thread.add_user(member)
        if sr:=guild.get_role(STAFF_ROLE_ID):
            for m in sr.members:
                try: await thread.add_user(m); await asyncio.sleep(0.2)
                except Exception: pass
        te=discord.Embed(title=f"🎫  Тикет #{ticket_num:04d}", color=C["ticket"], timestamp=datetime.now())
        te.description=(f"Привет, **{member.display_name}**! 👋\n\nТвой тикет принят.\n> Пиши прямо здесь 📎")
        te.add_field(name="👤  Автор",    value=f"{member.mention}\n`{member.name}`", inline=True)
        te.add_field(name="🪪  Имя",      value=f"`{self.name.value}`",               inline=True)
        te.add_field(name="🕐  Создан",   value=f"<t:{int(datetime.now().timestamp())}:R>", inline=True)
        te.add_field(name="📋  Проблема", value=f"```\n{self.problem.value[:900]}\n```", inline=False)
        te.set_thumbnail(url=member.display_avatar.url)
        te.set_footer(text=f"✦ CodeParis  •  Тикет #{ticket_num:04d}")
        await thread.send(content=f"{member.mention} — тикет открыт!", embed=te,
                          view=TicketCloseView(), allowed_mentions=discord.AllowedMentions(users=True))
        nm=discord.Embed(title="🔔  Новый тикет!", color=C["ticket"], timestamp=datetime.now())
        nm.description=(f"**#{ticket_num:04d}** от {member.mention}\n**Имя:** `{self.name.value}`\n\n"
                        f"**Проблема:**\n>>> {self.problem.value[:400]}\n\n**Ветка:** {thread.mention}")
        nm.set_thumbnail(url=member.display_avatar.url); nm.set_footer(text="✦ Admin  •  Удалится через 2 минуты")
        nmsg=await channel.send(content=f"<@&{STAFF_ROLE_ID}>" if STAFF_ROLE_ID else "@here",
                                embed=nm, allowed_mentions=discord.AllowedMentions(roles=True))
        asyncio.create_task(_delete_after(nmsg,120))
        st.stats["tickets"]=ticket_num; st.save()
        ce=discord.Embed(title="✅  Тикет создан!", color=C["success"], timestamp=datetime.now())
        ce.description=f"**Тикет #{ticket_num:04d}** открыт!\n\nТвоя ветка: {thread.mention}\n> Пиши там 📎"
        await interaction.response.send_message(embed=ce, ephemeral=True)

# ══════════════════════════════════════════════════════════════════════════════
#  🎰  РУЛЕТКА — МОДАЛ И VIEW
# ══════════════════════════════════════════════════════════════════════════════

class JoinRouletteModal(Modal, title="🎰  Присоединиться к рулетке"):
    bet_input = TextInput(label="Твоя ставка (монеты)", placeholder="Минимум 10 монет.",
                          min_length=1, max_length=12, required=True)
    def __init__(self, channel):
        super().__init__(); self.channel = channel

    async def on_submit(self, interaction: discord.Interaction):
        try:
            bet = int(self.bet_input.value.replace(",","").replace(" ","").replace(".",""))
        except ValueError:
            await interaction.response.send_message(embed=emb("Введи целое число монет.","",C["error"]),ephemeral=True); return
        if bet < 10:
            await interaction.response.send_message(embed=emb("Минимальная ставка",f"10 {COIN}",C["error"]),ephemeral=True); return
        uid=interaction.user.id
        if not roulette.active:
            await interaction.response.send_message(embed=emb("Игра завершилась","Жди следующую!",C["info"]),ephemeral=True); return
        if uid in roulette.players:
            await interaction.response.send_message(embed=emb("Уже в игре",f"Твоя ставка: {roulette.players[uid]['bet']:,} {COIN}",C["info"]),ephemeral=True); return
        bal=eco.get_balance(uid)
        if bal < bet:
            await interaction.response.send_message(embed=emb("Недостаточно монет",f"У тебя: {bal:,} {COIN}\nСтавка: {bet:,} {COIN}",C["error"]),ephemeral=True); return
        eco.spend(uid,bet); roulette.add_player(uid,interaction.user.display_name,bet); eco.casino_lose(uid,bet)
        remain=max(0,int(ROULETTE_WAIT-(time.time()-roulette.start_t)))
        loop=asyncio.get_event_loop()
        buf=await loop.run_in_executor(None,generate_roulette_wheel,dict(roulette.players),remain,None,roulette.game_num)
        f=discord.File(fp=buf,filename="roulette.png")
        embed=make_roulette_embed(dict(roulette.players),remain,game_num=roulette.game_num)
        embed.set_image(url="attachment://roulette.png")
        try:
            if roulette.message: await roulette.message.delete()
        except Exception: pass
        roulette.message=await self.channel.send(embed=embed,file=f,view=RouletteView(self.channel))
        await interaction.response.send_message(
            embed=emb("Ставка принята!",f"Ты поставил {bet:,} {COIN}\nБанк: {roulette.total_pot():,} {COIN}",C["success"]),ephemeral=True)

class RouletteView(View):
    def __init__(self, channel):
        super().__init__(timeout=None); self.channel=channel

    @discord.ui.button(label="Присоединиться", style=discord.ButtonStyle.green, emoji="🎰")
    async def join_btn(self, interaction: discord.Interaction, button: Button):
        if not roulette.active:
            await interaction.response.send_message(embed=emb("Игра завершилась","Жди следующую! 🎰",C["info"]),ephemeral=True); return
        if interaction.user.id in roulette.players:
            await interaction.response.send_message(embed=emb("Уже участвуешь",f"Ставка: {roulette.players[interaction.user.id]['bet']:,} {COIN}",C["info"]),ephemeral=True); return
        await interaction.response.send_modal(JoinRouletteModal(self.channel))

    @discord.ui.button(label="Мой баланс", style=discord.ButtonStyle.gray, emoji="💰")
    async def balance_btn(self, interaction: discord.Interaction, button: Button):
        bal=eco.get_balance(interaction.user.id)
        await interaction.response.send_message(embed=emb("Твой баланс",f"{bal:,} {COIN}",C["gold"]),ephemeral=True)

# ══════════════════════════════════════════════════════════════════════════════
#  🎭  ПРОФИЛЬ — КОСМЕТИЧЕСКИЕ РОЛИ
# ══════════════════════════════════════════════════════════════════════════════

class ProfileCosmeticView(View):
    def __init__(self, member: discord.Member):
        super().__init__(timeout=120)
        owned = eco.get_cosmetic_roles(member.id)
        for r in COSMETIC_ROLES:
            if r["discord_role"] in owned:
                role_obj = member.guild.get_role(r["discord_role"])
                has = role_obj in member.roles if role_obj else False
                label = f"Снять {r['name']}" if has else f"Надеть {r['name']}"
                style = discord.ButtonStyle.red if has else discord.ButtonStyle.green
                btn = Button(label=label, style=style, custom_id=f"cos_{r['discord_role']}_{member.id}")
                btn.callback = self._make_callback(r["discord_role"], r["name"])
                self.add_item(btn)

    def _make_callback(self, role_id: int, role_name: str):
        async def callback(interaction: discord.Interaction):
            member=interaction.user; role_obj=interaction.guild.get_role(role_id)
            if not role_obj:
                await interaction.response.send_message(embed=emb("❌","Роль не найдена!",C["error"]),ephemeral=True); return
            if not eco.has_cosmetic_role(member.id,role_id):
                await interaction.response.send_message(embed=emb("❌","У тебя нет этой роли.",C["error"]),ephemeral=True); return
            if role_obj in member.roles:
                await member.remove_roles(role_obj,reason="Снятие косметической роли")
                await interaction.response.send_message(embed=emb("✅",f"Роль **{role_name}** снята!",C["success"]),ephemeral=True)
            else:
                await member.add_roles(role_obj,reason="Надевание косметической роли")
                await interaction.response.send_message(embed=emb("✅",f"Роль **{role_name}** надета! 🎭",C["success"]),ephemeral=True)
        return callback

# ══════════════════════════════════════════════════════════════════════════════
#  🔘  VIEWS
# ══════════════════════════════════════════════════════════════════════════════

class AIMessageView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Очистить историю", style=discord.ButtonStyle.gray, emoji="🗑️", custom_id="v_clear_hist")
    async def clear_btn(self, i: discord.Interaction, b: Button):
        ai.clear(i.user.id)
        await i.response.send_message(embed=emb("✅","История очищена.",C["success"]),ephemeral=True)

class TicketCloseView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Закрыть тикет", style=discord.ButtonStyle.red, emoji="🔒", custom_id="t_close", row=0)
    async def close_btn(self, i: discord.Interaction, b: Button):
        if not i.user.guild_permissions.manage_threads:
            await i.response.send_message(embed=emb("❌","Только стафф.",C["error"]),ephemeral=True); return
        e=discord.Embed(title="🔒  Тикет закрыт",color=C["closed"],timestamp=datetime.now())
        e.description=f"Закрыт **{i.user.display_name}**. Архивируется через минуту."
        await i.response.send_message(embed=e)
        await asyncio.sleep(60)
        try: await i.channel.edit(archived=True,locked=True)
        except Exception: pass
    @discord.ui.button(label="Добавить стафф", style=discord.ButtonStyle.gray, emoji="➕", custom_id="t_add_staff", row=0)
    async def add_staff_btn(self, i: discord.Interaction, b: Button):
        if not i.user.guild_permissions.manage_threads:
            await i.response.send_message(embed=emb("❌","Только стафф.",C["error"]),ephemeral=True); return
        if not (sr:=i.guild.get_role(STAFF_ROLE_ID)):
            await i.response.send_message(embed=emb("❌","Роль не найдена!",C["error"]),ephemeral=True); return
        added=0
        for m in sr.members:
            try: await i.channel.add_user(m); added+=1; await asyncio.sleep(0.2)
            except Exception: pass
        await i.response.send_message(embed=emb("✅",f"Добавлено: **{added}**",C["success"]),ephemeral=True)

class VerificationView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Подтвердить вход", style=discord.ButtonStyle.blurple, emoji="🛡️", custom_id="v_verify", row=0)
    async def verify_btn(self, i: discord.Interaction, b: Button):
        m=i.user; g=i.guild
        ur=g.get_role(UNVERIFIED_ROLE_ID); vr=g.get_role(VERIFIED_ROLE_ID)
        if vr and vr in m.roles:
            await i.response.send_message(embed=emb("✦ Уже верифицирован","Полный доступ уже есть 😉",C["info"]),ephemeral=True); return
        try:
            if ur and ur in m.roles: await m.remove_roles(ur,reason="Верификация")
            if vr: await m.add_roles(vr,reason="Верификация")
        except discord.Forbidden:
            await i.response.send_message(embed=emb("❌","Нажми Ошибка/Тикет!",C["error"]),ephemeral=True); return
        e=discord.Embed(title="✦  Добро пожаловать!",color=C["verify"],timestamp=datetime.now())
        e.description=(f"Привет, **{m.display_name}**! 🎉\n\n"
                       "```\n✅  Верификация пройдена!\n    Все каналы открыты.\n```\n\n"
                       "**С чего начать?**\n› 📋 **#rules** → 💬 **#chat** → 🤖 **#ai-vemby** → 🎰 **#казино**")
        if m.avatar: e.set_thumbnail(url=m.avatar.url)
        e.set_footer(text="✦ CodeParis  •  Рады видеть тебя!")
        await i.response.send_message(embed=e,ephemeral=True)
        st.stats["verified"]+=1; st.save(); eco.get_balance(m.id)
    @discord.ui.button(label="Ошибка / Тикет", style=discord.ButtonStyle.red, emoji="🎫", custom_id="v_ticket_btn", row=0)
    async def ticket_from_verify(self, i: discord.Interaction, b: Button):
        await i.response.send_modal(TicketModal())

class TicketOpenView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Создать тикет", style=discord.ButtonStyle.blurple, emoji="🎫", custom_id="t_open")
    async def open_btn(self, i: discord.Interaction, b: Button):
        await i.response.send_modal(TicketModal())

class AdminPanelView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Включить AI",      style=discord.ButtonStyle.green,   emoji="🟢", custom_id="p_enable",   row=0)
    async def enable(self, i: discord.Interaction, b: Button):
        if not i.user.guild_permissions.administrator:
            await i.response.send_message(embed=emb("❌","Нет прав.",C["error"]),ephemeral=True); return
        st.set(True); await i.response.edit_message(embed=make_panel_embed(),view=self)
    @discord.ui.button(label="Выключить AI",     style=discord.ButtonStyle.red,     emoji="🔴", custom_id="p_disable",  row=0)
    async def disable(self, i: discord.Interaction, b: Button):
        if not i.user.guild_permissions.administrator:
            await i.response.send_message(embed=emb("❌","Нет прав.",C["error"]),ephemeral=True); return
        st.set(False); await i.response.edit_message(embed=make_panel_embed(),view=self)
    @discord.ui.button(label="Новости ВКЛ/ВЫКЛ", style=discord.ButtonStyle.blurple, emoji="📰", custom_id="p_news_tog", row=0)
    async def news_toggle(self, i: discord.Interaction, b: Button):
        if not i.user.guild_permissions.administrator:
            await i.response.send_message(embed=emb("❌","Нет прав.",C["error"]),ephemeral=True); return
        st.autonews_on=not st.autonews_on; st.save()
        status="включены 🟢" if st.autonews_on else "выключены 🔴"
        await i.response.edit_message(embed=make_panel_embed(),view=self)
        await i.followup.send(embed=emb("📰",f"Авто-новости {status}",C["success"]),ephemeral=True)
    @discord.ui.button(label="Очистить истории", style=discord.ButtonStyle.gray,    emoji="🗑️", custom_id="p_clear",    row=1)
    async def clear_all(self, i: discord.Interaction, b: Button):
        if not i.user.guild_permissions.administrator:
            await i.response.send_message(embed=emb("❌","Нет прав.",C["error"]),ephemeral=True); return
        ai.clear_all(); await i.response.send_message(embed=emb("✅","Диалоги сброшены.",C["success"]),ephemeral=True)
    @discord.ui.button(label="Обновить",         style=discord.ButtonStyle.gray,    emoji="🔄", custom_id="p_refresh",  row=1)
    async def refresh(self, i: discord.Interaction, b: Button):
        await i.response.edit_message(embed=make_panel_embed(),view=self)

# ══════════════════════════════════════════════════════════════════════════════
#  🤖  БОТ
# ══════════════════════════════════════════════════════════════════════════════

intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    activity=discord.Activity(type=discord.ActivityType.watching, name="✦ CodeParis  •  🎰"),
    status=discord.Status.online,
    help_command=None
)

# ══════════════════════════════════════════════════════════════════════════════
#  📨  СОБЫТИЯ
# ══════════════════════════════════════════════════════════════════════════════

@bot.event
async def on_ready():
    print(f"[on_ready] Logged in as {bot.user}")
    for v in [VerificationView(), AIMessageView(), AdminPanelView(), TicketOpenView(), TicketCloseView()]:
        bot.add_view(v)
    try: await bot.tree.sync()
    except Exception as e: print(f"⚠️ Sync: {e}")

    await _ensure_verify_posted()
    await _ensure_ticket_posted()
    await _ensure_panel_posted()
    await _ensure_shop_posted()
    await _post_stats_chart()
    await check_and_post_updates()

    if not leaderboard_updater.is_running(): leaderboard_updater.start()
    if not auto_news_task.is_running():      auto_news_task.start()
    if not analytics_updater.is_running():   analytics_updater.start()

    await _post_work_panel()
    await _post_analytics()

    print(f"""
╔══════════════════════════════════════════╗
║  ✦  CodeParis AI Bot v5.0  •  online    ║
║  AI Mode   : {"🟢 ON " if st.ai_mode else "🔴 OFF"}                       ║
║  Auto-News : {"🟢 ON " if st.autonews_on else "🔴 OFF"} (каждые {st.news_hours}ч)             ║
║  Font Bold : {"✅ " + _FONT_BOLD if _FONT_BOLD else "⚠️ Default (no TTF)"}
║  DATA_DIR  : {os.getenv("DATA_DIR",".")}
╚══════════════════════════════════════════╝""")


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot: return
    if message.content.startswith("!"): await bot.process_commands(message); return
    if isinstance(message.author, discord.Member):
        if message.channel.id not in {ADMIN_CHANNEL_ID, VERIFY_CHANNEL_ID, STATS_CHANNEL_ID}:
            ust.add_message(message.author)
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
        ust.voice_leave(member); await _check_voice_roles(member)


async def _check_voice_roles(member):
    vh = ust.get_voice_hours(member.id)
    for h,rid,rname in sorted(VOICE_ROLES, key=lambda x: x[0]):
        if vh >= h and not ust.has_role_given(member.id,rid):
            if role:=member.guild.get_role(rid):
                if role not in member.roles:
                    try:
                        await member.add_roles(role,reason=f"Авто-роль: {h}ч")
                        ust.add_role_given(member.id,rid)
                        if ch:=bot.get_channel(STATS_CHANNEL_ID):
                            n=discord.Embed(color=C["gold"],timestamp=datetime.now())
                            n.title="🎭  Новая роль!"
                            n.description=(f"{member.mention} достиг `{h}ч` и получил **{role.mention}**! 🎉\n"
                                           f"Суммарно: `{fmt_time(vh*3600)}`")
                            n.set_thumbnail(url=member.display_avatar.url)
                            n.set_footer(text="✦ CodeParis  •  Авто-роли")
                            msg=await ch.send(embed=n); asyncio.create_task(_delete_after(msg,300))
                    except Exception as ex: print(f"⚠️ Роль {rid}: {ex}")

# ══════════════════════════════════════════════════════════════════════════════
#  ⏰  ЗАДАЧИ
# ══════════════════════════════════════════════════════════════════════════════

async def _post_analytics():
    ch=bot.get_channel(ANALYTICS_CHANNEL_ID)
    if not ch: return
    guild=getattr(ch,"guild",None)
    loop=asyncio.get_event_loop()
    buf=await loop.run_in_executor(None,generate_analytics_chart,guild)
    f=discord.File(fp=buf,filename="analytics.png")
    total_coins=sum(d.get("balance",0) for d in eco._data.values())
    total_users=len(eco._data); total_games=sum(d.get("casino_wins",0)+d.get("casino_losses",0) for d in eco._data.values())
    top_player=max(eco._data.items(),key=lambda x: x[1].get("balance",0),default=(None,{}))[1]
    top_name=top_player.get("username","?") if top_player else "?"
    e=discord.Embed(title="📊  Аналитика экономики CodeParis",color=0x0F172A,timestamp=datetime.now())
    updated=datetime.now().strftime("%d.%m.%Y  %H:%M")
    e.description=(f"```\n  Монет в обороте:  {total_coins:,}\n  Участников:       {total_users}\n"
                   f"  Игр в казино:     {total_games}\n  Богатейший:       {top_name}\n  Обновлено:        {updated}\n```")
    e.set_image(url="attachment://analytics.png")
    e.set_footer(text="✦ CodeParis  •  Аналитика  •  Обновляется каждые 30 мин")
    try:
        async for msg in ch.history(limit=30):
            if msg.author.id==bot.user.id:
                try: await msg.delete(); await asyncio.sleep(0.3)
                except Exception: pass
    except Exception: pass
    await ch.send(embed=e,file=f)

async def _post_work_panel():
    ch=bot.get_channel(WORK_CHANNEL_ID)
    if not ch: return
    e=discord.Embed(title="💼  Рабочие места — CodeParis",color=0x065F46,timestamp=datetime.now())
    e.description=("Зарабатывай монеты работая каждый день!\n"
                   "**Бесплатные работы** — доступны всем\n"
                   "**Доходные роли** — купи раз, зарабатывай вечно")
    free_lines=[]
    for j in FREE_JOBS:
        m2,s2=divmod(j["cd"],60); h_j,m_j=divmod(m2,60)
        cd_str=f"{h_j}ч {m_j}м" if h_j else (f"{m_j}м" if m_j else f"{s2}с")
        free_lines.append(f"{j['name']}\n  💰 `{j['min']}`–`{j['max']}` {COIN}  •  ⏱️ КД: `{cd_str}`")
    e.add_field(name="🆓  Бесплатные работы",value="\n".join(free_lines),inline=False)
    inc_lines=[]
    for r in INCOME_ROLES:
        lo=int(r["price"]*0.01); hi=int(r["price"]*0.05)
        inc_lines.append(f"{r['emoji']} **{r['name']}** — `{r['price']:,}` {COIN}\n  Доход: `{lo:,}`–`{hi:,}` {COIN} каждые 3 мин")
    e.add_field(name="💼  Доходные роли (купить в !магазин)",value="\n".join(inc_lines),inline=False)
    e.add_field(name="📖  Команды",
                value=("`!работать` — по всем ролям (3 мин КД)\n`!работа дворник/курьер/пицца/такси/рыбак/фриланс`\n`!баланс` — проверить монеты"),
                inline=False)
    e.set_footer(text="✦ CodeParis  •  Работай и богатей!")
    try:
        async for msg in ch.history(limit=20):
            if msg.author.id==bot.user.id and msg.embeds:
                if "Рабочие места" in (msg.embeds[0].title or ""):
                    await msg.delete(); await asyncio.sleep(0.3)
    except Exception: pass
    await ch.send(embed=e)

@tasks.loop(minutes=30)
async def analytics_updater():
    try: await _post_analytics()
    except Exception as ex: print(f"analytics_updater: {ex}")

@tasks.loop(minutes=10)
async def leaderboard_updater():
    try: await _post_stats_chart()
    except Exception as e: print(f"⚠️ leaderboard_updater: {e}")

@tasks.loop(minutes=1)
async def auto_news_task():
    if not st.autonews_on: return
    last_file=os.path.join(os.getenv("DATA_DIR","."), "last_news.txt")
    try:
        if os.path.exists(last_file):
            last_ts=float(open(last_file).read().strip())
            if time.time()-last_ts < st.news_hours*3600: return
    except Exception: pass
    try:
        await post_auto_news()
        open(last_file,"w").write(str(time.time()))
    except Exception as e: print(f"⚠️ auto_news_task: {e}")

# ══════════════════════════════════════════════════════════════════════════════
#  🔧  ВНУТРЕННИЕ ФУНКЦИИ
# ══════════════════════════════════════════════════════════════════════════════

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
                except Exception: pass
    except Exception: pass
    new_msg=await ch.send(embed=embed,file=chart_file)
    try: await new_msg.pin()
    except Exception: pass
    st.stats_msg=new_msg.id; st.save()

async def _ensure_verify_posted():
    ch=bot.get_channel(VERIFY_CHANNEL_ID)
    if not ch: return
    if st.verify_msg:
        try: await ch.fetch_message(st.verify_msg); return
        except (discord.NotFound,discord.HTTPException): pass
    try:
        async for msg in ch.history(limit=20):
            if msg.author.id==bot.user.id: await msg.delete(); await asyncio.sleep(0.3)
    except Exception: pass
    msg=await ch.send(embed=make_verify_embed(),view=VerificationView())
    st.verify_msg=msg.id; st.save()

async def _force_reverify():
    ch=bot.get_channel(VERIFY_CHANNEL_ID)
    if not ch: return
    try:
        async for msg in ch.history(limit=50):
            if msg.author.id==bot.user.id: await msg.delete(); await asyncio.sleep(0.3)
    except Exception: pass
    st.verify_msg=None
    msg=await ch.send(embed=make_verify_embed(),view=VerificationView())
    st.verify_msg=msg.id; st.save()

async def _ensure_ticket_posted():
    ch=bot.get_channel(TICKET_CHANNEL_ID)
    if not ch: return
    if st.ticket_msg:
        try: await ch.fetch_message(st.ticket_msg); return
        except (discord.NotFound,discord.HTTPException): pass
    try:
        async for msg in ch.history(limit=20):
            if msg.author.id==bot.user.id and msg.embeds:
                if "Поддержка" in (msg.embeds[0].title or "") or "Тикет" in (msg.embeds[0].title or ""):
                    await msg.delete(); await asyncio.sleep(0.3)
    except Exception: pass
    msg=await ch.send(embed=make_ticket_embed(),view=TicketOpenView())
    st.ticket_msg=msg.id; st.save()

async def _ensure_panel_posted():
    ch=bot.get_channel(ADMIN_CHANNEL_ID)
    if not ch: return
    try:
        async for msg in ch.history(limit=15):
            if msg.author.id==bot.user.id and msg.embeds:
                if "Панель" in (msg.embeds[0].title or ""): await msg.delete(); await asyncio.sleep(0.3)
    except Exception: pass
    await ch.send(embed=make_panel_embed(),view=AdminPanelView())

async def _ensure_shop_posted():
    ch=bot.get_channel(SHOP_CHANNEL_ID)
    if not ch: return
    try:
        async for msg in ch.history(limit=20):
            if msg.author.id==bot.user.id and msg.embeds:
                if "Магазин" in (msg.embeds[0].title or ""): await msg.delete(); await asyncio.sleep(0.3)
    except Exception: pass
    msg=await ch.send(embed=make_shop_embed()); st.shop_msg=msg.id; st.save()

async def _forward_admin(message):
    ch=bot.get_channel(AI_CHANNEL_ID)
    if not ch: await message.reply(embed=emb("❌","AI-канал не найден!",C["error"]),delete_after=4); return
    e=ai_embed(message.content)
    if message.attachments: e.set_image(url=message.attachments[0].url)
    await ch.send(embed=e,view=AIMessageView())
    st.stats["admin_forwards"]+=1; st.save()
    await message.reply(embed=emb("✅",f"Отправлено в <#{AI_CHANNEL_ID}>.",C["success"]),delete_after=4,mention_author=False)

async def _ai_reply(message):
    async with message.channel.typing():
        response=await ai.get_response(message.author.id,message.content)
    await message.channel.send(embed=ai_embed(response),view=AIMessageView())
    st.stats["ai_responses"]+=1; st.save()

def admin_only():
    def pred(ctx):
        return ctx.channel.id==ADMIN_CHANNEL_ID and ctx.author.guild_permissions.administrator
    return commands.check(pred)

# ══════════════════════════════════════════════════════════════════════════════
#  🎰  КАЗИНО — КОМАНДЫ
# ══════════════════════════════════════════════════════════════════════════════

@bot.command(name="баланс", aliases=["bal","balance","монеты","кошелёк"])
async def cmd_balance(ctx, member: discord.Member=None):
    target=member or ctx.author; d=eco.get_user_data(target.id)
    e=discord.Embed(title=f"💰  Баланс — {target.display_name}",color=C["gold"],timestamp=datetime.now())
    e.set_thumbnail(url=target.display_avatar.url)
    e.add_field(name="💳 Баланс",     value=f"**`{d['balance']:,}`** {COIN}", inline=True)
    e.add_field(name="💹 Заработано", value=f"`{d['total_earned']:,}` {COIN}", inline=True)
    e.add_field(name="🛒 Потрачено",  value=f"`{d['total_spent']:,}` {COIN}", inline=True)
    owned=d.get("income_roles",[])
    if owned:
        names=[r["name"] for r in INCOME_ROLES if r["id"] in owned]
        e.add_field(name="💼 Доходные роли",value="\n".join(names),inline=False)
    else:
        e.add_field(name="💼 Доходные роли",value="Нет. Купи в `!магазин`!",inline=False)
    wins=d.get("casino_wins",0); losses=d.get("casino_losses",0)
    if wins or losses:
        e.add_field(name="🎰 Казино",value=f"🏆 `{wins}` побед  •  `{losses}` поражений",inline=False)
    e.set_footer(text="✦ CodeParis  •  Экономика")
    msg=await ctx.send(embed=e); asyncio.create_task(_delete_after(msg,60))
    try: await ctx.message.delete()
    except: pass

@bot.command(name="работать", aliases=["work","раб","ворк"])
async def cmd_work(ctx):
    uid=ctx.author.id; can,remaining=eco.can_work(uid)
    if not can:
        m2,s2=divmod(int(remaining),60)
        e=emb("⏳  Ещё рано!",f"Следующая работа через **{m2}м {s2:02d}с**\n\nПока иди в казино! 🎰 `!рулетка <ставка>`",C["warn"])
        msg=await ctx.send(embed=e); asyncio.create_task(_delete_after(msg,8))
        try: await ctx.message.delete()
        except: pass; return
    owned=eco.get_income_roles(uid)
    if not owned:
        e=emb("💼  Нет работы",f"Купи доходную роль в магазине!\n\nКоманда: `!магазин` или загляни в <#{SHOP_CHANNEL_ID}>",C["warn"])
        msg=await ctx.send(embed=e); asyncio.create_task(_delete_after(msg,10))
        try: await ctx.message.delete()
        except: pass; return
    earned=eco.do_work(uid); balance=eco.get_balance(uid)
    role_names=[r["name"] for r in INCOME_ROLES if r["id"] in owned]
    e=discord.Embed(title="💼  Рабочий день завершён!",color=C["success"],timestamp=datetime.now())
    e.set_thumbnail(url=ctx.author.display_avatar.url)
    e.description=(f"**{ctx.author.display_name}** хорошо поработал! 💪\n\n"
                   f"```\n  Заработано:  +{earned:,} {COIN}\n  Баланс:       {balance:,} {COIN}\n```")
    e.add_field(name="💼 Активные роли",value="\n".join(role_names),inline=False)
    e.set_footer(text=f"✦ Следующая работа через {WORK_COOLDOWN//60} мин  •  CodeParis")
    eco.set_username(ctx.author.id,ctx.author.display_name)
    work_ch=bot.get_channel(WORK_CHANNEL_ID)
    if work_ch and work_ch.id!=ctx.channel.id:
        await work_ch.send(embed=e)
        notif=emb("✅  Смена закрыта!",f"Заработано: **`{earned:,}` {COIN}**\nБаланс: `{balance:,}` {COIN}\nРепорт → <#{WORK_CHANNEL_ID}>",C["success"])
        msg=await ctx.send(embed=notif); asyncio.create_task(_delete_after(msg,10))
    else:
        msg=await ctx.send(embed=e); asyncio.create_task(_delete_after(msg,30))
    try: await ctx.message.delete()
    except: pass

@bot.command(name="работа", aliases=["job","джоб"])
async def cmd_free_job(ctx, job_name: str=None):
    if not job_name:
        uid=ctx.author.id; lines=[]
        for j in FREE_JOBS:
            can,remaining=eco.can_free_job(uid,j["id"])
            status="✅ Доступно" if can else f"⏳ {int(remaining//60)}м {int(remaining%60):02d}с"
            m2,s2=divmod(j["cd"],60); h_j,m_j=divmod(m2,60)
            cd_str=f"{h_j}ч {m_j}м" if h_j else (f"{m_j}м" if m_j else f"{s2}с")
            lines.append(f"{j['name']} — {status}  |  КД `{cd_str}`  |  `{j['min']}`–`{j['max']}` {COIN}")
        e=discord.Embed(title="💼  Доступные работы",color=0x065F46,timestamp=datetime.now())
        e.description="\n".join(lines)
        e.add_field(name="📖 Использование",value="`!работа дворник` / `!работа курьер` / ...",inline=False)
        e.set_footer(text="✦ CodeParis  •  Бесплатные работы")
        msg=await ctx.send(embed=e); asyncio.create_task(_delete_after(msg,30))
        try: await ctx.message.delete()
        except: pass; return

    name_lower=job_name.strip().lower()
    job_map={"дворник":"janitor","janitor":"janitor","метла":"janitor",
             "курьер":"courier","courier":"courier","посылки":"courier",
             "пицца":"pizza","pizza":"pizza","разносчик":"pizza",
             "такси":"taxi","taxi":"taxi","водитель":"taxi",
             "рыбак":"fisherman","рыбалка":"fisherman","fish":"fisherman",
             "фриланс":"programmer","фрилансер":"programmer","программист":"programmer","прога":"programmer"}
    job_id=job_map.get(name_lower)
    if not job_id:
        e=emb("❌  Работа не найдена","Доступные работы: `дворник` / `курьер` / `пицца` / `такси` / `рыбак` / `фриланс`",C["error"])
        msg=await ctx.send(embed=e); asyncio.create_task(_delete_after(msg,8))
        try: await ctx.message.delete()
        except: pass; return

    uid=ctx.author.id; can,remaining=eco.can_free_job(uid,job_id)
    if not can:
        m2,s2=divmod(int(remaining),60)
        e=emb("⏳  Работа ещё не готова",f"Следующий выход через **{m2}м {s2:02d}с**",C["warn"])
        msg=await ctx.send(embed=e); asyncio.create_task(_delete_after(msg,8))
        try: await ctx.message.delete()
        except: pass; return

    job=next(j for j in FREE_JOBS if j["id"]==job_id)
    earn=eco.do_free_job(uid,job_id); eco.set_username(uid,ctx.author.display_name); bal=eco.get_balance(uid)
    story_tmpl=random.choice(job["stories"]); story=story_tmpl.format(earn=f"{earn:,}",coin=COIN)
    e_work=discord.Embed(title=f"{job['name']}  •  Смена закрыта!",color=0x065F46,timestamp=datetime.now())
    e_work.set_thumbnail(url=ctx.author.display_avatar.url)
    e_work.description=(f"**{ctx.author.display_name}** хорошо поработал!\n> _{story}_\n"
                        f"```\n  Заработано:  +{earn:,} {COIN}\n  Баланс:       {bal:,} {COIN}\n```")
    m2,s2=divmod(job["cd"],60); h_j,m_j=divmod(m2,60)
    cd_str=f"{h_j}ч {m_j}м" if h_j else (f"{m_j}м" if m_j else f"{s2}с")
    e_work.set_footer(text=f"✦ Следующий выход через {cd_str}  •  CodeParis")
    work_ch=bot.get_channel(WORK_CHANNEL_ID)
    if work_ch and work_ch.id!=ctx.channel.id:
        await work_ch.send(embed=e_work)
        notif=emb("✅  Работа выполнена!",f"Заработано: **`{earn:,}` {COIN}**\nБаланс: `{bal:,}` {COIN}\nРепорт → <#{WORK_CHANNEL_ID}>",C["success"])
        msg=await ctx.send(embed=notif); asyncio.create_task(_delete_after(msg,10))
    else:
        msg=await ctx.send(embed=e_work); asyncio.create_task(_delete_after(msg,30))
    try: await ctx.message.delete()
    except: pass

@bot.command(name="магазин", aliases=["shop","шоп"])
async def cmd_shop(ctx):
    msg=await ctx.send(embed=make_shop_embed()); asyncio.create_task(_delete_after(msg,120))
    try: await ctx.message.delete()
    except: pass

@bot.command(name="купить", aliases=["buy"])
async def cmd_buy(ctx, *, name: str=None):
    if not name:
        e=emb("❌","Укажи название роли.\nПример: `!купить новичок`",C["error"])
        msg=await ctx.send(embed=e); asyncio.create_task(_delete_after(msg,8))
        try: await ctx.message.delete()
        except: pass; return
    uid=ctx.author.id; name=name.strip().lower()
    inc_match=next((r for r in INCOME_ROLES if name in r["name"].lower() or name in r["id"].lower()),None)
    if inc_match:
        if eco.has_income_role(uid,inc_match["id"]):
            e=emb("ℹ️  Уже куплено",f"Роль **{inc_match['name']}** у тебя уже есть!\nПиши `!работать` каждые 3 мин 💰",C["info"])
        elif eco.get_balance(uid)<inc_match["price"]:
            bal=eco.get_balance(uid)
            e=emb("❌  Недостаточно монет",f"Нужно `{inc_match['price']:,}` {COIN}\nУ тебя: `{bal:,}` {COIN}",C["error"])
        else:
            eco.buy_income_role(uid,inc_match["id"],inc_match["price"])
            lo=int(inc_match["price"]*0.01); hi=int(inc_match["price"]*0.05)
            e=discord.Embed(title="✅  Роль куплена!",color=C["success"],timestamp=datetime.now())
            e.set_thumbnail(url=ctx.author.display_avatar.url)
            e.description=(f"Ты купил **{inc_match['name']}**\n\n"
                           f"```\n  Доход за работу:  {lo:,}–{hi:,} {COIN}\n  Баланс:           {eco.get_balance(uid):,} {COIN}\n```\n"
                           f"Теперь пиши `!работать` каждые 3 мин! 💼")
            e.set_footer(text="✦ CodeParis  •  Магазин")
        msg=await ctx.send(embed=e); asyncio.create_task(_delete_after(msg,20))
        try: await ctx.message.delete()
        except: pass; return
    cos_match=next((r for r in COSMETIC_ROLES if name in r["name"].lower()),None)
    if cos_match:
        if eco.has_cosmetic_role(uid,cos_match["discord_role"]):
            e=emb("ℹ️  Уже куплено",f"**{cos_match['name']}** у тебя уже есть!\nНадень/сними через `!профиль` 🎭",C["info"])
        elif eco.get_balance(uid)<cos_match["price"]:
            bal=eco.get_balance(uid)
            e=emb("❌  Недостаточно монет",f"Нужно `{cos_match['price']:,}` {COIN}\nУ тебя: `{bal:,}` {COIN}",C["error"])
        else:
            eco.buy_cosmetic_role(uid,cos_match["discord_role"],cos_match["price"])
            role_obj=ctx.guild.get_role(cos_match["discord_role"])
            if role_obj:
                try: await ctx.author.add_roles(role_obj,reason="Покупка косметической роли")
                except Exception: pass
            e=discord.Embed(title="✅  Косметическая роль куплена!",color=C["success"],timestamp=datetime.now())
            e.set_thumbnail(url=ctx.author.display_avatar.url)
            e.description=(f"**{ctx.author.display_name}** приобрёл **{cos_match['name']}**! 🎭\n"
                           f"Роль автоматически надета. Управляй через `!профиль`\n\nБаланс: `{eco.get_balance(uid):,}` {COIN}")
            e.set_footer(text="✦ CodeParis  •  Магазин")
        msg=await ctx.send(embed=e); asyncio.create_task(_delete_after(msg,20))
        try: await ctx.message.delete()
        except: pass; return
    e=emb("❌  Роль не найдена",f"Роль с названием `{name}` не найдена.\nСмотри список в `!магазин`",C["error"])
    msg=await ctx.send(embed=e); asyncio.create_task(_delete_after(msg,10))
    try: await ctx.message.delete()
    except: pass

@bot.command(name="профиль", aliases=["profile","проф"])
async def cmd_profile(ctx, member: discord.Member=None):
    target=member or ctx.author
    view=ProfileCosmeticView(target) if target.id==ctx.author.id else None
    e=make_profile_embed(target)
    if view and view.children: msg=await ctx.send(embed=e,view=view)
    else: msg=await ctx.send(embed=e)
    asyncio.create_task(_delete_after(msg,90))
    try: await ctx.message.delete()
    except: pass

@bot.command(name="топмонет", aliases=["richlist","богачи","топбаланс"])
async def cmd_top_money(ctx):
    top=eco.get_top(10); guild=ctx.guild
    e=discord.Embed(title="💰  Топ богатейших — CodeParis",color=C["gold"],timestamp=datetime.now())
    if not top: e.description="Пока нет данных об экономике."
    else:
        lines=[]
        for rank,(uid,bal) in enumerate(top,1):
            member=guild.get_member(uid)
            name=discord.utils.escape_markdown(member.display_name if member else f"<@{uid}>")
            lines.append(f"{medal(rank)} **{name}** — `{bal:,}` {COIN}")
        e.description="\n".join(lines)
    e.set_footer(text="✦ CodeParis  •  Экономика")
    msg=await ctx.send(embed=e); asyncio.create_task(_delete_after(msg,60))
    try: await ctx.message.delete()
    except: pass

# ══════════════════════════════════════════════════════════════════════════════
#  🎡  РУЛЕТКА
# ══════════════════════════════════════════════════════════════════════════════

@bot.command(name="рулетка", aliases=["roulette","рул","spin"])
async def cmd_roulette(ctx, *, arg: str=None):
    allowed={CASINO_CHANNEL_ID,CASINO_CMD_CHANNEL_ID}
    if ctx.channel.id not in allowed:
        e=emb("🎰  Казино",f"Рулетка работает только в <#{CASINO_CHANNEL_ID}>!",C["warn"])
        msg=await ctx.send(embed=e); asyncio.create_task(_delete_after(msg,6))
        try: await ctx.message.delete()
        except: pass; return
    try: await ctx.message.delete()
    except: pass

    if arg and arg.lower() in ("старт","start","new","новая"):
        if roulette.active:
            e=emb("ℹ️","Игра уже идёт! Делай ставку: `!рулетка <сумма>`",C["info"])
            msg=await ctx.send(embed=e); asyncio.create_task(_delete_after(msg,6)); return
        roulette.reset(); roulette.game_num+=1; roulette.active=True; roulette.start_t=time.time()
        loop=asyncio.get_event_loop()
        buf=await loop.run_in_executor(None,generate_roulette_wheel,roulette.players,ROULETTE_WAIT,None,roulette.game_num)
        f=discord.File(fp=buf,filename="roulette.png")
        embed=make_roulette_embed(roulette.players,ROULETTE_WAIT,game_num=roulette.game_num)
        embed.set_image(url="attachment://roulette.png")
        roulette.message=await ctx.send(embed=embed,file=f,view=RouletteView(ctx.channel))
        asyncio.create_task(_roulette_countdown(ctx.channel)); return

    if arg is None:
        e=emb("❌  Укажи ставку","Пример: `!рулетка 500`\nИли `!рулетка старт`",C["error"])
        msg=await ctx.send(embed=e); asyncio.create_task(_delete_after(msg,8)); return

    try:
        bet=int(arg.replace(",","").replace(".","").replace(" ",""))
    except ValueError:
        e=emb("❌","Укажи целое число монет.\nПример: `!рулетка 500`",C["error"])
        msg=await ctx.send(embed=e); asyncio.create_task(_delete_after(msg,6)); return

    if bet < 10:
        e=emb("❌","Минимальная ставка: `10` "+COIN,C["error"])
        msg=await ctx.send(embed=e); asyncio.create_task(_delete_after(msg,6)); return

    uid=ctx.author.id; bal=eco.get_balance(uid)
    if bal < bet:
        e=emb("❌  Недостаточно монет",f"У тебя: `{bal:,}` {COIN}\nСтавка: `{bet:,}` {COIN}",C["error"])
        msg=await ctx.send(embed=e); asyncio.create_task(_delete_after(msg,8)); return
    if uid in roulette.players:
        e=emb("ℹ️  Уже участвуешь",f"Твоя ставка: `{roulette.players[uid]['bet']:,}` {COIN}",C["info"])
        msg=await ctx.send(embed=e); asyncio.create_task(_delete_after(msg,6)); return

    eco.spend(uid,bet); roulette.add_player(uid,ctx.author.display_name,bet); eco.casino_lose(uid,bet)

    if not roulette.active:
        roulette.game_num+=1; roulette.active=True; roulette.start_t=time.time()
        loop=asyncio.get_event_loop()
        buf=await loop.run_in_executor(None,generate_roulette_wheel,dict(roulette.players),ROULETTE_WAIT,None,roulette.game_num)
        f=discord.File(fp=buf,filename="roulette.png")
        embed=make_roulette_embed(dict(roulette.players),ROULETTE_WAIT,game_num=roulette.game_num)
        embed.set_image(url="attachment://roulette.png")
        roulette.message=await ctx.send(embed=embed,file=f,view=RouletteView(ctx.channel))
        asyncio.create_task(_roulette_countdown(ctx.channel))
    else:
        remain=max(0,int(ROULETTE_WAIT-(time.time()-roulette.start_t)))
        loop=asyncio.get_event_loop()
        buf=await loop.run_in_executor(None,generate_roulette_wheel,dict(roulette.players),remain,None,roulette.game_num)
        f=discord.File(fp=buf,filename="roulette.png")
        embed=make_roulette_embed(dict(roulette.players),remain,game_num=roulette.game_num)
        embed.set_image(url="attachment://roulette.png")
        try:
            if roulette.message: await roulette.message.delete()
        except Exception: pass
        roulette.message=await ctx.channel.send(embed=embed,file=f)
        notif=emb("✅  Ставка принята!",f"**{ctx.author.display_name}** поставил `{bet:,}` {COIN}\nБанк: `{roulette.total_pot():,}` {COIN}",C["success"])
        notif_msg=await ctx.send(embed=notif); asyncio.create_task(_delete_after(notif_msg,5))


async def _roulette_countdown(channel: discord.TextChannel):
    await asyncio.sleep(ROULETTE_WAIT)
    if not roulette.active or not roulette.players:
        roulette.reset(); return

    if len(roulette.players) < 2:
        uid,data=list(roulette.players.items())[0]
        eco.add_balance(uid,data["bet"])
        d=eco._get(uid)
        d["casino_losses"]=max(0,d.get("casino_losses",1)-1)
        d["casino_lost"]=max(0,d.get("casino_lost",data["bet"])-data["bet"]); eco.save()
        new_bal=eco.get_balance(uid)
        e=discord.Embed(title="ℹ️  Рулетка отменена — нет соперников",color=C["warn"],timestamp=datetime.now())
        e.description=(f"<@{uid}>, никто не составил тебе компанию 😔\n\n"
                       f"```\n  Ставка возвращена:  {data['bet']:,} {COIN}\n  Твой баланс:        {new_bal:,} {COIN}\n```\n"
                       f"Позови друзей и попробуй снова! `!рулетка <ставка>`")
        e.set_footer(text=f"✦ CodeParis  •  Игра #{roulette.game_num}")
        await channel.send(content=f"<@{uid}>",embed=e,allowed_mentions=discord.AllowedMentions(users=True))
        roulette.reset(); return

    winner_uid,winner_data=roulette.spin(); pot=roulette.total_pot()
    if winner_uid:
        eco.casino_win(winner_uid,pot)
        d=eco._get(winner_uid)
        d["casino_losses"]=max(0,d.get("casino_losses",1)-1)
        d["casino_lost"]=max(0,d.get("casino_lost",winner_data["bet"])-winner_data["bet"]); eco.save()

    players_snapshot=dict(roulette.players); game_num_snap=roulette.game_num
    try:
        if roulette.message: await roulette.message.delete()
    except Exception: pass

    await channel.send(content=f"🎡 Рулетка крутится... <@{winner_uid}>",allowed_mentions=discord.AllowedMentions(users=True))
    loop=asyncio.get_event_loop()
    gif_buf=await loop.run_in_executor(None,generate_spin_gif,players_snapshot,winner_uid,game_num_snap)
    gif_file=discord.File(fp=gif_buf,filename="spin.gif")
    spin_msg=await channel.send(file=gif_file); asyncio.create_task(_delete_after(spin_msg,15))
    await asyncio.sleep(4)

    buf=await loop.run_in_executor(None,generate_roulette_wheel,players_snapshot,None,winner_uid,game_num_snap)
    f=discord.File(fp=buf,filename="roulette_result.png")
    embed=make_roulette_embed(players_snapshot,winner_uid=winner_uid,game_num=game_num_snap,finished=True)
    embed.set_image(url="attachment://roulette_result.png")
    result_msg=await channel.send(content=f"🎉 <@{winner_uid}> победил в рулетке!",embed=embed,file=f,
                                   allowed_mentions=discord.AllowedMentions(users=True))
    summary=discord.Embed(title="🏆  Итоги игры",color=C["gold"],timestamp=datetime.now())
    summary.description=(f"**{winner_data['name']}** забрал весь банк!\n\n"
                         f"```\n  Банк:        {pot:,} {COIN}\n  Ставка:      {winner_data['bet']:,} {COIN}\n"
                         f"  Шанс:        {winner_data['bet']/pot*100:.1f}%\n  Новый баланс: {eco.get_balance(winner_uid):,} {COIN}\n```")
    summary.set_footer(text=f"✦ CodeParis  •  Игра #{roulette.game_num}")
    await channel.send(embed=summary)
    asyncio.create_task(_delete_after(result_msg,120)); roulette.reset()

# ══════════════════════════════════════════════════════════════════════════════
#  👑  КОМАНДЫ АДМИНИСТРАТОРА
# ══════════════════════════════════════════════════════════════════════════════

@bot.command(name="say")
@admin_only()
async def cmd_say(ctx, *, text: str):
    ch=bot.get_channel(AI_CHANNEL_ID)
    if not ch: await ctx.send(embed=emb("❌","Канал не найден!",C["error"]),delete_after=4); return
    await ch.send(embed=ai_embed(text),view=AIMessageView())
    st.stats["admin_forwards"]+=1; st.save()
    await ctx.send(embed=emb("✅",f"Отправлено в <#{AI_CHANNEL_ID}>.",C["success"]),delete_after=4)
    try: await ctx.message.delete()
    except: pass

@bot.command(name="aiclear")
@admin_only()
async def cmd_aiclear(ctx, user_id: str=None):
    if user_id:
        try: ai.clear(int(user_id)); e=emb("✅",f"История `{user_id}` удалена.",C["success"])
        except ValueError: e=emb("❌","Укажи числовой ID.",C["error"])
    else: ai.clear_all(); e=emb("✅","Все диалоги сброшены.",C["success"])
    await ctx.send(embed=e,delete_after=5)

@bot.command(name="aistats")
@admin_only()
async def cmd_aistats(ctx):
    up=str(datetime.now()-datetime.fromisoformat(st.stats["start"])).split(".")[0]
    e=emb("📊 Статистика бота",
          f"```\nАптайм:          {up}\nAI ответов:      {st.stats['ai_responses']}\n"
          f"Пересылок:       {st.stats['admin_forwards']}\nВерифицировано:  {st.stats.get('verified',0)}\n"
          f"Тикетов:         {st.stats.get('tickets',0)}\nНовостей:        {st.news_counter}\n"
          f"AI Mode:         {'ON' if st.ai_mode else 'OFF'}\nАвто-новости:    {'ON' if st.autonews_on else 'OFF'}\n"
          f"Шрифт:           {'TTF OK' if _FONT_BOLD else 'Default'}\n```",C["info"])
    await ctx.send(embed=e,delete_after=15)

@bot.command(name="reverify")
@admin_only()
async def cmd_reverify(ctx):
    await _force_reverify()
    await ctx.send(embed=emb("✅",f"Верификация пересоздана в <#{VERIFY_CHANNEL_ID}>.",C["success"]),delete_after=5)
    try: await ctx.message.delete()
    except: pass

@bot.command(name="reticket")
@admin_only()
async def cmd_reticket(ctx):
    st.ticket_msg=None; await _ensure_ticket_posted()
    await ctx.send(embed=emb("✅",f"Тикет-панель обновлена в <#{TICKET_CHANNEL_ID}>.",C["success"]),delete_after=5)
    try: await ctx.message.delete()
    except: pass

@bot.command(name="reshop")
@admin_only()
async def cmd_reshop(ctx):
    await _ensure_shop_posted()
    await ctx.send(embed=emb("✅",f"Магазин обновлён в <#{SHOP_CHANNEL_ID}>.",C["success"]),delete_after=5)
    try: await ctx.message.delete()
    except: pass

@bot.command(name="resetstats")
@admin_only()
async def cmd_resetstats(ctx, user_id: str=None):
    if user_id:
        key=str(user_id)
        if key in ust._data: del ust._data[key]; ust.save(); await ctx.send(embed=emb("✅",f"Стат. `{user_id}` сброшена.",C["success"]),delete_after=5)
        else: await ctx.send(embed=emb("❌","Пользователь не найден.",C["error"]),delete_after=5)
    else: ust._data.clear(); ust.save(); await ctx.send(embed=emb("✅","Вся статистика сброшена.",C["success"]),delete_after=5)
    try: await ctx.message.delete()
    except: pass

@bot.command(name="reseteco")
@admin_only()
async def cmd_reseteco(ctx, user_id: str=None):
    if user_id:
        try: eco.reset_user(int(user_id)); await ctx.send(embed=emb("✅",f"Экономика `{user_id}` сброшена.",C["success"]),delete_after=5)
        except ValueError: await ctx.send(embed=emb("❌","Укажи числовой ID.",C["error"]),delete_after=5)
    else: eco.reset_all(); await ctx.send(embed=emb("✅","Вся экономика сброшена.",C["success"]),delete_after=5)
    try: await ctx.message.delete()
    except: pass

@bot.command(name="givemoney")
@admin_only()
async def cmd_givemoney(ctx, member: discord.Member=None, amount: int=None):
    if not member or not amount:
        await ctx.send(embed=emb("❌","Использование: `!givemoney @user <сумма>`",C["error"]),delete_after=6)
        try: await ctx.message.delete()
        except: pass; return
    eco.add_balance(member.id,amount); bal=eco.get_balance(member.id)
    await ctx.send(embed=emb("✅",f"**{member.display_name}** получил `{amount:,}` {COIN}\nНовый баланс: `{bal:,}` {COIN}",C["success"]),delete_after=8)
    try: await ctx.message.delete()
    except: pass

@bot.command(name="postnews")
@admin_only()
async def cmd_postnews(ctx, *, custom_topic: str=None):
    await ctx.send(embed=emb("⏳","Генерирую новость...",""),delete_after=5)
    try: await ctx.message.delete()
    except: pass
    ch=bot.get_channel(NEWS_CHANNEL_ID)
    if not ch: await ctx.send(embed=emb("❌","Канал новостей не найден!",C["error"]),delete_after=8); return
    topic=custom_topic or random.choice(NEWS_TOPICS); text=await ai.generate_news(topic)
    st.news_counter+=1; st.save()
    e=discord.Embed(color=C["news"],timestamp=datetime.now())
    e.title=f"📰  Новости CodeParis  #{st.news_counter}"; e.description=text
    e.set_footer(text="✦ Vemby  •  Авто-новости CodeParis")
    await ch.send(embed=e)
    await ctx.send(embed=emb("✅",f"Новость #{st.news_counter} опубликована.",C["success"]),delete_after=5)

@bot.command(name="postupdate")
@admin_only()
async def cmd_postupdate(ctx, version: str=None):
    try: await ctx.message.delete()
    except: pass
    if version:
        update=next((u for u in SERVER_CHANGELOG if u["version"]==version),None)
        if not update: await ctx.send(embed=emb("❌",f"Версия `{version}` не найдена.",C["error"]),delete_after=8); return
    else:
        update=next((u for u in SERVER_CHANGELOG if not u.get("posted",False)),None)
        if not update: await ctx.send(embed=emb("ℹ️","Все обновления уже опубликованы.",C["info"]),delete_after=8); return
    await ctx.send(embed=emb("⏳",f"Публикую {update['version']}...",""),delete_after=5)
    await post_update_report(update)
    await ctx.send(embed=emb("✅",f"Отчёт {update['version']} опубликован.",C["success"]),delete_after=5)

@bot.command(name="autonews")
@admin_only()
async def cmd_autonews(ctx, action: str=None, value: str=None):
    try: await ctx.message.delete()
    except: pass
    if action=="on": st.autonews_on=True; st.save(); await ctx.send(embed=emb("📰","🟢 Включены",C["success"]),delete_after=5)
    elif action=="off": st.autonews_on=False; st.save(); await ctx.send(embed=emb("📰","🔴 Выключены",C["warn"]),delete_after=5)
    elif action=="interval" and value:
        try:
            h=int(value)
            if 1<=h<=48: st.news_hours=h; st.save(); await ctx.send(embed=emb("📰",f"Теперь каждые **{h}ч**",C["success"]),delete_after=5)
            else: await ctx.send(embed=emb("❌","От 1 до 48 часов.",C["error"]),delete_after=5)
        except ValueError: await ctx.send(embed=emb("❌","Укажи число.",C["error"]),delete_after=5)
    else:
        status="🟢 Включены" if st.autonews_on else "🔴 Выключены"
        e=emb("📰 Статус авто-новостей",color=C["news"])
        e.add_field(name="Состояние",value=status,inline=True)
        e.add_field(name="Интервал",value=f"`{st.news_hours}ч`",inline=True)
        e.add_field(name="Опубликовано",value=f"`{st.news_counter}`",inline=True)
        await ctx.send(embed=e,delete_after=15)

@bot.command(name="аналитика", aliases=["analytics"])
@admin_only()
async def cmd_analytics(ctx):
    try: await ctx.message.delete()
    except: pass
    await ctx.send(embed=emb("⏳","Генерирую аналитику...",""),delete_after=5)
    await _post_analytics()
    await ctx.send(embed=emb("✅",f"Аналитика обновлена в <#{ANALYTICS_CHANNEL_ID}>.",C["success"]),delete_after=5)

@bot.command(name="рабочие", aliases=["workpanel"])
@admin_only()
async def cmd_work_panel(ctx):
    try: await ctx.message.delete()
    except: pass
    await _post_work_panel()
    await ctx.send(embed=emb("✅",f"Панель работ обновлена в <#{WORK_CHANNEL_ID}>.",C["success"]),delete_after=5)

@bot.command(name="mystats")
async def cmd_mystats(ctx, member: discord.Member=None):
    target=member or ctx.author
    msg=await ctx.send(embed=make_personal_stats_embed(target))
    asyncio.create_task(_delete_after(msg,60))
    try: await ctx.message.delete()
    except: pass

@bot.command(name="leaderboard", aliases=["lb","топ"])
async def cmd_leaderboard(ctx):
    await ctx.send(embed=emb("⏳","Генерирую график...",C["info"]),delete_after=5)
    try: await ctx.message.delete()
    except: pass
    await _post_stats_chart()

@bot.command(name="с")
@commands.has_permissions(manage_messages=True)
async def cmd_clear_chat(ctx, amount: int=None):
    if amount is None:
        await ctx.send(embed=emb("❌","Пример: `!с 50`",C["error"]),delete_after=5)
        try: await ctx.message.delete()
        except: pass; return
    if not 1<=amount<=1000:
        await ctx.send(embed=emb("❌","От **1** до **1000**.",C["error"]),delete_after=5)
        try: await ctx.message.delete()
        except: pass; return
    try: await ctx.message.delete()
    except: pass
    deleted=await ctx.channel.purge(limit=amount)
    msg=await ctx.send(embed=emb("🗑️ Чат очищен",f"Удалено: **{len(deleted)}**\nМодератор: {ctx.author.mention}",C["success"]))
    await asyncio.sleep(4)
    try: await msg.delete()
    except: pass

@cmd_clear_chat.error
async def clear_chat_error(ctx, error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send(embed=emb("❌","Нужны права **Manage Messages**.",C["error"]),delete_after=5)
    elif isinstance(error,commands.BadArgument):
        await ctx.send(embed=emb("❌","Укажи целое число.",C["error"]),delete_after=5)

@bot.command(name="ping")
async def cmd_ping(ctx):
    ms=round(bot.latency*1000)
    await ctx.send(embed=emb("🏓 Пинг",f"Задержка: **{ms} мс**",
        C["success"] if ms<100 else C["warn"] if ms<200 else C["error"]),delete_after=5)

@bot.command(name="help")
@admin_only()
async def cmd_help(ctx):
    e=discord.Embed(title="✦  Полный список команд  —  CodeParis v5.0",color=C["panel"],timestamp=datetime.now())
    e.add_field(name="👑  АДМИН",value=(
        "`!say <текст>` — опубликовать от имени ИИ\n`!aiclear [id]` — сброс истории AI\n`!aistats` — статистика бота\n"
        "`!reverify` — перепостить верификацию\n`!reticket` — перепостить тикеты\n`!reshop` — перепостить магазин\n"
        "`!resetstats [id]` — сброс статистики\n`!reseteco [id]` — сброс экономики\n`!givemoney @user <сумма>` — выдать монеты\n"
        "`!postnews [тема]` — новость\n`!postupdate [версия]` — обновление\n`!autonews [on|off|interval <ч>]` — расписание\n"
    ),inline=False)
    e.add_field(name="👥  ДЛЯ ВСЕХ",value=(
        "`!баланс` `!работать` `!работа <тип>` `!магазин` `!купить` `!профиль` `!топмонет`\n"
        "`!рулетка <ставка>` `!mystats` `!lb` `!ping`"
    ),inline=False)
    e.set_footer(text="✦ CodeParis Admin Panel  •  v5.0")
    await ctx.send(embed=e,delete_after=30)
    try: await ctx.message.delete()
    except: pass

# ══════════════════════════════════════════════════════════════════════════════
#  🚀  ЗАПУСК
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if not TOKEN:
        print("❌ Токен не найден! Укажи переменную среды BOT_TOKEN или TOKEN")
        print("   В Railway: Settings → Variables → Add Variable")
        print("   Имя: BOT_TOKEN  Значение: ваш токен")
        sys.exit(1)

    print(f"✅ Токен найден (первые символы: {TOKEN[:10]}...)")
    print(f"✅ GROQ_API_KEY: {'найден' if GROQ_API_KEY else '❌ НЕ ЗАДАН — AI будет недоступен'}")
    print(f"✅ Шрифт: {_FONT_BOLD or 'Default (TTF не найден)'}")
    print(f"✅ DATA_DIR: {os.getenv('DATA_DIR','.')} (⚠️ на Railway данные сбрасываются при рестарте!)")

    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("❌ Неверный токен Discord! Проверь переменную BOT_TOKEN в Railway.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)
