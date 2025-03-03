from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import random

def fetch_douban_books():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

    try:
        driver = webdriver.Chrome(options=options)
        url = 'https://book.douban.com/'
        driver.get(url)
        
        # 等待图书列表加载
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.popular-books .cover'))
        )
        
        results = []
        
        # 获取热门图书
        books = driver.find_elements(By.CSS_SELECTOR, '.popular-books li')
        
        for book in books:
            try:
                # 提取书名
                title = book.find_element(By.CSS_SELECTOR, 'img').get_attribute('alt')
                
                # 提取作者
                try:
                    author = book.find_element(By.CSS_SELECTOR, '.author').text.strip()
                except:
                    author = '未知作者'
                
                # 提取图片地址
                img_url = book.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
                
                results.append({
                    'title': title,
                    'author': author,
                    'image_url': img_url
                })
                
                # 随机延迟
                time.sleep(random.uniform(0.3, 0.8))
                
            except Exception as e:
                print(f"处理单本图书时出错: {str(e)}")
                continue
        
        # 保存结果
        with open('douban_books.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
            
        print(f"成功抓取 {len(results)} 本图书")
        
    except Exception as e:
        print(f"抓取失败: {str(e)}")
        return []
        
    finally:
        driver.quit()

if __name__ == '__main__':
    fetch_douban_books()