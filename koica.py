from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas 
import os
from dotenv import load_dotenv

# Edge WebDriver-i konfiqurasiya edin
driver = webdriver.Edge()
load_dotenv()
# İstifadəçi adı və şifrəni oxumaq
username = os.getenv("NAME")
password = os.getenv("PASSWORD")

if username is None or password is None:
    raise Exception(".env faylından istifadəçi adı və ya şifrə tapılmadı.")

# Giriş URL-ni daxil edin
def məlumat_giriş():
    url = "https://sso.aztu.edu.az/"
    driver.get(url)
    print("KOICA giriş səhifəsinə keçilir...")
    
    try:
        # İstifadəçi məlumatlarını daxil etmək
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/section/div/div[1]/div/div/form/div[1]/input"))
        )
        username_field.send_keys(username)
        
        password_field = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/div/div/form/div[2]/input")
        password_field.send_keys(password)
        
        login_button = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/div/div/form/div[3]/button")
        login_button.click()
        print("Giriş məlumatları daxil edildi.")
    except Exception as e:
        print(f"Məlumatların daxil edilməsi zamanı səhv: {e}")
    finally:
        time.sleep(5)

def menyu():
 # Menyunu açmaq üçün fa-bars ikonuna klikləyin
 try:
    menu_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "i.fas.fa-bars"))
    )
    menu_icon.click()
 except Exception as e:
    print(f"Xəta baş verdi: {e}")

def tələbə_keçid():
 # Tələbə keçidi düyməsini tapın və klikləyin
 try:
    student_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Tələbə keçid"))
    )
    student_link.click()
 except Exception as e:
    print(f"Xəta baş verdi: {e}")

def fənlər():
 # "Fənlər" bölməsini tapın və klikləyin
 try:
    subjects_menu = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Fənlər')]//parent::a"))
    )
    subjects_menu.click()
 except Exception as e:
    print(f"Fənlər bölməsi tapılmadı: {e}")

def python():
 # "Python proqramlaşdırma dili" linkini tapın və klikləyin
 try:
    python_course = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Python proqramlaşdırma dili"))
    )
    python_course.click()
 except Exception as e:
    print(f"Xəta baş verdi: {e}")

def davamiyyət():
 # Davamiyyət düyməsinə klikləyin
 time.sleep(3)
 attendance_button = driver.find_element(By.LINK_TEXT, "Davamiyyət")
 attendance_button.click()

 WebDriverWait(driver, 10).until(
     EC.presence_of_all_elements_located((By.XPATH, "//th[contains(@class, 'list_text6')]//font"))
 )
 date_elements = driver.find_elements(By.XPATH, "//th[contains(@class, 'list_text6')]//font")
 dates = [date.text for date in date_elements if date.text.strip() != '']

 # Tarixləri almaq
 date_elements = driver.find_elements(By.XPATH, "//th[contains(@class, 'list_text6') and font]//font")
 dates = [date.text for date in date_elements if date.text.strip() != '']

 # İştirak statuslarını almaq
 attendance_elements = driver.find_elements(By.XPATH, "//td[contains(@class, 'attend-td')]//span")
 attendance_status = [att.text.strip() for att in attendance_elements if att.text.strip() in ["i/e", "q/b"]]

 # İştirak məlumatlarını tarixi ilə birləşdirmək
 attendance_data = list(zip(dates, attendance_status))

 # Məlumatları Excel faylına yazmaq
 import pandas as pd

 # İştirak məlumatlarını DataFrame-ə yazmaq
 attendance_df = pd.DataFrame(attendance_data, columns=["Tarix", "Davamiyyət"])

 # Excel faylına yazmaq
 attendance_df.to_excel('attendance_data.xlsx', index=False)  # `encoding` arqumenti çıxarıldı

 print("Məlumatlar uğurla 'attendance_data.xlsx' adlı Excel faylına yazıldı.")

def main():
    məlumat_giriş()
    menyu()
    tələbə_keçid()
    fənlər()
    python()
    davamiyyət()
    driver.quit()

if __name__ == "__main__":
    main()

