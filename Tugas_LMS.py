import sys
import io
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === Agar output terminal mendukung karakter UTF-8 di Windows ===
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# === KONFIGURASI DASAR ===
URL = "https://lms.unm.ac.id/"
USERNAME = "240210501064"
PASSWORD = "Xdms7425"

# === SETUP SELENIUM CHROME ===
chrome_opts = Options()
chrome_opts.add_argument("--start-maximized")
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_opts)
wait = WebDriverWait(driver, 20)

# === FUNGSI LOGIN ===
def login_lms():
    print("Membuka halaman LMS...")
    driver.get(URL)

    print("Klik Login/Register...")
    login_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="mm-0"]/div[1]/header/div/nav/ul[2]/li[1]/a/span')
    ))
    driver.execute_script("arguments[0].click();", login_btn)
    time.sleep(2)

    print("Mengisi username dan password...")
    username_field = wait.until(EC.presence_of_element_located((By.ID, "login_username")))
    password_field = wait.until(EC.presence_of_element_located((By.ID, "login_password")))

    username_field.clear()
    username_field.send_keys(USERNAME)
    password_field.clear()
    password_field.send_keys(PASSWORD)

    submit_btn = wait.until(EC.element_to_be_clickable((
        By.XPATH, '/html/body/div[1]/div[1]/div[3]/div/div/div[2]/div/div/form/button'
    )))
    driver.execute_script("arguments[0].click();", submit_btn)
    print("[OK] Login berhasil dikirim.")


# === FUNGSI MEMBUKA MATA KULIAH ===
def buka_mata_kuliah():
    print("Membuka mata kuliah...")
    course_link = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//a[@class='mcc_view' and contains(text(),'View')]"
    )))
    driver.execute_script("arguments[0].click();", course_link)
    time.sleep(4)


# === FUNGSI MEMBUKA PENGANTAR PERKULIAHAN ===
def buka_pengantar_perkuliahan():
    print("Masuk ke Pengantar Perkuliahan...")
    try:
        pengantar = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//a[contains(@class,'accordion-toggle') and normalize-space(text())='Pengantar Perkuliahan']"
        )))
        driver.execute_script("arguments[0].scrollIntoView(true);", pengantar)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", pengantar)
        print("[OK] Klik Pengantar Perkuliahan berhasil.")

        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='module-695962']")))
        print("[OK] Panel terbuka dan elemen Absensi terdeteksi.")
    except Exception as e:
        print(f"[ERROR] Gagal klik Pengantar Perkuliahan: {e}")


# === FUNGSI MEMBUKA ABSENSI ===
def buka_absensi():
    print("Membuka halaman Absensi...")
    absen_btn = wait.until(EC.element_to_be_clickable((
        By.XPATH, '//*[@id="module-695962"]/div/div/div[2]/div[1]/a/span'
    )))
    driver.execute_script("arguments[0].click();", absen_btn)
    time.sleep(4)


# === FUNGSI SUBMIT ABSENSI ===
def submit_absensi():
    print("Klik tombol Submit Absen...")
    try:
        submit_absen = wait.until(EC.presence_of_element_located((
            By.XPATH, '//*[@id="ccn-main"]/table[1]/tbody/tr[6]/td[3]/a'
        )))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", submit_absen)
        time.sleep(1.5)
        wait.until(EC.element_to_be_clickable((
            By.XPATH, '//*[@id="ccn-main"]/table[1]/tbody/tr[6]/td[3]/a'
        )))
        driver.execute_script("arguments[0].click();", submit_absen)
        print("[OK] Tombol Submit Absen berhasil diklik.")
        time.sleep(2)
    except Exception as e:
        print(f"[ERROR] Gagal klik tombol Submit Absen: {e}")

    print("Memilih opsi Hadir...")
    hadir_opt = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id_status_520420"]')))
    driver.execute_script("arguments[0].click();", hadir_opt)
    time.sleep(2)

    print("Menyimpan absensi...")
    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id_submitbutton"]')))
    driver.execute_script("arguments[0].click();", save_btn)
    time.sleep(3)
    print("[OK] Absen berhasil disubmit!")


# === PROGRAM UTAMA ===
try:
    login_lms()
    buka_mata_kuliah()
    buka_pengantar_perkuliahan()
    buka_absensi()
    submit_absensi()

except Exception as e:
    print(f"[ERROR] Terjadi kesalahan utama: {e}")

finally:
    print("Menutup browser...")
    time.sleep(5)
    driver.quit()