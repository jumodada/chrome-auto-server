from DrissionPage import ChromiumOptions, Chromium
import time
import json
from datetime import datetime
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('monitor.log'),
        logging.StreamHandler()
    ]
)

class DyMonitor:
    def __init__(self):
        self.co = ChromiumOptions().set_browser_path(
            r'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        )
        self.co.set_user_data_path(
            r'/Users/kunyunwu/Library/Application Support/Google/Chrome/Default'
        )
        self.browser = None
        self.target_url = 'https://buyin.jinritemai.com/dashboard'

    def start_browser(self):
        try:
            if self.browser is None:
                self.browser = Chromium(addr_or_opts=self.co)
            logging.info("浏览器启动成功")
        except Exception as e:
            logging.error(f"浏览器启动失败: {str(e)}")
            raise e

    def get_page_data(self):
        try:
            tab = self.browser.latest_tab
            tab.get(url=self.target_url)
            
            # 获取cookies
            cookies = tab.cookies()
            
            # 获取localStorage和其他数据
            tab.console.start()
            js_code = '''
                console.log(JSON.stringify({
                    localStorage: Object.fromEntries(
                        Object.keys(localStorage).map(key => [key, localStorage.getItem(key)])
                    ),
                    BTM_MAP_DATA: window.BTM_MAP_DATA,
                    pageList: window.pageList,
                }));
            '''
            tab.run_js(js_code)
            window_data = tab.console.wait()
            
            # 保存数据
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # 保存cookies
            with open(f'data/cookies_{timestamp}.json', 'w', encoding='utf-8') as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            
            # 保存window数据
            if window_data and window_data.text:
                with open(f'data/window_data_{timestamp}.json', 'w', encoding='utf-8') as f:
                    json.dump(json.loads(window_data.text), f, ensure_ascii=False, indent=2)
            
            logging.info(f"数据获取成功，已保存至 data/cookies_{timestamp}.json 和 data/window_data_{timestamp}.json")
            
            # TODO: 这里可以添加数据处理逻辑
            
            return True
            
        except Exception as e:
            logging.error(f"数据获取失败: {str(e)}")
            return False

    def run(self, interval=300):  # 默认5分钟运行一次
        while True:
            try:
                if self.browser is None:
                    self.start_browser()
                
                success = self.get_page_data()
                if not success:
                    # 如果失败，重启浏览器
                    if self.browser:
                        self.browser.quit()
                    self.browser = None
                    
                time.sleep(interval)
                
            except Exception as e:
                logging.error(f"运行出错: {str(e)}")
                if self.browser:
                    self.browser.quit()
                self.browser = None
                time.sleep(60)  # 出错后等待1分钟再重试

if __name__ == "__main__":
    import os
    
    # 创建数据保存目录
    if not os.path.exists('data'):
        os.makedirs('data')
        
    monitor = DyMonitor()
    monitor.run() 