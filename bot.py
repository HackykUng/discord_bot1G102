import discord
import os
import aiohttp
import asyncio
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True

client = discord.Client(intents=intents)

# เก็บเวลาที่ user เข้า VC  { user_id: datetime }
vc_join_times = {}

def format_duration(seconds: float) -> str:
    """แปลงวินาทีเป็นรูปแบบที่อ่านได้ง่าย"""
    total_seconds = int(seconds)
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60

    parts = []
    if days > 0:
        parts.append(f"{days} วัน")
    if hours > 0:
        parts.append(f"{hours} ชั่วโมง")
    if minutes > 0:
        parts.append(f"{minutes} นาที")
    if secs > 0 or not parts:
        parts.append(f"{secs} วินาที")

    return " ".join(parts)

def get_tier(seconds: float) -> dict:
    """คำนวณ Tier จากเวลาใน VC"""
    minutes = seconds / 60

    if minutes < 5:
        return {"tier": "🪨 Tier F", "color": 0x95a5a6, "desc": "แค่แวบเข้ามา!"}
    elif minutes < 30:
        return {"tier": "🥉 Tier C", "color": 0xcd7f32, "desc": "เริ่มต้นได้ดี"}
    elif minutes < 60:
        return {"tier": "🥈 Tier B", "color": 0xC0C0C0, "desc": "ใช้เวลาพอสมควร"}
    elif minutes < 180:
        return {"tier": "🥇 Tier A", "color": 0xFFD700, "desc": "อยู่นานมาก!"}
    elif minutes < 360:
        return {"tier": "💎 Tier S", "color": 0x00bfff, "desc": "เซียน VC!"}
    else:
        return {"tier": "👑 Tier SS", "color": 0xff69b4, "desc": "ตำนานแห่ง VC!!"}

async def send_webhook(user: discord.Member, channel_name: str, duration_seconds: float, join_time: datetime, leave_time: datetime):
    """ส่งข้อมูลไปยัง Discord Webhook"""
    tier_info = get_tier(duration_seconds)
    duration_text = format_duration(duration_seconds)

    join_str = join_time.strftime("%d/%m/%Y %H:%M:%S")
    leave_str = leave_time.strftime("%d/%m/%Y %H:%M:%S")

    embed = {
        "title": f"{tier_info['tier']}  —  {user.display_name}",
        "description": tier_info["desc"],
        "color": tier_info["color"],
        "thumbnail": {"url": str(user.display_avatar.url)},
        "fields": [
            {"name": "👤 ผู้ใช้", "value": f"{user.mention} (`{user}`)", "inline": True},
            {"name": "🔊 ห้อง VC", "value": channel_name, "inline": True},
            {"name": "⏱️ ระยะเวลา", "value": f"**{duration_text}**", "inline": False},
            {"name": "🟢 เข้า VC", "value": join_str, "inline": True},
            {"name": "🔴 ออก VC", "value": leave_str, "inline": True},
        ],
        "footer": {"text": "VC Tier Tracker • Discord Bot"},
        "timestamp": leave_time.isoformat(),
    }

    payload = {"embeds": [embed]}

    async with aiohttp.ClientSession() as session:
        async with session.post(WEBHOOK_URL, json=payload) as resp:
            if resp.status not in (200, 204):
                print(f"[ERROR] Webhook failed: {resp.status} - {await resp.text()}")
            else:
                print(f"[OK] Sent webhook for {user} | {duration_text} | {tier_info['tier']}")

@client.event
async def on_ready():
    print(f"✅ Bot พร้อมใช้งาน: {client.user} (ID: {client.user.id})")

@client.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    user_id = member.id

    # เข้า VC (ไม่ได้อยู่ใน VC มาก่อน → เข้าห้องใหม่)
    if before.channel is None and after.channel is not None:
        vc_join_times[user_id] = datetime.now(timezone.utc)
        print(f"[JOIN] {member} เข้า {after.channel.name}")

    # ออก VC (อยู่ใน VC → ออกจากทุกห้อง)
    elif before.channel is not None and after.channel is None:
        join_time = vc_join_times.pop(user_id, None)
        if join_time:
            leave_time = datetime.now(timezone.utc)
            duration = (leave_time - join_time).total_seconds()
            channel_name = before.channel.name
            print(f"[LEAVE] {member} ออก {channel_name} | {format_duration(duration)}")
            asyncio.create_task(
                send_webhook(member, channel_name, duration, join_time, leave_time)
            )

client.run(TOKEN)
