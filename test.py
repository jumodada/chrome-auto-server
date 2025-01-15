from DrissionPage import Chromium, ChromiumOptions
path = r'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'  # 请改为你电脑内Chrome可执行文件路径
co = ChromiumOptions().set_browser_path(path)
tab = Chromium(co).latest_tab
tab.get('https://DrissionPage.cn')
