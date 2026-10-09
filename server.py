"""
Bank Payment Slip Scanner - Complete Server & API
គាំទ្រការស្គែន slip ធនាគារគ្រប់ប្រភេទ (ACLEDA, ABA, Bakong, Wing, Canadia, TrueMoney, etc.)
"""

import os
import sys
import json
import io
import base64
import cv2
import dotenv
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image

# Force UTF-8 encoding on Windows console
if sys.platform == "win32":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

# Load environment variables (.env)
dotenv.load_dotenv()

# Check dependencies
try:
    # pyrefly: ignore [missing-import]
    from pyzbar.pyzbar import decode as pyzbar_decode
    PYZBAR_AVAILABLE = True
except ImportError:
    PYZBAR_AVAILABLE = False

try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class BankSlipScanner:
    """Class សម្រាប់ស្គែន និងស្រង់ទិន្នន័យពីបង្កាន់ដៃផ្ទេរប្រាក់ (Bank Slip)"""
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI-API-KEY")
        if self.api_key and GEMINI_AVAILABLE:
            print("✨ Gemini AI Vision ដំណើរការរួចរាល់...")
            self.client = genai.Client(api_key=self.api_key)
        else:
            print("⚠️ មិនមាន GEMINI_API_KEY ត្រឹមត្រូវទេក្នុង .env")
            self.client = None

    def scan_qr_code(self, img_pil):
        """ស្គែន QR Code / KHQR (Bakong) ពីលើ Slip"""
        try:
            if PYZBAR_AVAILABLE:
                decoded = pyzbar_decode(img_pil)
                for obj in decoded:
                    return {
                        "qr_data": obj.data.decode('utf-8', errors='ignore'),
                        "qr_found": True
                    }
        except Exception:
            pass

        # Fallback ស្គែនតាម OpenCV
        try:
            import numpy as np
            cv_img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
            qr_detector = cv2.QRCodeDetector()
            data, bbox, _ = qr_detector.detectAndDecode(cv_img)
            if data:
                return {"qr_data": data, "qr_found": True}
        except Exception:
            pass

        return {"qr_data": None, "qr_found": False}

    def extract_with_gemini(self, img_pil: Image.Image) -> dict:
        """ប្រើ Gemini AI Vision ដើម្បីស្រង់ទិន្នន័យ Slip បានយ៉ាងសុក្រឹតបំផុត"""
        if not self.client:
            return None

        prompt = """
        You are an expert OCR & Document Analyzer for Cambodian Bank Payment Slips (បង្កាន់ដៃផ្ទេរប្រាក់).
        Analyze this bank transfer slip (e.g. ACLEDA Bank, ABA Bank, Bakong, Wing, Canadia, TrueMoney, etc.) carefully.
        
        Extract the following fields accurately and return ONLY valid JSON:
        {
            "bank_name": "ឈ្មោះធនាគារ (e.g. ACLEDA Bank, ABA Bank, Bakong, Wing, etc.)",
            "transaction_type": "ប្រភេទប្រតិបត្តិការ (e.g. ប្រតិបត្តិការ QR, ផ្ទេរប្រាក់)",
            "amount": "ចំនួនទឹកប្រាក់ជាលេខ (e.g. 56,500 ឬ 10.00)",
            "currency": "KHR ឬ USD",
            "sender_name": "ឈ្មោះអ្នកផ្ញើ / គណនីកាត់ប្រាក់",
            "sender_account": "លេខគណនី ឬលេខទូរស័ព្ទអ្នកផ្ញើ",
            "receiver_name": "ឈ្មោះអ្នកទទួលប្រាក់",
            "receiver_account": "លេខគណនី ឬលេខទូរស័ព្ទអ្នកទទួល",
            "transaction_id": "លេខយោង / លេខកូដប្រតិបត្តិការ (Reference / Trx ID)",
            "date": "កាលបរិច្ឆេទប្រតិបត្តិការ",
            "time": "ពេលវេលាប្រតិបត្តិការ"
        }
        Return ONLY valid JSON without markdown wrapping or backticks.
        """

        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[img_pil, prompt]
            )
            text_resp = response.text.strip()

            # Clean markdown formatting if present
            if text_resp.startswith("```json"):
                text_resp = text_resp[7:]
            if text_resp.startswith("```"):
                text_resp = text_resp[3:]
            if text_resp.endswith("```"):
                text_resp = text_resp[:-3]

            return json.loads(text_resp.strip())
        except Exception as e:
            print(f"⚠️ Gemini Vision Error: {e}")
            return None

    def scan_image(self, img_pil: Image.Image) -> dict:
        """Process slip image from PIL Image"""
        qr_info = self.scan_qr_code(img_pil)
        
        # Extract via AI
        data = self.extract_with_gemini(img_pil)
        if not data:
            data = {
                "bank_name": "Unknown",
                "transaction_type": None,
                "amount": None,
                "currency": None,
                "sender_name": None,
                "sender_account": None,
                "receiver_name": None,
                "receiver_account": None,
                "transaction_id": None,
                "date": None,
                "time": None
            }
        
        data.update(qr_info)
        return data

    def scan_file_path(self, file_path: str) -> dict:
        """Process slip image from local file path"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"រកមិនឃើញរូបភាព: {file_path}")
        img_pil = Image.open(file_path)
        return self.scan_image(img_pil)


# ----------------------------------------------------
# Flask REST API Server Setup
# ----------------------------------------------------
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)
scanner = BankSlipScanner()


@app.route("/", methods=["GET"])
def index():
    """Route មេសម្រាប់បង្ហាញ UI index.html"""
    index_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
    if os.path.exists(index_path):
        return send_file(index_path)
    return jsonify({
        "message": "Bank Slip Scanner API Server is running.",
        "api_endpoint": "POST /api/scan-slip"
    })


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "online",
        "gemini_ready": bool(scanner.client),
        "pyzbar_ready": PYZBAR_AVAILABLE
    })


@app.route("/api/scan-slip", methods=["POST"])
def api_scan_slip():
    """
    API Endpoint មេសម្រាប់ទទួលរូបភាព Slip មកស្គែន
    គាំទ្រ:
      1. multipart/form-data (key: file, image, ឬ slip)
      2. application/json (key: image_base64)
    """
    img_pil = None

    # ១. ទទួលជា File Upload (Form Data)
    if 'file' in request.files:
        img_pil = Image.open(request.files['file'].stream)
    elif 'image' in request.files:
        img_pil = Image.open(request.files['image'].stream)
    elif 'slip' in request.files:
        img_pil = Image.open(request.files['slip'].stream)

    # ២. ទទួលជា Base64 JSON
    elif request.is_json:
        req_data = request.get_json()
        if 'image_base64' in req_data:
            base64_str = req_data['image_base64']
            if ',' in base64_str:
                base64_str = base64_str.split(',')[1]
            img_bytes = base64.b64decode(base64_str)
            img_pil = Image.open(io.BytesIO(img_bytes))

    if img_pil is None:
        return jsonify({
            "success": False,
            "error": "សូមផ្ញើរូបភាពតាមរយៈ 'file' (form-data) ឬ 'image_base64' (JSON)"
        }), 400

    try:
        # ដំណើរការស្គែន
        result = scanner.scan_image(img_pil)
        return jsonify({
            "success": True,
            "data": result
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ----------------------------------------------------
# Main Execution Entry
# ----------------------------------------------------
if __name__ == "__main__":
    # បើដំណើរការ command ជាមួយ argument រូបភាព (e.g. python server.py slip.jpg)
    if len(sys.argv) > 1 and sys.argv[1].lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp')):
        image_path = sys.argv[1]
        print(f"📸 កំពុងស្គែនរូបភាព: {image_path}")
        res = scanner.scan_file_path(image_path)
        print("\n" + "=" * 60)
        print(" 📋 លទ្ធផលស្គែន (Extracted Slip Details)")
        print("=" * 60)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        print("=" * 60)
    else:
        # ដំណើរការ Server API
        port = int(os.getenv("PORT", 5000))
        print("=" * 60)
        print(f" 🚀 Bank Slip Scanner API Server ដំណើរការលើ http://localhost:{port}")
        print(f" 📖 API Endpoint: POST http://localhost:{port}/api/scan-slip")
        print("=" * 60)
        app.run(host="0.0.0.0", port=port, debug=False)
