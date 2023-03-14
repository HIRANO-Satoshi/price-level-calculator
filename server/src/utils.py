'''
  Utility functions

  Created on 2021/05/12

  @author HIRANO Satoshi
'''

import logging
from typing import Any
from fastapi import HTTPException

def error(value: Any, msg: str) -> None:
    ''' log an error and raises HTTP 400 exception. '''

    log_msg: str = '{msg: ' + msg if msg else ''
    log_msg += ', value: ' + str(value) if value else ''
    log_msg += '}'
    logging.warning(log_msg)
    raise HTTPException(status_code=400, detail=msg)
