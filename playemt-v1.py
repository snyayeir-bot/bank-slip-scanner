"""
Bank Payment Slip Scanner (ស្គែនបង្កាន់ដៃផ្ទេរប្រាក់/Slip ធនាគារ)
គាំទ្រការស្គែន slip ធនាគារនៅកម្ពុជា (ACLEDA, ABA, Bakong, Wing, Canadia, TrueMoney, etc.)
"""

import os
import sys
import json
import io
import cv2
import dotenv

# Force UTF-8 for Windows console to handle Khmer unicode & emojis properly
if sys.platform == "win32":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

# Load .env file
dotenv.load_dotenv()


# Optional OCR / Vision engines
try:
    from PIL import Image
    # pyrefly: ignore [missing-import]
    from pyzbar.pyzbar import decode as pyzbar_decode
    PYZBAR_AVAILABLE = True
except ImportError:
    PYZBAR_AVAILABLE = False

try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class BankSlipScanner:
    def __init__(self, use_gemini: bool = True):
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI-API-KEY")
        self.use_gemini = use_gemini and GEMINI_AVAILABLE and bool(api_key)
        
        if self.use_gemini:
            print("✨ ប្រើប្រាស់ Gemini AI Vision សម្រាប់អាន Slip (គាំទ្រភាសាខ្មែរ & អង់គ្លេស 100%)...")
            self.ai_client = genai.Client(api_key=api_key)
        else:
            print("⚠️ មិនមាន GEMINI_API_KEY ទេ (សូមពិនិត្យមើលឯកសារ .env)")

    def scan_qr_code(self, img):
        """Scan QR code from slip (Bakong / KHQR / Bank QR)."""
        if PYZBAR_AVAILABLE:
            try:
                decoded_objs = pyzbar_decode(img)
                for obj in decoded_objs:
                    return {"qr_data": obj.data.decode('utf-8', errors='ignore'), "qr_found": True}
            except Exception:
                pass

        qr_detector = cv2.QRCodeDetector()
        data, bbox, _ = qr_detector.detectAndDecode(img)
        if data:
            return {"qr_data": data, "qr_found": True}
        return {"qr_data": None, "qr_found": False}

    def extract_with_gemini(self, image_path: str) -> dict:
        """Extract structured slip details using Gemini AI Vision with high precision for Cambodian banks."""
        try:
            from PIL import Image
            img = Image.open(image_path)
            prompt = """
            You are an expert OCR & Document Analyzer for Cambodian Bank Payment Slips (បង្កាន់ដៃផ្ទេរប្រាក់).
            Analyze this bank transfer slip (e.g. ACLEDA Bank, ABA Bank, Bakong, Wing, Canadia, etc.) carefully.
            
            Extract the following fields accurately and return ONLY valid JSON:
            {
                "bank_name": "ឈ្មោះធនាគារ (e.g. ACLEDA Bank / ធនាគារ អេស៊ីលីដា, ABA Bank, Bakong)",
                "transaction_type": "ប្រភេទប្រតិបត្តិការ (e.g. ប្រតិបត្តិការ QR, ផ្ទេរប្រាក់)",
                "amount": "ចំនួនទឹកប្រាក់ (e.g. 56,500)",
                "currency": "រូបិយប័ណ្ណ (e.g. KHR / រៀល ឬ USD / $)",
                "sender_name": "ឈ្មោះអ្នកផ្ញើ / គណនីកាត់ប្រាក់ចេញ (e.g. Rin Sopha Rath)",
                "sender_account": "លេខគណនីអ្នកផ្ញើ (e.g. 348***518)",
                "receiver_name": "ឈ្មោះអ្នកទទួលប្រាក់ (e.g. YAI SORNYA)",
                "receiver_account": "លេខគណនីអ្នកទទួល / លេខទូរស័ព្ទ (e.g. 097 881 0715)",
                "transaction_id": "លេខយោង / លេខកូដប្រតិបត្តិការ (Reference / Trx ID, e.g. 62805320857)",
                "date": "កាលបរិច្ឆេទ (e.g. ០៧ តុលា ២០២៦ / 07/10/2026)",
                "time": "ពេលវេលា (e.g. ០៥:៥៥ ល្ងាច / 05:55 PM)",
                "contact_info": "លេខទំនាក់ទំនងធនាគារ (បើមាន)"
            }
            Return ONLY the JSON object. Do not add markdown or backticks.
            """
            response = self.ai_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[img, prompt]
            )
            text_resp = response.text.strip()
            
            # Clean possible markdown wrapping
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

    def scan_slip(self, image_path: str) -> dict:
        """Main method to scan slip image."""
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"មិនអាចបើករូបភាពបានទេ: {image_path}")

        # 1. QR Code scan
        qr_info = self.scan_qr_code(img)

        # 2. Extract with Gemini AI Vision
        if self.use_gemini:
            gemini_data = self.extract_with_gemini(image_path)
            if gemini_data:
                gemini_data.update(qr_info)
                return gemini_data

        # Fallback
        return {
            "bank_name": "Unknown",
            "amount": None,
            "currency": None,
            "sender_name": None,
            "receiver_name": None,
            "transaction_id": None,
            "date": None,
            "time": None,
            **qr_info
        }


if __name__ == "__main__":
    import tkinter as tk
    from tkinter import filedialog

    print("=" * 60)
    print(" 🚀 កម្មវិធីស្គែនបង្កាន់ដៃផ្ទេរប្រាក់ (Bank Slip Scanner)")
    print("=" * 60)

    slip_image = None

    # 1. ពិនិត្យមើល Command Line Argument
    if len(sys.argv) > 1:
        slip_image = sys.argv[1]

    # 2. បើគ្មាន សូមបើកផ្ទាំងជ្រើសរើសរូបភាព File Dialog
    if not slip_image or not os.path.exists(slip_image):
        print("📁 កំពុងបើកផ្ទាំងជ្រើសរើសរូបភាព Slip...")
        try:
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            selected_path = filedialog.askopenfilename(
                title="ជ្រើសរើសរូបភាពបង្កាន់ដៃ (Select Bank Slip Image)",
                filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.webp;*.bmp"), ("All Files", "*.*")]
            )
            root.destroy()
            if selected_path:
                slip_image = selected_path
        except Exception:
            pass

    # 3. បើមិនទាន់បានជ្រើសរើស សួរតាម Terminal
    if not slip_image or not os.path.exists(slip_image):
        user_input = input("\n👉 សូមបញ្ចូលឈ្មោះ ឬ Path រូបភាព Slip: ").strip().strip('"').strip("'")
        if user_input and os.path.exists(user_input):
            slip_image = user_input

    if not slip_image or not os.path.exists(slip_image):
        print(f"\n❌ មិនមានរូបភាពដើម្បីស្គែនទេ! សូមដាក់រូបភាព រួចសាកល្បងម្ដងទៀត។")
    else:
        print(f"\n📸 កំពុងដំណើរការស្គែនរូបភាព: {slip_image}")
        scanner = BankSlipScanner(use_gemini=True)
        result = scanner.scan_slip(slip_image)
        
        print("\n" + "=" * 60)
        print(" 📋 លទ្ធផលស្គែនលម្អិត (Extracted Slip Details)")
        print("=" * 60)
        print(f"🏦 ធនាគារ (Bank)           : {result.get('bank_name')}")
        print(f"🔖 ប្រភេទប្រតិបត្តិការ       : {result.get('transaction_type')}")
        print(f"💰 ចំនួនទឹកប្រាក់ (Amount)   : {result.get('amount')} {result.get('currency', '')}")
        print(f"👤 អ្នកផ្ញើ (Sender)         : {result.get('sender_name')} (គណនី: {result.get('sender_account')})")
        print(f"👥 អ្នកទទួល (Receiver)       : {result.get('receiver_name')} (គណនី: {result.get('receiver_account')})")
        print(f"🔢 លេខយោង (Trx ID)         : {result.get('transaction_id')}")
        print(f"📅 កាលបរិច្ឆេទ (Date)        : {result.get('date')}")
        print(f"⏰ ពេលវេលា (Time)           : {result.get('time')}")
        if result.get('qr_data'):
            print(f"🔲 QR Code Data            : {result.get('qr_data')}")
        print("=" * 60)
