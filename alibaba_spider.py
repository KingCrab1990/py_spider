from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import random

def fetch_1688_products():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

    try:
        driver = webdriver.Chrome(options=options)
        url = 'https://s.1688.com/selloffer/offer_search.htm?keywords=%CF%D4%BF%A8'
        driver.get(url)
        
        # 等待登录，这里需要手动登录
        print("请在浏览器中手动登录1688（30秒）...")
        time.sleep(30)
        
        # 等待商品列表加载
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.offer-list-row-offer'))
        )
        
        # 滚动页面以加载更多商品
        for i in range(3):
            driver.execute_script('window.scrollBy(0, 800)')
            time.sleep(1)
        
        results = []
        items = driver.find_elements(By.CSS_SELECTOR, '.offer-list-row-offer')
        
        for item in items:
            try:
                # 提取标题
                title = item.find_element(By.CSS_SELECTOR, '.title').text.strip()
                
                # 提取价格
                price = item.find_element(By.CSS_SELECTOR, '.price').text.strip()
                
                # 提取商家名称
                company = item.find_element(By.CSS_SELECTOR, '.company-name').text.strip()
                
                # 提取图片地址
                img_url = item.find_element(By.CSS_SELECTOR, '.img').get_attribute('src')
                if not img_url.startswith('http'):
                    img_url = 'https:' + img_url
                
                results.append({
                    'title': title,
                    'price': price,
                    'company': company,
                    'image_url': img_url
                })
                
                # 随机延迟
                time.sleep(random.uniform(0.3, 0.8))
                
            except Exception as e:
                print(f"处理单个商品时出错: {str(e)}")
                continue
        
        # 保存结果
        with open('alibaba_products.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
            
        print(f"成功抓取 {len(results)} 个商品")
        
    except Exception as e:
        print(f"抓取失败: {str(e)}")
        return []
        
    finally:
        driver.quit()

if __name__ == '__main__':
    fetch_1688_products()