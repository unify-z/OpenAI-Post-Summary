from fastapi import FastAPI
from core import app as base_router
from core.db import MongoDB
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.ai import get_ai_response
from core.config import Config
from loguru import logger
import secrets
import yaml
import os
from datetime import datetime
config = Config()
import asyncio
app = FastAPI()
app.include_router(base_router,prefix="/v1")

mongodb = MongoDB(config.mongo_host,config.mongo_port,config.mongo_db_name,config.mongo_collection_name,config.mongo_username,config.mongo_password)
async def auto_update_desc_cache():
    all_docs = mongodb.find_all()
    for doc in all_docs:
        _id = str(doc.get("_id"))
        logger.info(f"正在更新id {_id} 的摘要缓存")
        text = doc.get("text")
        result = await get_ai_response(text)
        mongodb.update_one(
            {"_id": doc.get("_id")},
            {"$set": {"desc": result}}
        )
@app.middleware("http")
async def _(request,call_next):
    start_time = datetime.now()
    response = await call_next(request)
    process_time = (datetime.now() - start_time).total_seconds()
    response_size = len(response.body) if hasattr(response, 'body') else 0
    referer = request.headers.get('Referer')
    user_agent = request.headers.get('user-agent', '-')
    logger.info(
        f"Serve {response.status_code} | {process_time:.2f}s | {response_size}B | "
        f"{request.client.host} | {request.method} {request.url.path} | \"{user_agent}\" | \"{referer}\""
    )
    
    return response
async def main():
    import uvicorn
    scheduler = AsyncIOScheduler()
    scheduler.add_job(auto_update_desc_cache, 'interval', hours=24)
    scheduler.start()
    uvicorn_config = uvicorn.Config(app, host=config.web_host, port=config.web_port,access_log=False,log_level="warning")
    server = uvicorn.Server(uvicorn_config)
    logger.info(f"Server is running on {config.web_host}:{config.web_port}")
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())