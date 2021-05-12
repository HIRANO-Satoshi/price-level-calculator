'''
 Configuration of the Luncho server

 Author: HIRANO Satoshi
 Date: 2021/05/12
'''

def Header_To_Fetch(lang: str) -> str:
    return {"Accept-Language": "".join([lang, ";"]), "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}
