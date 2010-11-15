import re

def construct_keyname(param):
    # clean non aplhanumeric 
    param = re.sub('[^\w\s]', '', param)
    
    # replace space with dash
    return param.replace(' ','-')