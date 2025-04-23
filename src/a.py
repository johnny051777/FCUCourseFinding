from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# 設定 headless 模式（可視情況開啟）
options = Options()
# options.add_argument('--headless')  # 嘗試移除這行進行可視化測試
options.add_argument('--disable-gpu')

# 啟動 ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 你的課程查詢連結（含 token）
url = "https://coursesearch03.fcu.edu.tw/main.aspx?token=yourToken"
driver.get(url)

# 初始化課程資料列表
courses = []

try:
    # 增加等待時間，確保頁面加載完成
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//tr[@ng-repeat]"))
    )
    print("頁面加載完成！")

    # 等待頁面渲染完成
    time.sleep(3)  # 進一步確保頁面渲染完成

    # 抓取所有課程行（每行一門課）
    rows = driver.find_elements(By.XPATH, "//tr[@ng-repeat]")
    print(f"共找到 {len(rows)} 筆課程資料")

    if len(rows) == 0:
        print("未能成功找到資料，請檢查 XPath 或等候時間")

    for row in rows:
        try:
            # 抓取各個資料欄位
            code = row.find_element(By.XPATH, ".//td[@data-title='選課代碼']").text.strip()
            course_id = row.find_element(By.XPATH, ".//td[@data-title='課程編碼']").text.strip()
            name = row.find_element(By.XPATH, ".//td[@data-title='課程名稱']//a").text.strip()
            course_url = row.find_element(By.XPATH, ".//td[@data-title='課程名稱']//a").get_attribute("href")
            credit = row.find_element(By.XPATH, ".//td[@data-title='學分']").text.strip()
            elective = row.find_element(By.XPATH, ".//td[@data-title='必選修']").text.strip()
            teaching_method = row.find_element(By.XPATH, ".//td[@data-title='上課方式']").text.strip()
            class_info = row.find_element(By.XPATH, ".//td[@data-title='開課班級']").text.strip()
            schedule = row.find_element(By.XPATH, ".//td[@data-title='上課時間/上課教室/授課教師']").text.strip()

            time.sleep(2)  # 等待頁面加載

            # 將課程資料加入到 courses 列表中
            courses.append({
                '選課代碼': code,
                '課程編碼': course_id,
                '課程名稱': name,
                '學分': credit,
                '必選修': elective,
                '上課方式': teaching_method,
                '開課班級': class_info,
                '上課時間': schedule,
            })

        except Exception as e:
            print("資料解析錯誤：", e)

except Exception as e:
    print("無法載入課程資料：", e)

finally:
    driver.quit()

# 顯示抓取到的課程資料
print(f"共抓取到 {len(courses)} 筆資料")
print("=" * 40)

for course in courses:
    print(course)
    print("-" * 40)
