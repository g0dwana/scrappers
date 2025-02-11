import json
import csv  # CSV modülünü ekledik
from datetime import datetime 

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # YYYYMMDD_HHMMSS formatı
file_name = f"output_{timestamp}.csv"

# JSON verisini bir dosyadan okuyorsanız, burada `data.json` dosyasının yolunu belirleyin.
file_path = r"C:\Users\eng\Desktop\Yeni klasör (3)\expolcuk.json"

# JSON dosyasını aç ve yükle
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Mesajları içeren kısma erişim
messages = data.get("data", {}).get("messages", [])

# Username ve content bilgilerini al
result = [
    {"username": message["sender"]["username"], "content": message["content"]}
    for message in messages
    if "sender" in message and "content" in message
]

# Çıktıyı yazdır
for entry in result:
    print(f"Username: {entry['username']}, Content: {entry['content']}")



with open(file_name, "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["username", "content"])
    writer.writeheader()
    writer.writerows(result)


print(f"Çıktı {file_name} dosyasına kaydedildi.")
