import os
import zipfile
from ftplib import FTP
from concurrent.futures import ThreadPoolExecutor
from time import sleep

DOWNLOAD_DIR = "aw3d30_tiles"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


ftp = FTP("ftp.eorc.jaxa.jp")
ftp.login()
ftp.cwd("/pub/ALOS/ext1/AW3D30/release_v2012_single_format")
available_files = ftp.nlst()
ftp.quit()

def download_and_unzip(tile_name):
    if not tile_name.endswith(".zip"):
        return

    local_path = os.path.join(DOWNLOAD_DIR, tile_name)

    if os.path.exists(local_path):
        print(f"✔ Zaten var: {tile_name}")
        return

    try:
        ftp = FTP("ftp.eorc.jaxa.jp")
        ftp.login()
        ftp.cwd("/pub/ALOS/ext1/AW3D30/release_v2012_single_format")

        print(f"⬇ İndiriliyor: {tile_name}")
        with open(local_path, "wb") as f:
            ftp.retrbinary("RETR " + tile_name, f.write)
        ftp.quit()
        print(f"✅ İndirildi: {tile_name}")


        if zipfile.is_zipfile(local_path):
            with zipfile.ZipFile(local_path, 'r') as zip_ref:
                zip_ref.extractall(DOWNLOAD_DIR)
            print(f"📂 Açıldı: {tile_name}")

    except Exception as e:
        print(f"⛔ Hata ({tile_name}): {e}")
        sleep(1)


MAX_WORKERS = 5
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    executor.map(download_and_unzip, available_files)
