# ═══════════════════════════════════════════════════════════════
#              ★ PREMIUM TCP BOT — BY RAFIN TxT ★
#              ▌ Render.com Ready Edition ▌
# ═══════════════════════════════════════════════════════════════

import asyncio
import os
import time
import sys

from aiohttp import web

try:
    from cfonts import render
    HAS_CFONTS = True
except Exception:
    HAS_CFONTS = False

import login_engine
import bot_core


# ═══════════════════════════════════════════════════════════════
#                    ★ কনফিগ (Env Variable থেকে) ★
# ═══════════════════════════════════════════════════════════════

FF_UID    = os.environ.get("FF_UID", "8240708002")
FF_PW     = os.environ.get("FF_PW",  "048CDA2F8FEEB4D8B641F16BEFC789DB8B556681EFA6BB0635DF6BC71883F7CB")
FF_REGION = os.environ.get("FF_REGION", "IND")
HTTP_PORT = int(os.environ.get("PORT", "10000"))


# ═══════════════════════════════════════════════════════════════
#                    ★ প্রিমিয়াম ডিজাইন ★
# ═══════════════════════════════════════════════════════════════

def print_banner():
    print("\n" + "═" * 70)
    if HAS_CFONTS:
        try:
            print(render('RAFIN TxT', colors=['red', 'yellow'], align='center'))
            print(render('PREMIUM TCP BOT', colors=['cyan', 'magenta'], align='center'))
        except Exception:
            print("        ★  R A F I N   T x T  ★")
            print("        ★  PREMIUM TCP BOT  ★")
    else:
        print("        ★  R A F I N   T x T  ★")
        print("        ★  PREMIUM TCP BOT  ★")
    print("        ▌ Developed & Powered by RAFIN TxT ▌")
    print("═" * 70 + "\n")


def print_line(title, value, icon="➤"):
    print(f"  {icon}  \033[1;36m{title:<14}\033[0m : \033[1;33m{value}\033[0m")


def print_box(title, lines, color="\033[1;35m"):
    width = 60
    print(f"\n{color}┌{'─' * width}┐\033[0m")
    print(f"{color}│\033[0m  \033[1;33m{title.center(width - 2)}\033[0m {color}│\033[0m")
    print(f"{color}├{'─' * width}┤\033[0m")
    for line in lines:
        print(f"{color}│\033[0m  {line:<{width - 2}} {color}│\033[0m")
    print(f"{color}└{'─' * width}┘\033[0m\n")


def log(level, message):
    icons = {
        "INFO":  ("\033[1;36m",  "ℹ"),
        "OK":    ("\033[1;32m",  "✔"),
        "WAIT":  ("\033[1;33m",  "⏳"),
        "WARN":  ("\033[1;33m",  "⚠"),
        "ERROR": ("\033[1;31m",  "✘"),
        "BOT":   ("\033[1;35m",  "★"),
        "NET":   ("\033[1;36m",  "⇄"),
    }
    color, icon = icons.get(level, ("\033[1;37m", "•"))
    ts = time.strftime("%H:%M:%S")
    print(f"\033[1;90m[{ts}]\033[0m {color}{icon} {level:<5}\033[0m │ {message}")


# ═══════════════════════════════════════════════════════════════
#              ★ Render.com Health Check Server ★
# ═══════════════════════════════════════════════════════════════

BOT_STATUS = {"online": False, "uid": "-", "region": "-", "started": time.time()}


async def health_check(request):
    html = f"""
    <html>
    <head><title>RAFIN TxT Bot</title></head>
    <body style="background:#111;color:#0f0;font-family:monospace;padding:20px">
        <h1>★ RAFIN TxT — Free Fire Bot ★</h1>
        <p>Status : <b>{'🟢 ONLINE' if BOT_STATUS['online'] else '🔴 OFFLINE'}</b></p>
        <p>Bot UID : <b>{BOT_STATUS['uid']}</b></p>
        <p>Region  : <b>{BOT_STATUS['region']}</b></p>
        <p>Uptime  : <b>{int(time.time() - BOT_STATUS['started'])}s</b></p>
        <p>Powered by <b>RAFIN TxT</b></p>
    </body>
    </html>
    """
    return web.Response(text=html, content_type="text/html")


async def health_json(request):
    return web.json_response(BOT_STATUS)


async def start_web_server():
    app = web.Application()
    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_json)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", HTTP_PORT)
    await site.start()
    log("OK", f"Health server চালু → http://0.0.0.0:{HTTP_PORT}")


# ═══════════════════════════════════════════════════════════════
#                    ★ মূল প্রোগ্রাম ★
# ═══════════════════════════════════════════════════════════════

async def MaiiiinE():
    log("INFO", "লগইন প্রক্রিয়া শুরু হচ্ছে ...")
    log("INFO", f"লক্ষ্য অঞ্চল (Region) : {FF_REGION}")
    print()

    try:
        result = await login_engine.do_login(FF_UID, FF_PW, FF_REGION)
    except Exception as e:
        log("ERROR", f"লগইনের সময় সমস্যা : {e}")
        return

    if not result:
        log("ERROR", "লগইন ব্যর্থ — ১০ সেকেন্ড পর পুনরায় চেষ্টা ...")
        await asyncio.sleep(10)
        return

    bot_core.bot_uid = result["bot_uid"]
    bot_core.ToKen   = result["token"]
    bot_core.region  = result["region"]

    key         = result["key"]
    iv          = result["iv"]
    timestamp   = result["timestamp"]
    online_ip   = result["online_ip"]
    online_port = result["online_port"]
    chat_ip     = result["chat_ip"]
    chat_port   = result["chat_port"]
    acc_name    = result["account_name"]

    BOT_STATUS["online"] = True
    BOT_STATUS["uid"]    = result["bot_uid"]
    BOT_STATUS["region"] = result["region"]

    log("OK", "লগইন সফলভাবে সম্পন্ন !")
    print_box(
        "ACCOUNT INFORMATION — RAFIN TxT",
        [
            f"\033[1;37mUID\033[0m      : \033[1;32m{result['bot_uid']}\033[0m",
            f"\033[1;37mName\033[0m     : \033[1;32m{acc_name}\033[0m",
            f"\033[1;37mRegion\033[0m   : \033[1;32m{result['region']}\033[0m",
            f"\033[1;37mServer\033[0m   : \033[1;32m{online_ip}:{online_port}\033[0m",
            f"\033[1;37mChat\033[0m     : \033[1;32m{chat_ip}:{chat_port}\033[0m",
        ]
    )

    log("INFO", "অথেনটিকেশন টোকেন তৈরি হচ্ছে ...")
    ChatAutH      = bot_core.create_auth_token_chat(
        int(result["bot_uid"]), result["token"], int(timestamp), key, iv
    )
    OnlineAutH, _ = bot_core.build_ob55_online_auth(
        int(result["bot_uid"]), result["token"], int(timestamp), key, iv
    )
    log("OK", "অথেনটিকেশন টোকেন তৈরি সফল।")

    log("WAIT", "চ্যাট সার্ভারে সংযোগ স্থাপন ...")
    ready_event = asyncio.Event()
    t1 = asyncio.create_task(
        bot_core.TcPChaT(chat_ip, chat_port, ChatAutH, key, iv, ready_event, result["region"])
    )
    await ready_event.wait()
    log("OK", "চ্যাট সার্ভার সংযোগ সফল।")

    await asyncio.sleep(1)

    log("WAIT", "অনলাইন সার্ভারে সংযোগ স্থাপন ...")
    t2 = asyncio.create_task(
        bot_core.TcPOnLine(online_ip, online_port, key, iv, OnlineAutH)
    )

    print()
    print("═" * 70)
    if HAS_CFONTS:
        try:
            print(render('BOT ONLINE', colors=['green', 'cyan'], align='center'))
        except Exception:
            print("                    ★ BOT ONLINE ★")
    else:
        print("                    ★ BOT ONLINE ★")
    print("═" * 70)
    print_line("Owner",  "RAFIN TxT")
    print_line("Region", result["region"])
    print_line("Bot UID", result["bot_uid"])
    print_line("Name",   acc_name)
    print_line("Status", "\033[1;32m● RUNNING\033[0m")
    print("═" * 70)
    print(f"   \033[1;35m▌ সমস্ত সিস্টেম সচল — RAFIN TxT প্রিমিয়াম বট ▌\033[0m")
    print("═" * 70 + "\n")

    await asyncio.gather(t1, t2)


# ═══════════════════════════════════════════════════════════════
#              ★ অটো-রিস্টার্ট লুপ (প্রতি ৭ ঘণ্টায়) ★
# ═══════════════════════════════════════════════════════════════

async def StarTinG():
    attempt = 0
    while True:
        attempt += 1
        try:
            log("BOT", f"সেশন #{attempt} শুরু হচ্ছে — RAFIN TxT")
            await asyncio.wait_for(MaiiiinE(), timeout=7 * 60 * 60)
        except asyncio.TimeoutError:
            log("WARN", "টোকেনের সময় শেষ — পুনরায় চালু ...")
            BOT_STATUS["online"] = False
            await asyncio.sleep(3)
        except KeyboardInterrupt:
            log("WARN", "ব্যবহারকারী দ্বারা বন্ধ। বিদায় !")
            sys.exit(0)
        except Exception as e:
            log("ERROR", f"সমস্যা : {e} → ৫ সেকেন্ড পর পুনরায় ...")
            BOT_STATUS["online"] = False
            await asyncio.sleep(5)


# ═══════════════════════════════════════════════════════════════
#                       ★ এন্ট্রি পয়েন্ট ★
# ═══════════════════════════════════════════════════════════════

async def main_with_web():
    print_banner()
    log("BOT", "RAFIN TxT — Render.com Edition চালু হচ্ছে ...")
    await start_web_server()
    await StarTinG()


if __name__ == "__main__":
    try:
        asyncio.run(main_with_web())
    except KeyboardInterrupt:
        print("\n\033[1;31m▌ বট বন্ধ — RAFIN TxT ▌\033[0m\n")