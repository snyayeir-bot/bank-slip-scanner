# 🚀 Bank Slip Scanner & REST API (ប្រព័ន្ធស្គែនបង្កាន់ដៃផ្ទេរប្រាក់)

ប្រព័ន្ធស្គែន និងស្រង់ទិន្នន័យពីបង្កាន់ដៃផ្ទេរប្រាក់ (Bank Payment Slip) គ្រប់ធនាគារនៅកម្ពុជា (ACLEDA, ABA, Bakong, Wing, Canadia, TrueMoney...) ដោយប្រើប្រាស់ **Google Gemini AI Vision** និង **QR Code Decoder (PyZbar)**។

---

## ✨ លក្ខណៈពិសេស (Features)
- 🔍 **ស្គែនបង្កាន់ដៃគ្រប់ធនាគារ**: ស្រង់ទិន្នន័យ (ឈ្មោះធនាគារ, ចំនួនទឹកប្រាក់, អ្នកផ្ញើ, អ្នកទទួល, លេខយោង, កាលបរិច្ឆេទ) ជាភាសាខ្មែរ និងអង់គ្លេសបានត្រឹមត្រូវ ១០០%
- 🔲 **ស្គែន QR Code / KHQR (Bakong)** ពីលើ Slip ដោយស្វ័យប្រវត្តិ
- ⚡ **REST API Server**: ផ្ដល់នូវ API Endpoint `POST /api/scan-slip` សម្រាប់ភ្ជាប់ជាមួយ Website, Mobile App ឬ Telegram Bot
- 🎨 **Web Interface**: មានផ្ទាំង UI `index.html` ស្រស់ស្អាតសម្រាប់ទម្លាក់រូបភាពស្គែនតេស្តភ្លាមៗ

---

## 🛠️ ការដំឡើង និងរៀបចំ (Installation & Setup)

### ១. Clone Repository
```bash
git clone https://github.com/snyayeir-bot/bank-slip-scanner.git
cd bank-slip-scanner
```

### ២. ដំឡើង Dependencies
```bash
pip install -r requirements.txt
```

### ៣. កំណត់ Environment Variables (.env)
បង្កើតឯកសារឈ្មោះ `.env` (ឬចម្លងពី `.env.example`) រួចដាក់ Gemini API Key របស់អ្នក៖
```env
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
PORT=5000
```

---

## 🚀 របៀបប្រើប្រាស់ (Usage Guide)

### របៀបទី ១៖ ដំណើរការ Web UI & API Server
```bash
python server.py
```
- បើក Browser ចូលទៅកាន់ 👉 **http://localhost:5000**
- អ្នកអាច **អូសទម្លាក់រូបភាព (Drag & Drop)** ឬចុច Upload ដើម្បីស្គែនភ្លាមៗ។

---

### របៀបទី ២៖ ស្គែនផ្ទាល់តាម Terminal (CLI Mode)
អ្នកអាចស្គែនរូបភាពបានភ្លាមៗដោយគ្រាន់តែបញ្ជាក់ path រូបភាព៖
```bash
python server.py path/to/your_slip.jpg
```

---

## 📖 ឯកសារ API Documentation

### **Endpoint**: `POST /api/scan-slip`
គាំទ្រការផ្ញើរូបភាពតាមរយៈ **Form-Data (File)** ឬ **JSON (Base64)**។

#### ១. ហៅប្រើតាម cURL / Postman
```bash
curl -X POST "http://localhost:5000/api/scan-slip" -F "file=@slip.jpg"
```

#### ២. ហៅប្រើតាម JavaScript / Fetch
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const res = await fetch('http://localhost:5000/api/scan-slip', {
    method: 'POST',
    body: formData
});
const data = await res.json();
console.log(data);
```

#### ៣. ហៅប្រើតាម Python (requests)
```python
import requests

url = "http://localhost:5000/api/scan-slip"
files = {'file': open('slip.jpg', 'rb')}

response = requests.post(url, files=files)
print(response.json())
```

---

### 📋 ទម្រង់ JSON Response ដែលទទួលបាន៖

```json
{
  "success": true,
  "data": {
    "bank_name": "ACLEDA Bank",
    "transaction_type": "ប្រតិបត្តិការ QR",
    "amount": "56,500",
    "currency": "KHR",
    "sender_name": "Rin Sopha Rath",
    "sender_account": "348***518",
    "receiver_name": "YAI SORNYA",
    "receiver_account": "097 881 0715",
    "transaction_id": "62805320857",
    "date": "07 October 2026",
    "time": "05:55 PM",
    "qr_data": null,
    "qr_found": false
  }
}
```

---

## 🔒 Security
- ឯកសារ `.env` ត្រូវបានការពារដោយ `.gitignore` មិនឱ្យ push ឡើង GitHub ជាដាច់ខាត ដើម្បីសុវត្ថិភាព API Key។
