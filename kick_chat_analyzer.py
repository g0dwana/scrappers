import asyncio
import websockets
import json
from collections import defaultdict
from datetime import datetime, timedelta

# Kullanıcı mesajlarını saklamak için bir yapı
user_messages = defaultdict(list)

def log_event(event_type, details):
    """Olayları kaydetmek için"""
    with open("events_log.txt", "a") as f:
        f.write(f"[{datetime.now()}] {event_type}: {details}\n")
    print(f"{event_type}: {details}")

def process_message(username, content):
    """Mesajı işleyip spam kontrolü yapar"""
    now = datetime.now()
    user_messages[username].append((content, now))
    
    # Geçmiş mesajları temizle (örneğin, son 10 dakikayı dikkate alalım)
    user_messages[username] = [
        (msg, ts) for msg, ts in user_messages[username]
        if now - ts < timedelta(minutes=10)
    ]
    
    # Aynı mesajın tekrarını kontrol et
    repeated_messages = [msg for msg, ts in user_messages[username] if msg == content]
    if len(repeated_messages) > 3:  # 3'ten fazla tekrar spam sayılır
        log_event("Spam Detected", f"{username} - {content}")

async def handle_message(message):
    """Gelen mesajı işleyip uygun olayı tetikler"""
    try:
        data = json.loads(message)
        if "type" in data:
            if data["type"] == "ChatMessage":
                username = data["user"]["username"]
                content = data["content"]
                log_event("ChatMessage", f"{username}: {content}")
                process_message(username, content)
            elif data["type"] == "Subscription":
                username = data["user"]["username"]
                log_event("Subscription", f"Yeni abonelik: {username}")
            elif data["type"] == "GiftedSubscriptions":
                username = data["user"]["username"]
                log_event("GiftedSubscriptions", f"Hediye abonelik: {username}")
    except Exception as e:
        log_event("Error", f"Mesaj işlenemedi: {e}")

async def connect_to_kick(channel_name):
    """Kick sohbetine bağlanır ve mesajları işler"""
    websocket_url = f"wss://kick.com/api/chat/{expolcuk}"
    retry_attempts = 5
    delay_between_attempts = 5  # saniye

    for attempt in range(retry_attempts):
        try:
            async with websockets.connect(websocket_url) as ws:
                print(f"{channel_name} kanalına bağlanıldı.")
                while True:
                    try:
                        message = await ws.recv()
                        await handle_message(message)
                    except websockets.ConnectionClosed:
                        log_event("Warning", "Bağlantı kapandı, yeniden bağlanmayı deneyin.")
                        break
                    except Exception as e:
                        log_event("Error", f"Hata oluştu: {e}")
        except Exception as e:
            print(f"Bağlantı başarısız ({attempt + 1}/{retry_attempts}): {e}")
            if attempt < retry_attempts - 1:
                await asyncio.sleep(delay_between_attempts)
            else:
                log_event("Critical", "Maksimum deneme sayısına ulaşıldı, çıkılıyor.")
                return

def main():
    """Ana fonksiyon"""
    channel_name = "expolcuk"  # Buraya Kick kanal adınızı girin
    asyncio.run(connect_to_kick(channel_name))

if __name__ == "__main__":
    main()
