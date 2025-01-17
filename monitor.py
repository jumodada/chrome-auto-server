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
        self.api_base_url = 'http://127.0.0.1:8000/api'  # 根据实际情况修改
        
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
            
            cookies = tab.cookies()
            if not cookies:
                logging.warning("未获取到cookie数据")
                return False
            
            tab.console.start()
            window_data = tab.local_storage()
            if not window_data or not window_data:
                logging.warning("未获取到localStorage数据")
                return False
                
            cookie_payload = {
                "domain": "buyin.jinritemai.com",
                "username": "default_user",
                "cookie_data": cookies
            }
            storage_payload = {
                "domain": "buyin.jinritemai.com",
                "username": "default_user",
                "storage_data": window_data
            }
            print(  f"{self.api_base_url}/chrome/save-cookies")
            cookies_response = requests.post(
                f"{self.api_base_url}/chrome/save-cookies",
                json=cookie_payload
            )
            print(cookies_response.connection)
            storage_response = requests.post(
                f"{self.api_base_url}/chrome/save-storage",
                json=storage_payload
            )
            if cookies_response.status_code == 200 and storage_response.status_code == 200:
                logging.info("数据成功发送到后端")
                logging.info(f"Cookie数据大小: {len(str(cookies))} bytes")
                logging.info(f"Storage数据大小: {len(str(window_data))} bytes")
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
                    time.sleep(10)  # 失败后等待1分钟再重试
                else:
                    time.sleep(interval)  # 成功后等待10秒
                
            except Exception as e:
                logging.error(f"运行出错: {str(e)}")
                if self.browser:
                    self.browser.quit()
                self.browser = None
                time.sleep(10)  # 出错后等待1分钟再重试

if __name__ == "__main__":
    monitor = DyMonitor()
    monitor.run() 