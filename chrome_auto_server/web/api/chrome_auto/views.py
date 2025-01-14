from fastapi import APIRouter
from DrissionPage import Chromium, ChromiumOptions
router = APIRouter()

@router.post("/start-browser")
async def start_browser():
    """
    启动Chrome浏览器的API端点
    """
    try:
        co = ChromiumOptions().set_browser_path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
        print(co)
        browser = Chromium(addr_or_opts=co)
        # 获取标签页对象
        tab = browser.latest_tab  
        tab.get('https://www.baidu.com') 
        
        return {
            "success": True,
            "message": "浏览器启动成功"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"浏览器启动失败: {str(e)}"
        } 