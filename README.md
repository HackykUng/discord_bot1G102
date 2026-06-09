# 🎙️ Discord VC Tier Tracker Bot

บอทบันทึกระยะเวลาการเข้า Voice Channel และจัด **Tier** พร้อมส่งผลผ่าน Webhook

---

## 📁 โครงสร้างโปรเจกต์

```
discord-vc-bot/
├── bot.py              ← โค้ดหลัก
├── requirements.txt    ← library ที่ต้องใช้
├── .env.example        ← ตัวอย่างไฟล์ .env
├── .env                ← (สร้างเอง, ห้าม push!)
├── .gitignore          ← ป้องกัน .env หลุด GitHub
└── README.md
```

---

## 🏆 ระบบ Tier

| Tier | เวลาใน VC |
|------|-----------|
| 🪨 Tier F | น้อยกว่า 5 นาที |
| 🥉 Tier C | 5 – 30 นาที |
| 🥈 Tier B | 30 – 60 นาที |
| 🥇 Tier A | 1 – 3 ชั่วโมง |
| 💎 Tier S | 3 – 6 ชั่วโมง |
| 👑 Tier SS | มากกว่า 6 ชั่วโมง |

---

## 🚀 วิธีติดตั้งและรัน (Local)

### 1. สร้าง Discord Bot

1. ไปที่ [Discord Developer Portal](https://discord.com/developers/applications)
2. คลิก **New Application** → ตั้งชื่อ
3. ไปที่แท็บ **Bot** → คลิก **Reset Token** → คัดลอก Token
4. เปิด Intents: ✅ **SERVER MEMBERS INTENT** และ ✅ **VOICE STATE INTENT**
5. ไปที่ **OAuth2 → URL Generator**:
   - Scopes: `bot`
   - Bot Permissions: `View Channels`, `Connect`
6. คัดลอก URL แล้วเปิดในเบราว์เซอร์เพื่อเชิญบอทเข้า Server

### 2. สร้าง Webhook

1. ไปที่ Channel ที่ต้องการรับการแจ้งเตือน
2. **Edit Channel → Integrations → Webhooks → New Webhook**
3. คัดลอก Webhook URL

### 3. ตั้งค่าไฟล์ .env

```bash
cp .env.example .env
```

แก้ไขไฟล์ `.env`:

```env
DISCORD_TOKEN=MTxxxxxxxxxxxxxxxxxxxxxxxx.Gxxxxx.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/1234567890/abcdefghijklmnop
```

### 4. ติดตั้ง Library และรัน

```bash
pip install -r requirements.txt
python bot.py
```

---

## ☁️ Deploy บน Render.com

### วิธีซ่อน TOKEN และ WEBHOOK บน Render (สำคัญมาก!)

**ไม่ต้อง** อัปโหลดไฟล์ `.env` ขึ้น GitHub เลย  
ให้ใส่ค่าในหน้า **Environment Variables** ของ Render แทน

---

### ขั้นตอน Deploy

**ขั้นที่ 1 – Push โค้ดขึ้น GitHub**

```bash
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/discord-vc-bot.git
git push -u origin main
```

> ⚠️ ตรวจสอบว่า **ไม่มีไฟล์ `.env`** ใน commit (ดู `.gitignore`)

---

**ขั้นที่ 2 – สร้าง Service บน Render**

1. ไปที่ [render.com](https://dashboard.render.com) → **New → Web Service** (หรือ **Background Worker**)
2. เชื่อมต่อ GitHub Repository
3. ตั้งค่าดังนี้:

| ฟิลด์ | ค่า |
|-------|-----|
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python bot.py` |

---

**ขั้นที่ 3 – ใส่ Environment Variables บน Render**

> นี่คือวิธีซ่อน Token ที่ปลอดภัยที่สุด — ไม่มีใครเห็นได้นอกจากคุณ

1. ไปที่แท็บ **Environment** ในหน้า Service
2. คลิก **Add Environment Variable** แล้วเพิ่ม 2 ตัว:

```
Key: DISCORD_TOKEN
Value: (วาง Token ของบอทที่นี่)

Key: DISCORD_WEBHOOK_URL  
Value: (วาง Webhook URL ที่นี่)
```

3. คลิก **Save Changes** → Render จะ Redeploy อัตโนมัติ

---

**ขั้นที่ 4 – เปลี่ยน Plan เป็น Background Worker**

บอทไม่ต้องการ HTTP Port → ใช้ **Background Worker** ประหยัดกว่า:
- ใน Render Dashboard เลือก **New → Background Worker** แทน Web Service
- ใช้ค่าเดิมทุกอย่าง

---

## 🔒 สรุปการซ่อน Token

| วิธี | ความปลอดภัย | คำอธิบาย |
|------|-------------|-----------|
| ✅ `.env` + `.gitignore` | ปลอดภัยสำหรับ Local | ไม่ push ขึ้น GitHub |
| ✅ Render Environment Variables | ปลอดภัยสำหรับ Production | ตั้งในหน้าเว็บ Render |
| ❌ เขียน Token ตรงในโค้ด | **อันตราย!** | ห้ามทำเด็ดขาด |
| ❌ Push ไฟล์ `.env` ขึ้น GitHub | **อันตราย!** | ทุกคนเห็น Token ได้ |

---

## 🆘 แก้ปัญหาเบื้องต้น

- **บอทไม่ตอบสนอง** → ตรวจสอบ Token และ Intents ใน Developer Portal
- **Webhook ไม่ส่ง** → ตรวจสอบ Webhook URL และสิทธิ์ Channel
- **Render หยุดทำงานหลัง 15 นาที** → เปลี่ยนจาก Web Service เป็น **Background Worker**
