#!/usr/local/bin/pypy3
'''
  Luncho server

  @author HIRANO Satoshi
  @date  2020/02/28
'''

#import pdb
#import logging
import sys
import json
#from typing import List, Dict, Tuple, Union, Any, Type, Generator, Optional, ClassVar, cast

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi_utils.openapi import simplify_operation_ids
from starlette.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Luncho server converts between local currency and Universal Luncho index for the economic inequality problem",
    description="With 100 Luncho, you can have simple lunch in every country.",
    version="0.0.1"
)

#pylint: disable=wrong-import-position
from src import api       # initialize routes
from src import ppp_data

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

# use method names in OpenAPI operationIds to generate methods with the method names
simplify_operation_ids(app)

# static files in static dir
#app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    # command line
    if len(sys.argv) == 2 and sys.argv[1] == 'gen':
        print(api.gen_openapi_schema())
else:

    # initialize Lunch server
    ppp_data.init()
