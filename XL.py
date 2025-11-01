import requests, re, json

def headers(bear):
    return {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'Bearer {bear}',
        'content-type': 'application/json',
        'origin': 'https://www.xlaxiata.co.id',
        'referer': 'https://www.xlaxiata.co.id/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'dnt': '1',
        'priority': 'u=1, i',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

def bearer():
    try:
        header = {
            'Referer': 'https://www.xlaxiata.co.id/registrasi',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        }
        js_url = 'https://www.xlaxiata.co.id/registrasi/_next/static/chunks/pages/regbypuk/regbypukform-b0a844f3483c094b.js'
        resp = requests.get(js_url, headers=header, timeout=10)
        bear = re.search(r'concat\("([^"]+)"\)', resp.text.strip()).group(1)
    except:
        bear = "VzNicHIzR24wbjEzaW8yMDI0OmJ5ZHQybzI0KiE="

    try:
        token = requests.post(
            'https://jupiter-ms-webprereg.xlaxiata.id/generate-jwt',
            headers=headers(bear),
            timeout=10
        ).json().get('encryptToken')
        return token
    except:
        return "Ln9YN5trk3UUGHnHXoV8644+QEDWRf8qpLJ0tovzrhQVRjJKzRulyHxNIa8eos0pH7iNIePuPNOxNmY4sRnHZIPEPD7iKAX2Z8Z2qOucrAQ+h6Z98l7GQEoIrDwRTXAD7nLAyRnH9dVwzmidCPSH9dwWBE31I739FGTNKJdqB44Ieq3PIs1y1ay6eZgmNBY84QrE22qRYOzUFWX/68cCNwFoJJdf0BdZeKclWxJAasfLAHR1bnM5V8VkNiC+CZlWe08UiEGaltTDcp2hoLGsaYshcy48PIefK3WseHwQn1SvSERWWNbHO0F70RLz7V0CXOg222YN7LQdwhm2Nv1tiw=="

token = bearer()

while True:
    number = input("📱 Masukkan nomor +62: ")

    response_otp_request = requests.post(
        'https://jupiter-ms-webprereg.xlaxiata.id/request-otp',
        headers=headers(token),
        json={"msisdn": number}
    )

    try:
        resp_json = response_otp_request.json()
    except json.JSONDecodeError:
        resp_json = {}

    print(f"📩 OTP request status: {response_otp_request.status_code}")
    print("📥 Response:", resp_json)

    with open('nik.txt', 'r') as file:
        for line in file:
            NIK, KK = line.strip().split('|')

            while True:
                OTP = input(f"NIK: {NIK} | KK: {KK}\n➡️ Masukkan OTP: ")

                response_otp_verification = requests.post(
                    'https://jupiter-ms-webprereg.xlaxiata.id/submit-registration-otp-non-biometric',
                    headers=headers(token),
                    json={"msisdn": number, "nik": NIK, "kk": KK, "otpCode": OTP}
                )

                try:
                    result = response_otp_verification.json()
                except json.JSONDecodeError:
                    print("⚠️ Response tidak valid:", response_otp_verification.text)
                    break

                text_result = str(result).lower()

                if 'success' in text_result or result.get('status') == 'SUCCESS':
                    print(f"✅ {number} BERHASIL REGISTRASI (NIK: {NIK})")
                    break

                elif any(k in text_result for k in ["sudah terdaftar", "already registered", "nomer anda sudah diaktifkan sebelumnya"]):
                    print(f"⚠️ {number} SUDAH TERDAFTAR — KEMBALI KE MENU MASUKAN NOMOR")
                    break

                elif any(k in text_result for k in ["otp salah", "invalid otp", "otpcode invalid"]):
                    print("❌ OTP SALAH — silakan coba lagi")
                    continue

                elif any(k in text_result for k in ["nik", "kk", "tidak valid", "not valid"]):
                    print(f"❌ NIK/KK TIDAK VALID — {NIK} | {KK}")
                    break

                else:
                    print(f"❌ GAGAL REGISTRASI — {result.get('message', 'Unknown error')}")
                    break
