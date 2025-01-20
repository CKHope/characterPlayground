import pinyin
import pandas as pd 

dfChar=pd.read_pickle("01dfCharacterZFL_add_pinyinNumber.pkl")

def returnCharRadical(char:str):
    try:
        radical=dfChar[dfChar.character==char].radical.item()[0]
        return radical
    except:
        radical=char
        return radical