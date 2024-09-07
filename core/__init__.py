from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse,JSONResponse
from .ai import *
from .config import Config 
config = Config()
import asyncio
from loguru import logger
from .db import MongoDB
app = APIRouter()
mongodb = MongoDB(config.mongo_host,config.mongo_port,config.mongo_db_name,config.mongo_collection_name,config.mongo_username,config.mongo_password)
@app.get("/get_desc")
def _():
    return JSONResponse(content={"msg": "请使用 POST 方法请求"},status_code=405)
@app.post("/get_desc")
async def _(request: Request):
    referer = request.headers.get('Referer', '-')
    if referer in config.auth_referer_whilelist:
        data = await request.form()
        if data.get("api_key") != config.auth_key:
            return PlainTextResponse("invalid api key",status_code=403)
        title = data.get("title")
        text = data.get("text")
        cache = mongodb.find_one({"title":title})
        if cache:
            return {"title":title,"desc": cache.get("desc",""),"cache": True}
        else:
            zy = await get_ai_response(title,text)
            if "Error" not in zy:
                asyncio.create_task(mongodb.insert_one({"title":title,"text":text,"desc":zy}))
            else:
                logger.info(f"摘要获取失败，不进行缓存，{zy}")
            return {"title":title,"desc":zy,"cache": False}
    else:
        return PlainTextResponse("invaild referer header", status_code=403)