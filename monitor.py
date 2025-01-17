import requests
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
        # 添加API基础URL
        self.api_base_url = 'http://localhost:8000'  # 根据实际情况修改
        
    def start_browser(self):
        try:
            if self.browser is None:
                self.browser = Chromium(addr_or_opts=self.co)
            logging.info("浏览器启动成功")
        except Exception as e:
            logging.error(f"浏览器启动失败: {str(e)}")
            raise e

    def get_and_send_data(self):
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
            
            # 准备发送到后端的数据
            storage_data = json.loads(window_data.text) if window_data and window_data.text else {}
            
            # 发送cookies到后端
            cookie_payload = {
                "domain": "buyin.jinritemai.com",
                "username": "default_user",  # 可以根据需要修改
                "cookie_data": cookies
            }
            
            # 发送storage数据到后端
            storage_payload = {
                "domain": "buyin.jinritemai.com",
                "username": "default_user",  # 可以根据需要修改
                "cookie_data": storage_data  # 这里复用了cookie_data字段
            }
            
            # 调用后端API
            cookies_response = requests.post(
                f"{self.api_base_url}/chrome/save-cookies",
                json=cookie_payload
            )
            storage_response = requests.post(
                f"{self.api_base_url}/chrome/save-storage",
                json=storage_payload
            )
            
            if cookies_response.status_code == 200 and storage_response.status_code == 200:
                logging.info("数据成功发送到后端")
                return True
            else:
                logging.error(f"发送数据失败: Cookies状态码 {cookies_response.status_code}, Storage状态码 {storage_response.status_code}")
                return False
                
        except Exception as e:
            logging.error(f"数据获取或发送失败: {str(e)}")
            return False

    def run(self, interval=10):  # 修改默认间隔为10秒
        while True:
            try:
                if self.browser is None:
                    self.start_browser()
                
                success = self.get_and_send_data()
                if not success:
                    # 如果失败，重启浏览器
                    if self.browser:
                        self.browser.quit()
                    self.browser = None
                    time.sleep(60)  # 失败后等待1分钟再重试
                else:
                    time.sleep(interval)  # 成功后等待10秒
                
            except Exception as e:
                logging.error(f"运行出错: {str(e)}")
                if self.browser:
                    self.browser.quit()
                self.browser = None
                time.sleep(60)  # 出错后等待1分钟再重试

if __name__ == "__main__":
    monitor = DyMonitor()
    monitor.run() 