import os
import re
import base64
from urllib.parse import unquote
import hashlib
import argparse
import json

def ghici_strat(s):
    if "%" in s and re.search(r'%[0-9A-Fa-f]{2}', s):
        return "url"
    if all(c in "0123456789abcdefABCDEF" for c in s) and len(s) % 2 == 0:
        return "hex"
    if re.match(r'^[A-Za-z0-9+/]+={0,2}$', s) and len(s) % 4 == 0:
        return "base64"
    return "necunoscut"

def desfa(s):
    strat = ghici_strat(s)
    if strat == "base64":
        try:
            return strat, base64.b64decode(s)
        except Exception:
            pass
    elif strat == "hex":
        try:
            return strat, bytes.fromhex(s)
        except Exception:
            pass
    elif strat == "url":
        try:
            return strat, unquote(s).encode()
        except Exception:
            pass
    return "necunoscut", s.encode()

def citibil(b):
    return all(32 <= c < 127 for c in b)

def decodare_multipla(val):

    rezultat_final = val

    strat_final = "necunoscut"

    for _ in range(8):

        strat, b = desfa(val)

        if strat == "necunoscut":

            break

        if citibil(b):

            try:

                rezultat_final = b.decode('utf-8')

            except UnicodeDecodeError:

                rezultat_final = b.hex()

            strat_final = strat

            break

        else:

            try:

                val = b.decode('utf-8', errors='ignore')

                strat_final = strat

            except Exception:

                break

    return strat_final, rezultat_final



def sparge_xor(cale_bin):
    if not os.path.exists(cale_bin):
        return None, None
    date = open(cale_bin, "rb").read()
    for k in range(256):
        clar = bytes(b ^ k for b in date)
        if citibil(clar):
            try:
                return k, clar.decode('utf-8')
            except UnicodeDecodeError:
                continue
    return None, None

def sparge_hash(cale_hashuri, cale_wordlist):

    if not os.path.exists(cale_hashuri) or not os.path.exists(cale_wordlist):

        return None, None

    tinta = open(cale_hashuri).readline().strip()

    lungime = len(tinta)

   

    with open(cale_wordlist, encoding="latin1") as f:

        for cuv in f:

            cuv = cuv.strip()

            if lungime == 32:

                h = hashlib.md5(cuv.encode()).hexdigest()

            elif lungime == 40:

                h = hashlib.sha1(cuv.encode()).hexdigest()

            elif lungime == 64:

                h = hashlib.sha256(cuv.encode()).hexdigest()

            else:

                return None, None

            if h == tinta:

                return tinta, cuv

    return tinta, None

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("intrare", nargs="?", default="probe/mesaj.txt")
    p.add_argument("--fisier", action="store_true")
    a = p.parse_args()

    if a.fisier or os.path.exists(a.intrare):
        with open(a.intrare, "rb") as f:
            continut = f.read().decode('utf-8', errors='ignore').strip()
    else:
        continut = a.intrare

    strat, rezultat = decodare_multipla(continut)
    
    # Verificare opțională pentru XOR și Hashuri din probe
    cheie_xor, text_xor = sparge_xor("probe/xor.bin")
    _, parola_sparta = sparge_hash("probe/hashuri.txt", "probe/wordlist.txt")

    fisa = {
        "strat_mesaj": strat,
        "rezultat_mesaj": rezultat,
        "cheie_xor": cheie_xor,
        "text_xor": text_xor,
        "parola_sparta": parola_sparta
    }
    
    os.makedirs("arsenal/forensics", exist_ok=True)
    with open("arsenal/forensics/fisa.json", "w", encoding="utf-8") as f:
        json.dump(fisa, f, indent=4)
    
    print(f"[+] Decodat cu succes! Strat: {strat}")
    print(f"[+] Rezultat mesaj: {rezultat}")
    if cheie_xor is not None:
        print(f"[+] XOR spart cu cheia 0x{cheie_xor:02x}: {text_xor}")
    if parola_sparta:
        print(f"[+] Parolă găsită în dicționar: {parola_sparta}")
    print(f"[+] Date salvate în arsenal/forensics/fisa.json")