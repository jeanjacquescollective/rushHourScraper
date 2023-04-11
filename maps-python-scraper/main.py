from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scrape import getLinks, scrapeDataFromLinks
app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/rushhours/{query}")
async def getRushhours(query: str):
    links = getLinks(query)
    data = scrapeDataFromLinks(links)
    return {'data': data}