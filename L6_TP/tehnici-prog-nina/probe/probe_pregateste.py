# -*- coding: utf-8 -*-
# Tehnici de programare, Sesiunea 6 - generatorul tintelor de laborator.
# Se pune in depozitul de start al studentului ca  probe/pregateste.py  si se ruleaza o data:
#     python probe/pregateste.py
# Produce, in acelasi folder probe/, fisierele pe care le analizeaza laboratorul.
# Depinde doar de Pillow (pip install pillow). Nu atinge nimic din afara folderului probe/.

import os
import base64
import hashlib
import random
from urllib.parse import quote
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))


def scrie(nume, date):
    cale = os.path.join(HERE, nume)
    mod = "wb" if isinstance(date, (bytes, bytearray)) else "w"
    with open(cale, mod, encoding=(None if "b" in mod else "utf-8")) as f:
        f.write(date)
    print("  scris:", nume)


# 1) mesaj.txt: text ascuns sub trei straturi (base64 -> hex -> base64)
clar = b"FLAG{straturi_de_encoding}"
strat_hex = clar.hex().encode()              # text hex, ca octeti
strat_b64_1 = base64.b64encode(strat_hex)    # base64 peste hex
strat_b64_2 = base64.b64encode(strat_b64_1)  # inca un base64 deasupra
scrie("mesaj.txt", strat_b64_2.decode())

# 2) xor.bin: un text clar, criptat cu XOR pe un singur octet
# Cheia 0x80 este aleasa anume: orice cheie gresita lasa octeti neimprimabili,
# deci filtrul simplu „toti octetii imprimabili" gaseste prima data exact cheia buna.
secret = b"Un singur octet tine tot secretul... gaseste-l! FLAG{xor_un_octet}"
K = 0x80
scrie("xor.bin", bytes(b ^ K for b in secret))

# 3) hashuri.txt + wordlist.txt: parole de spart prin dictionar
parole = ["password", "dragon", "qwerty", "letmein", "monkey"]
wordlist = ["123456", "football", "iloveyou"] + parole + ["admin", "welcome"]
random.seed(6); random.shuffle(wordlist)
scrie("hashuri.txt", "\n".join(hashlib.md5(p.encode()).hexdigest() for p in parole) + "\n")
scrie("wordlist.txt", "\n".join(wordlist) + "\n")

# 4) foto.jpg: o imagine cu metadate EXIF, inclusiv coordonate GPS (Chisinau)
img = Image.new("RGB", (640, 480), (70, 110, 160))
exif = Image.Exif()
exif[0x010F] = "Apple"                     # Make
exif[0x0110] = "iPhone 13"                 # Model
exif[0x0132] = "2026:09:14 10:30:00"       # DateTime
# GPS IFD: 47.0167 N, 28.8575 E  (grade, minute, secunde ca rationale)
exif[0x8825] = {
    1: "N", 2: (47.0, 1.0, 0.0),
    3: "E", 4: (28.0, 51.0, 27.0),
}
img.save(os.path.join(HERE, "foto.jpg"), exif=exif, quality=90)
print("  scris: foto.jpg")

# 5) ascuns.png: o imagine PNG cu o arhiva ZIP lipita la coada (file carving)
png_path = os.path.join(HERE, "ascuns.png")
Image.new("RGB", (320, 240), (40, 160, 90)).save(png_path)
import zipfile, io
buf = io.BytesIO()
with zipfile.ZipFile(buf, "w") as z:
    z.writestr("secret.txt", "FLAG{ascuns_prin_carving}\n")
with open(png_path, "ab") as f:
    f.write(buf.getvalue())
print("  adaugat ZIP la coada: ascuns.png")

# 6) challenge.bin (optional, pentru varful salii): encoding peste XOR
inner = bytes(b ^ 0x80 for b in b"FLAG{lant_complet_despicat}")
scrie("challenge.bin", base64.b64encode(inner))
scrie("challenge_hint.txt",
      "Un strat de base64 peste un XOR cu cheie de un octet. "
      "Verificare: md5 al textului clar = " + hashlib.md5(b"FLAG{lant_complet_despicat}").hexdigest() + "\n")

print("Gata. Tintele de laborator sunt in:", HERE)
