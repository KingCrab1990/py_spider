import requests
from bs4 import BeautifulSoup
import json

def fetch_zhihu_feed():
    # 设置请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    url = 'https://www.zhihu.com/?lang=zh-Hant'
    
    try:
        # 发送GET请求
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找所有文章卡片
        articles = soup.find_all('div', class_='Card')
        
        results = []
        for article in articles:
            # 提取标题
            title_element = article.find('h2')
            title = title_element.text.strip() if title_element else ''
            
            # 提取摘要
            excerpt_element = article.find('div', class_='RichContent-inner')
            excerpt = excerpt_element.text.strip() if excerpt_element else ''
            
            # 提取图片地址
            img_element = article.find('img')
            img_url = img_element.get('src') if img_element else ''
            
            if title:  # 只保存有标题的内容
                results.append({
                    'title': title,
                    'excerpt': excerpt,
                    'image_url': img_url
                })
        
        # 将结果保存到JSON文件
        with open('zhihu_feed.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
            
        print(f"成功抓取 {len(results)} 条内容")
        return results
            
    except Exception as e:
        print(f"抓取失败: {str(e)}")
        return []

if __name__ == '__main__':
    fetch_zhihu_feed()