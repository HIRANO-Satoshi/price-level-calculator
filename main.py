from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*", # "http://localhost:8082",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/convert-from-luncho/")
async def read_item(currency_code: str, luncho_value: float):
    ppp = 1.0
    if currency_code == 'USD':
        ppp = 4.81
    elif currency_code == 'JPY':
        ppp = 530
    elif currency_code == 'EURO':
        ppp = 4.40

    return {"currency_value": luncho_value * ppp}
