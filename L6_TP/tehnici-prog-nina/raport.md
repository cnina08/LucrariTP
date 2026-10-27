# Raport - Laboratorul 6: Informații invizibile, forensics și steganografie

- **Mesajul decodat din straturi (`mesaj.txt`):** `FLAG{straturi_de_encoding}`
- **Criptograma XOR (`xor.bin`):** Cheia găsită este `0x80`, iar textul clar descoperit este `FLAG{xor_un_octet}`.
- **Parola spartă din hash-uri (`hashuri.txt`):** Cuvântul din dicționar corespunzător hash-ului MD5 este `password`.
- **Tipul real al fișierelor (Magic Bytes):**
  - `probe/foto.jpg`: `jpeg`
  - `probe/ascuns.png`: `png` (cu arhivă ZIP lipită la coadă).
- **Metadate EXIF și GPS (`probe/foto.jpg`):** 
  - Dispozitiv: Apple iPhone 13
  - Coordonate GPS: Latitudine ~47.0167 N, Longitudine ~28.8575 E (Chișinău).
- **Arhiva ascunsă (`probe/ascuns.png`):** Fișierul extras prin *file carving* conține fișierul `secret.txt` cu flag-ul `FLAG{ascuns_prin_carving}`.
- **Steganografie LSB:** Mesajul ascuns și extras cu succes din imaginea `stego.png` este `FLAG{ascuns_in_pixeli}`.