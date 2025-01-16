from fastapi import APIRouter, Depends
from DrissionPage import Chromium, ChromiumOptions
from sqlalchemy.ext.asyncio import AsyncSession

from chrome_auto_server.db.dependencies import get_db_session
from chrome_auto_server.db.dao.cookie_dao import CookieDAO
from chrome_auto_server.web.api.chrome_auto.schemas import CookieCreate, CookieResponse

router = APIRouter()
co = ChromiumOptions().set_browser_path(r'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
# 用该配置创建页面对象
co.set_user_data_path(r'/Users/kunyunwu/Library/Application Support/Google/Chrome/Default')
browser = Chromium(addr_or_opts=co)

@router.post("/start-browser")
async def start_browser():
    try:
        tab = browser.latest_tab
        tab.get(url='https://buyin.jinritemai.com/dashboard') 
        tab.set_cookie(name='code', value='652c6ee708d2e4adz5HM24Fb4TDspeUQXtiR_hl')
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

@router.post("/save-cookies", response_model=CookieResponse)
async def save_cookies(
    cookie_data: CookieCreate,
    db: AsyncSession = Depends(get_db_session),
) -> CookieResponse:
    try:
        tab = browser.latest_tab
        cookies = tab.cookies()
        # 将CookiesList转换为字典列表
        
        
        dao = CookieDAO(db)
        await dao.create_cookie(
            domain=cookie_data.domain,
            username=cookie_data.username,
            cookie_data=cookies,
        )
        return CookieResponse(
            success=True,
            message="Cookie保存成功",
            data=cookies
        )
    except Exception as e:
        return CookieResponse(
            success=False,
            message=f"Cookie保存失败: {str(e)}"
        )

@router.get("/get-cookies/{domain}/{username}", response_model=CookieResponse)
async def get_cookies(
    domain: str,
    username: str,
    db: AsyncSession = Depends(get_db_session),
) -> CookieResponse:
    try:
        dao = CookieDAO(db)
        cookie = await dao.get_cookie(domain=domain, username=username)
        

        if not cookie:
            return CookieResponse(
                success=False,
                message="未找到对应的Cookie记录"
            )
            
        return CookieResponse(
            success=True,
            message="Cookie获取成功",
            data=cookie.cookie_data
        )
    except Exception as e:
        return CookieResponse(
            success=False,
            message=f"Cookie获取失败: {str(e)}"
        ) 

@router.get("/console-info")
async def get_console_info():
    try:
        tab = browser.latest_tab
        tab.console.start()  # 启动控制台监听
        
        
        js_code = '''
            console.log(JSON.stringify({
                indexedDB: window.indexedDB,
                localStorage: window.localStorage,
                BTM_MAP_DATA: window.BTM_MAP_DATA,
                pageList: window.pageList,
            }));
        '''
        tab.run_js(js_code)
        window_data = tab.console.wait()
        return {
            "success": True,
            "message": "控制台信息获取成功",
            "data": {
                 "window": window_data.text if window_data else None
            }
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"获取控制台信息失败: {str(e)}"
        } 