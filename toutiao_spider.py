from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

def fetch_toutiao_search():
    # 配置 Chrome 选项
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 无头模式
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

    try:
        # 初始化浏览器
        driver = webdriver.Chrome(options=options)
        driver.get('https://so.toutiao.com/search?dvpf=pc&source=input&keyword=trae')
        
        # 等待页面加载
        time.sleep(3)
        
        results = []
        # 查找所有新闻卡片
        articles = driver.find_elements(By.CSS_SELECTOR, '.cs-card-content')
        
        for article in articles:
            try:
                # 提取标题
                title = article.find_element(By.CSS_SELECTOR, '.cs-title-text').text.strip()
                
                # 提取摘要
                try:
                    excerpt = article.find_element(By.CSS_SELECTOR, '.cs-abstract-text').text.strip()
                except:
                    excerpt = ''
                
                # 提取图片地址
                try:
                    img_url = article.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
                except:
                    img_url = ''
                
                if title:
                    results.append({
                        'title': title,
                        'excerpt': excerpt,
                        'image_url': img_url
                    })
            except Exception as e:
                print(f"处理单条新闻时出错: {str(e)}")
                continue
        
        # 将结果保存到JSON文件
        with open('toutiao_search.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
            
        print(f"成功抓取 {len(results)} 条内容")
        
    except Exception as e:
        print(f"抓取失败: {str(e)}")
        return []
    
    finally:
        driver.quit()

if __name__ == '__main__':
    fetch_toutiao_search()