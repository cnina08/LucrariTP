import os
import re
from PIL import Image
from PIL.ExifTags import TAGS

# B1. Magic bytes: tipul real, nu extensia
def tip_real(cale):
    if not os.path.exists(cale):
        return "inexistent"
    cap = open(cale, "rb").read(8)
    if cap.startswith(b"%PDF"):
        return "pdf"
    elif cap.startswith(b"\x89PNG"):
        return "png"
    elif cap.startswith(b"\xff\xd8"):
        return "jpeg"
    elif cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    return cap.hex()

# B2. strings: textul citibil dintr-un binar
def extrage_strings(cale):
    if not os.path.exists(cale):
        return []
    date = open(cale, "rb").read()
    return [m.decode('utf-8', errors='ignore') for m in re.findall(rb"[ -~]{4,}", date)]

# B3. Metadate EXIF și GPS din poză
def citeste_exif_gps(cale):
    if not os.path.exists(cale):
        return None
    try:
        img = Image.open(cale)
        exif = img._getexif() or {}
        gps_info = {}
        for tag_id, val in exif.items():
            nume_tag = TAGS.get(tag_id, tag_id)
            if nume_tag == 'GPSInfo':
                for t in val:
                    sub_nume = TAGS.get(t, t)
                    gps_info[sub_nume] = val[t]
        return gps_info
    except Exception:
        return None

# B4. File carving: scoți fișierul ascuns
def file_carving(cale_sursa, iesire_zip="gasit.zip"):
    if not os.path.exists(cale_sursa):
        return False
    date = open(cale_sursa, "rb").read()
    i = date.find(b"PK\x03\x04")
    if i != -1:
        with open(iesire_zip, "wb") as f:
            f.write(date[i:])
        print(f"[+] Arhivă extrasă de la octetul {i} în {iesire_zip}")
        return True
    return False

# B5. Ascunzi un mesaj prin LSB
def ascunde_lsb(cale_foto, mesaj, cale_iesire="stego.png"):
    img = Image.open(cale_foto).convert("RGB")
    px = list(img.getdata())
    mesaj_bytes = mesaj + b"\x00"
    biti = "".join(f"{x:08b}" for x in mesaj_bytes)
    
    px_nou = []
    bit_idx = 0
    for p in px:
        r, g, b = p
        if bit_idx < len(biti):
            r = (r & ~1) | int(biti[bit_idx]); bit_idx += 1
        if bit_idx < len(biti):
            g = (g & ~1) | int(biti[bit_idx]); bit_idx += 1
        if bit_idx < len(biti):
            b = (b & ~1) | int(biti[bit_idx]); bit_idx += 1
        px_nou.append((r, g, b))
        
    img_noua = Image.new("RGB", img.size)
    img_noua.putdata(px_nou)
    img_noua.save(cale_iesire)
    print(f"[+] Mesaj ascuns salvat în {cale_iesire}")

# B6. Dezvălui mesajul înapoi
def dezvaluie_lsb(cale_stego):
    px = list(Image.open(cale_stego).convert("RGB").getdata())
    biti = []
    for (r, g, b) in px:
        biti.append(str(r & 1))
        biti.append(str(g & 1))
        biti.append(str(b & 1))
        
    biti_str = "".join(biti)
    octeti = []
    for i in range(0, len(biti_str), 8):
        octet_str = biti_str[i:i+8]
        if len(octet_str) < 8:
            break
        val = int(octet_str, 2)
        if val == 0:
            break
        octeti.append(val)
    return bytes(octeti)

if __name__ == "__main__":
    print("Tip real foto.jpg:", tip_real("../../probe/foto.jpg"))
    print("Tip real ascuns.png:", tip_real("../../probe/ascuns.png"))
    print("GPS info:", citeste_exif_gps("../../probe/foto.jpg"))
    file_carving("../../probe/ascuns.png", "../../gasit.zip")
    
    # Test LSB
    mesaj_test = b"FLAG{ascuns_in_pixeli}"
    ascunde_lsb("../../probe/foto.jpg", mesaj_test, "../../stego.png")
    extras = dezvaluie_lsb("../../stego.png")
    print("Mesaj LSB dezvăluit:", extras.decode('utf-8', errors='ignore'))