'''
  Utility functions

  Created on 2021/05/12

  Author: HIRANO Satoshi
'''

import logging
from typing import Type, Optional, List, Dict #, Tuple, Union, Any, Generator, cast
from mypy_extensions import TypedDict
from fastapi import FastAPI, HTTPException

def error(value: any, msg: str) -> None:
    log_msg = '{msg: ' + msg if msg else ''
    log_msg += ', value: ' + str(value) if value else ''
    log_msg += '}'
    logging.warning(log_msg)
    raise HTTPException(status_code=400, detail=msg)
