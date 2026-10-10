# 🚀 Bank Slip Scanner & REST API (ប្រព័ន្ធស្គែនបង្កាន់ដៃផ្ទេរប្រាក់)

ប្រព័ន្ធស្គែន និងស្រង់ទិន្នន័យពីបង្កាន់ដៃផ្ទេរប្រាក់ (Bank Payment Slip) គ្រប់ធនាគារនៅកម្ពុជា (ACLEDA, ABA, Bakong, Wing, Canadia, TrueMoney...) ដោយប្រើប្រាស់ **Google Gemini AI Vision** និង **QR Code Decoder (PyZbar)**។

---

## 📚 មាតិកា (Table of Contents)
1. [លក្ខណៈពិសេស (Features)](#-លក្ខណៈពិសេស-features)
2. [ការដំឡើង និងរៀបចំ (Installation & Setup)](#️-ការដំឡើង-និងរៀបចំ-installation--setup)
3. [របៀបដំណើរការ Server (Running Server)](#-របៀបដំណើរការ-server)
4. [សេចក្ដីលម្អិតនៃ API និមួយៗ (API Endpoints & Specifications)](#-សេចក្ដីលម្អិតនៃ-api-និមួយៗ-api-endpoints--specifications)
   - [១. Endpoint: GET / (Web Test Interface)](#១-endpoint-get---web-test-interface)
   - [២. Endpoint: GET /api/health (Health Check)](#២-endpoint-get-apihealth-health-check)
   - [៣. Endpoint: POST /api/scan-slip (Scan Slip API)](#៣-endpoint-post-apiscan-slip-core-api)
5. [ឧទាហរណ៍នៃការហៅប្រើ (Code Examples)](#-ឧទាហរណ៍នៃការហៅប្រើ-code-examples)

---

## ✨ លក្ខណៈពិសេស (Features)
- 🔍 **ស្គែនបង្កាន់ដៃគ្រប់ធនាគារ**: ស្រង់ទិន្នន័យ (ឈ្មោះធនាគារ, ចំនួនទឹកប្រាក់, អ្នកផ្ញើ, អ្នកទទួល, លេខយោង, កាលបរិច្ឆេទ) ជាភាសាខ្មែរ និងអង់គ្លេសបានត្រឹមត្រូវ ១០០%
- 🔲 **ស្គែន QR Code / KHQR (Bakong)** ពីលើ Slip ដោយស្វ័យប្រវត្តិ
- ⚡ **REST API Server**: ផ្ដល់នូវ API Endpoint សម្រាប់ភ្ជាប់ជាមួយ Website, Mobile App (Flutter, React Native, iOS, Android) ឬ Telegram Bot
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

## ▶️ របៀបដំណើរការ Server

```bash
python server.py
```
- Web UI: `http://localhost:5000`
- API Base URL: `http://localhost:5000/api`

---

## 📖 សេចក្ដីលម្អិតនៃ API និមួយៗ (API Endpoints & Specifications)

---

### ១. Endpoint: `GET /` - Web Test Interface

#### 🎯 ប្រើសម្រាប់ធ្វើអ្វី?
- ប្រើសម្រាប់បើកផ្ទាំងកម្មវិធី **Web Interface (UI)** លើ Browser ដើម្បីឱ្យអ្នកប្រើប្រាស់អាច **អូសទម្លាក់រូបភាព (Drag & Drop)** ឬចុចជ្រើសរើសរូបភាព Slip មកស្គែនតេស្តមើលលទ្ធផលផ្ទាល់ភ្លាមៗ។

#### 📥 តម្រូវការ Request (Request Requirements)
- **Method**: `GET`
- **URL**: `http://localhost:5000/`
- **Headers**: មិនត្រូវការ
- **Body / Params**: គ្មាន (None)

#### 📤 ទិន្នន័យត្រឡប់មកវិញ (Response)
- **Content-Type**: `text/html`
- បង្ហាញទំព័រ `index.html` លើ Browser។

---

### ២. Endpoint: `GET /api/health` - Health Check

#### 🎯 ប្រើសម្រាប់ធ្វើអ្វី?
- ប្រើសម្រាប់ **ពិនិត្យមើលស្ថានភាពរបស់ Server (Status)** ថា Server កំពុង Online ឬអត់
- ពិនិត្យមើលថាតើ `GEMINI_API_KEY` ត្រូវបានកំណត់ត្រឹមត្រូវដែរឬទេ (`gemini_ready`)
- ពិនិត្យមើលថាតើ Library ស្គែន QR Code ដំណើរការរួចរាល់ដែរឬទេ (`pyzbar_ready`)។

#### 📥 តម្រូវការ Request (Request Requirements)
- **Method**: `GET`
- **URL**: `http://localhost:5000/api/health`
- **Headers**: មិនត្រូវការ
- **Body / Params**: គ្មាន (None)

#### 📤 ទិន្នន័យត្រឡប់មកវិញ (Response)
- **Status Code**: `200 OK`
- **Content-Type**: `application/json`

```json
{
  "status": "online",
  "gemini_ready": true,
  "pyzbar_ready": true
}
```

---

### ៣. Endpoint: `POST /api/scan-slip` - Core API

#### 🎯 ប្រើសម្រាប់ធ្វើអ្វី?
- ជា **API Endpoint ស្នូល** សម្រាប់ទទួលរូបភាពវិក្កយបត្រ/បង្កាន់ដៃផ្ទេរប្រាក់ (Slip) ពីប្រព័ន្ធផ្សេងៗ (Website, App, Telegram Bot, POS)
- AI នឹងវិភាគ និងស្រង់ទិន្នន័យចេញពី Slip ទាំងអស់ រួមទាំងស្គែន QR Code រួចផ្ដល់ទិន្នន័យមកវិញជាទម្រង់ **JSON**។

#### 📥 តម្រូវការ Request (Request Requirements)
លោកអ្នកអាចជ្រើសរើសផ្ញើរូបភាពតាម **ជម្រើសមួយក្នុងចំណោម ២ ខាងក្រោម**៖

##### ជម្រើសទី ១៖ ផ្ញើជា File Upload (Form-Data) — *ណែនាំឱ្យប្រើ*
- **Method**: `POST`
- **Header**: `Content-Type: multipart/form-data`
- **Body (Form-Data Key)**:
  - `file` (ឬ `image` ឬ `slip`) : File រូបភាព Slip (JPG, PNG, WEBP, BMP...)

##### ជម្រើសទី ២៖ ផ្ញើជា Base64 JSON
- **Method**: `POST`
- **Header**: `Content-Type: application/json`
- **Body (JSON)**:
  ```json
  {
    "image_base64": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQ..."
  }
  ```

---

#### 📤 ទិន្នន័យត្រឡប់មកវិញ (Response Output)

##### ✅ ករណីជោគជ័យ (`200 OK`):
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

##### 📋 ការពន្យល់អត្ថន័យនៃ Field និមួយៗ (Field Descriptions):
| Field ក្នុង JSON | ប្រភេទ (Type) | ការពន្យល់ (Description) |
| :--- | :--- | :--- |
| `success` | `boolean` | `true` ប្រសិនបើស្គែនជោគជ័យ, `false` បើបរាជ័យ |
| `bank_name` | `string` | ឈ្មោះធនាគារ (ឧ. ACLEDA Bank, ABA Bank, Bakong, Wing, Canadia...) |
| `transaction_type` | `string` | ប្រភេទប្រតិបត្តិការ (ឧ. ប្រតិបត្តិការ QR, ផ្ទេរប្រាក់...) |
| `amount` | `string` | ចំនួនទឹកប្រាក់ដែលបានផ្ទេរ (ឧ. `56,500` ឬ `10.00`) |
| `currency` | `string` | រូបិយប័ណ្ណ (`KHR` សម្រាប់រៀល ឬ `USD` សម្រាប់ដុល្លារ) |
| `sender_name` | `string` | ឈ្មោះអ្នកផ្ញើ ឬគណនីកាត់ប្រាក់ចេញ |
| `sender_account` | `string` | លេខគណនី ឬលេខទូរស័ព្ទរបស់អ្នកផ្ញើ |
| `receiver_name` | `string` | ឈ្មោះអ្នកទទួលប្រាក់ |
| `receiver_account` | `string` | លេខគណនី ឬលេខទូរស័ព្ទរបស់អ្នកទទួលប្រាក់ |
| `transaction_id` | `string` | លេខយោង ឬលេខកូដប្រតិបត្តិការ (Trx ID / Ref No) |
| `date` | `string` | កាលបរិច្ឆេទនៃប្រតិបត្តិការ |
| `time` | `string` | ពេលវេលានៃប្រតិបត្តិការ |
| `qr_data` | `string / null` | ទិន្នន័យជាអក្សរក្នុង QR Code (Bakong / KHQR) |
| `qr_found` | `boolean` | `true` បើស្គែនឃើញ QR Code លើ Slip |

##### ❌ ករណី Error (`400 Bad Request` ឬ `500 Internal Server Error`):
```json
{
  "success": false,
  "error": "សារពន្យល់ពីបញ្ហា (ឧ. មិនមានរូបភាពផ្ញើមកទេ ឬ API Key មិនត្រឹមត្រូវ)"
}
```

---

## 💻 ឧទាហរណ៍នៃការហៅប្រើ (Code Examples)

### ១. ហៅប្រើតាម cURL
```bash
curl -X POST "http://localhost:5000/api/scan-slip" -F "file=@slip.jpg"
```

### ២. ហៅប្រើតាម JavaScript / TypeScript (Fetch API)
```javascript
async function scanBankSlip(file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('http://localhost:5000/api/scan-slip', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    if (result.success) {
        console.log("ធនាគារ:", result.data.bank_name);
        console.log("ទឹកប្រាក់:", result.data.amount, result.data.currency);
        console.log("លេខយោង:", result.data.transaction_id);
    } else {
        console.error("Error:", result.error);
    }
}
```

### ៣. ហៅប្រើតាម Python (requests)
```python
import requests

def scan_slip(image_path):
    url = "http://localhost:5000/api/scan-slip"
    with open(image_path, 'rb') as img_file:
        files = {'file': img_file}
        response = requests.post(url, files=files)
        return response.json()

# ហៅប្រើ
result = scan_slip("slip.jpg")
print(result)
```

---

## 🔒 Security
- ឯកសារ `.env` ត្រូវបានការពារដោយ `.gitignore` មិនឱ្យ push ឡើង GitHub ជាដាច់ខាត ដើម្បីសុវត្ថិភាព API Key។
