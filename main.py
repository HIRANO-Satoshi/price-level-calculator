'''
Luncho server

@author HIRANO Satoshi
@date  2020/02/28
'''

dummy: str

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS
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
async def convert_from_luncho(currency_code: str, luncho_value: float):
    ppp = 1.0
    if currency_code == 'USD':
        ppp = 4.81
    elif currency_code == 'JPY':
        ppp = 530
    elif currency_code == 'EURO':
        ppp = 4.40
    elif currency_code == 'CNY':
        ppp = 33.92

    return {"currency_value": luncho_value * ppp}
