from fastapi import FastAPI

from controller.DataSourceApi import dataSourceApi
from controller.QueryDataApi import queryDataApi

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# 加载 dataSourceApi 接口
app.mount("/dataSource", dataSourceApi)
app.mount("/query", queryDataApi)
