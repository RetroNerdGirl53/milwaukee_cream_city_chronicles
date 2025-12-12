import base64
import json
import time
import os
import textwrap

try:
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives import serialization
    from PIL import Image, ImageDraw, ImageFont
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("WARNING: Cryptography or Pillow not available. Token system will be disabled.")

# New Keys generated in session to ensure they match
PRIVATE_KEY_PEM = b"""-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDMVy9NWH3Fefiv
w99Na0PT81vSV/xffQPECj2Y2kpQUBDykY4eYcD/8Vv7bVSeruQ6TMvUnyNaM9aN
H1zVADO5ArAsntajbPtSnPzxMx0mTC/Px4spuVts9DSntPpbDfj3AHV9nlvfTe34
kwedM6laZHax5inyIzb+F0xcEaoMTh+X+87WI0CWT6Mz9SVKF5cyKKSSEHNvVA6c
L0And3qejBGHJVtH44cS83dt9nn8CHNwmTlulZfY79szMWQrBJj6/x6gSB4nAhL3
hb5qXlJ82MUlJTM/WpvHzfntWodVsCB2jjAugMtFg2ELXQ3rX7C+RwgSReqwTejc
i1ZOE6/bAgMBAAECggEAK4cs79x4Wj8rvwFKCZteZQFzn2CXxZ2DVljaGzvw1Z/g
pFNmQ0mOi9bVwb7d5jmaK2Mdjmrh5H6jZwd1xnfXDMOqVK73SPPXq5b+eMDrJjPX
gXrfxaES/SgeKVVveUMGNFOYM4yuxGg815U2a4HMQxGgiS/e4pImzkSXQwuOPjVq
ltGCSfLLUSnwbn20QpATtggGDXxuZnjx6UDfDgtvYYLnZEqo9UcYUgc8+ua1/o4L
/YzsXqvz9Lxk8r4Q0hRZks4PrAXwbn9w0EWy4Dq+SkC+dLgvNqmn9oceTp7teaI8
ArBvEGIza5Vf28PyPjOEOTrxf94odJJpR0177ygeDQKBgQDuJ3jJGwCamnf02aVC
jaj/8HYnAA3v0jYhLkBLaGvVstdFeHXblYtrLX2s93DO/2wZjATO5izWgp9Wl4zZ
WSYjwiPTKqQlEdnC6SzfJflg26kx3ubNk5pWGap2j5ELtACCoXYu8ylVstK488Wd
KKYHT8bKcIQeB2PnOSp9iI//lQKBgQDbpxBdkXPqQ5eeD60XIWROxEYfsQvXPlME
OnktmAq6jPzylK0lpH+YzLQXmygocl0rKtKsWnfMe52a8xy02LlbwfjyZJpdb313
VLnf4f5Ms+FYCTIfF8Us1rooiVyX6CTRVaPskZ+oTGD9mN1xi+Q5dWk9you5vZLc
QzY+mMnVrwKBgQDsea866aAQ4/7m1tJ9IlLESM3Zbflov+/VxKo89mPVHy8YoUNO
FdEJTHN1M4IFWKTLPThtBStSmQOEpRlLnHT9nsGZ5cZ1tKLpIkXXEkrsfVEk3vOI
/96JThTwgyAAYez7yT2j4vmRSe5pjk0T/4/UxMdcrprRgn8V0rK5UcfCfQKBgADQ
fsQKDQb6Vy6T2k1ypz+PhL8LVgLnTUF/wgFERg3pBesUWAwCryJu5+AKiDyWJ/hI
AV34O+d7MdtoOVwGTbGkZ3rmmpfsGOf/XW0SFnJMXHKKHjB1UxrWdPw/fiNmDfTk
v2XaKGBkYBuwnGmWXjNEVy6OeLQomsnMSgAzatQrAoGBALNuKY+Q702e9jVxeQLb
9Ofd4IzhCmbgjTxfgtCl1n8ddYTqQPTup+yNjTb4QGYCliHy1WtovTng7/GWl2G5
ly45seNzHSfvIZxH/Z8r2e1bQgD12bnKkg6RXPrcI+dSnItM0YWG+kmIEs53HBOm
y6VqVzCaKVyhv9ftpzUC9lvF
-----END PRIVATE KEY-----"""

PUBLIC_KEY_PEM = b"""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzFcvTVh9xXn4r8PfTWtD
0/Nb0lf8X30DxAo9mNpKUFAQ8pGOHmHA//Fb+21Unq7kOkzL1J8jWjPWjR9c1QAz
uQKwLJ7Wo2z7Upz88TMdJkwvz8eLKblbbPQ0p7T6Ww349wB1fZ5b303t+JMHnTOp
WmR2seYp8iM2/hdMXBGqDE4fl/vO1iNAlk+jM/UlSheXMiikkhBzb1QOnC9AJ3d6
nowRhyVbR+OHEvN3bfZ5/AhzcJk5bpWX2O/bMzFkKwSY+v8eoEgeJwIS94W+al5S
fNjFJSUzP1qbx8357VqHVbAgdo4wLoDLRYNhC10N61+wvkcIEkXqsE3o3ItWThOv
2wIDAQAB
-----END PUBLIC KEY-----"""

class CryptoManager:
    def __init__(self):
        if not CRYPTO_AVAILABLE:
            self.private_key = None
            self.public_key = None
            return

        self.private_key = serialization.load_pem_private_key(
            PRIVATE_KEY_PEM,
            password=None
        )
        self.public_key = serialization.load_pem_public_key(PUBLIC_KEY_PEM)

    def sign_data(self, data_str):
        """Sign a string message."""
        if not self.private_key: return "ERROR: NO CRYPTO"
        signature = self.private_key.sign(
            data_str.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return base64.b64encode(signature).decode('utf-8')

    def verify_signature(self, data_str, signature_b64):
        """Verify a signature."""
        if not self.public_key: return False
        try:
            signature = base64.b64decode(signature_b64)
            self.public_key.verify(
                signature,
                data_str.encode('utf-8'),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception as e:
            # print(f"Verification failed: {e}")
            return False

    def generate_token(self, item_name, player_name, extra_data=None):
        """Generates a full token JSON string."""
        if not CRYPTO_AVAILABLE: return "{}"

        payload = {
            "item": item_name,
            "owner": player_name,
            "timestamp": time.time(),
            "id": base64.b64encode(os.urandom(6)).decode('utf-8'),
            "extra": extra_data or {}
        }

        # Serialize payload deterministically
        payload_str = json.dumps(payload, sort_keys=True)
        signature = self.sign_data(payload_str)

        token = {
            "payload": payload,
            "signature": signature
        }
        return base64.b64encode(json.dumps(token).encode('utf-8')).decode('utf-8')

    def verify_token(self, token_b64):
        """Verifies a token string and returns the payload if valid."""
        if not CRYPTO_AVAILABLE: return None
        try:
            token_json = base64.b64decode(token_b64).decode('utf-8')
            token = json.loads(token_json)

            payload = token['payload']
            signature = token['signature']

            payload_str = json.dumps(payload, sort_keys=True)

            if self.verify_signature(payload_str, signature):
                return payload
            else:
                return None
        except Exception as e:
            print(f"Token error: {e}")
            return None

    def create_image_artifact(self, token_b64, filename="artifact.png"):
        """Creates an image with the token embedded."""
        if not CRYPTO_AVAILABLE: return

        try:
            # Decode token to get info for the text
            token_json = base64.b64decode(token_b64).decode('utf-8')
            token_obj = json.loads(token_json)
            payload = token_obj['payload']
            item_name = payload['item']
            owner = payload['owner']

            # Create Image
            width, height = 600, 300
            img = Image.new('RGB', (width, height), color=(25, 25, 25))
            d = ImageDraw.Draw(img)

            # Draw Border
            d.rectangle([10, 10, width-10, height-10], outline=(255, 0, 255), width=5)

            # Draw Text (using default font since we might not have a ttf)
            # Load default font is tricky in PIL sometimes if system fonts are missing,
            # so we stick to default bitmap font which is small.
            # Or try to load a basic one.
            try:
                # Try to grab a truetype if possible, otherwise default
                font_title = ImageFont.load_default()
                # On some systems load_default returns a very small font.
                # We can't easily scale it without a ttf file.
                # We will just write multiple lines or hope it's legible.
            except:
                font_title = None

            # Centered Text Helper
            def draw_centered_text(y, text, color):
                # Simple approximation for centering with default font
                # Default font is roughly 6x10 pixels usually?
                text_width = len(text) * 6
                x = (width - text_width) / 2
                d.text((x, y), text, fill=color)

            # Draw Content
            d.text((50, 40), "MILWAUKEE BLOCKCHAIN AUTHORITY", fill=(0, 255, 255))
            d.text((50, 80), f"ITEM: {item_name.upper()}", fill=(255, 255, 0))
            d.text((50, 110), f"OWNER: {owner}", fill=(255, 255, 255))
            d.text((50, 140), f"DATE: {time.ctime(payload['timestamp'])}", fill=(200, 200, 200))

            # Draw Token (wrapped)
            d.text((50, 180), "DIGITAL TOKEN (VERIFIABLE):", fill=(255, 0, 255))
            lines = textwrap.wrap(token_b64, width=80)
            y = 200
            for line in lines[:5]: # Only show first few lines
                d.text((50, y), line, fill=(100, 100, 100))
                y += 12

            if len(lines) > 5:
                d.text((50, y), "... (See metadata for full token)", fill=(100, 100, 100))

            # Embed Token in Metadata (PNG tEXt chunk)
            from PIL.PngImagePlugin import PngInfo
            metadata = PngInfo()
            metadata.add_text("MilwaukeeToken", token_b64)
            metadata.add_text("Description", f"Official Proof of {item_name}")

            img.save(filename, "PNG", pnginfo=metadata)
            return True
        except Exception as e:
            print(f"Failed to create image: {e}")
            return False

    def verify_image_artifact(self, filepath):
        """Reads a PNG and verifies the embedded token."""
        if not CRYPTO_AVAILABLE: return None
        try:
            with Image.open(filepath) as img:
                token_b64 = img.text.get("MilwaukeeToken")
                if not token_b64:
                    return {"valid": False, "error": "No token found in image."}

                payload = self.verify_token(token_b64)
                if payload:
                    return {"valid": True, "payload": payload}
                else:
                    return {"valid": False, "error": "Invalid Signature"}
        except Exception as e:
            return {"valid": False, "error": str(e)}
