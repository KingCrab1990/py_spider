from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

def fetch_weather_tips():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

    try:
        driver = webdriver.Chrome(options=options)
        url = 'https://weather.cma.cn/web/channel-380.html'
        driver.get(url)
        
        # 等待内容加载
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.contentInfo'))
        )
        
        results = []
        
        # 获取天气提示列表
        tips = driver.find_elements(By.CSS_SELECTOR, '.contentInfo')
        
        for tip in tips:
            try:
                # 提取标题
                title = tip.find_element(By.CSS_SELECTOR, '.title').text.strip()
                
                # 提取发布时间
                time_info = tip.find_element(By.CSS_SELECTOR, '.time').text.strip()
                
                # 提取内容
                content = tip.find_element(By.CSS_SELECTOR, '.content').text.strip()
                
                results.append({
                    'title': title,
                    'time': time_info,
                    'content': content
                })
                
            except Exception as e:
                print(f"处理单条天气提示时出错: {str(e)}")
                continue
        
        # 保存结果
        with open('weather_tips.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
            
        print(f"成功抓取 {len(results)} 条天气提示")
        
    except Exception as e:
        print(f"抓取失败: {str(e)}")
        return []
        
    finally:
        driver.quit()

if __name__ == '__main__':
    fetch_weather_tips()