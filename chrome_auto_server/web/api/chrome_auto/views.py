from fastapi import APIRouter
from DrissionPage import Chromium, ChromiumOptions
router = APIRouter()
co = ChromiumOptions().set_browser_path(r'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
# 用该配置创建页面对象
browser = Chromium(addr_or_opts=co)
@router.post("/start-browser")
async def start_browser():
    """
    启动Chrome浏览器的API端点
    """
    try:
        tab = browser.latest_tab  
        tab.get(url='https://buyin.jinritemai.com/dashboard') 
        html = '<a href="https://DrissionPage.cn" target="blank">DrissionPage </a> '
        ele = tab.add_ele(html)  # 插入到导航栏
        ele.click('js')
        return {
            "success": True,
            "message": "浏览器启动成功"
        }
    
    except Exception as e:
        print(e)
        return {
            "success": False,
            "message": f"浏览器启动失败: {str(e)}"
        } 