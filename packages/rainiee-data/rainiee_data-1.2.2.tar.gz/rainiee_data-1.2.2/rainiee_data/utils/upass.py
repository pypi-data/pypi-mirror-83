# -*- coding:utf-8 -*-
import os

TOKEN_F_P = 'rainiee_data.token'

def set_token(token):
    user_home = os.path.expanduser('~')
    with open(user_home + TOKEN_F_P, 'w') as f:
        f.write(token)

def get_token():
    user_home = os.path.expanduser('~')
    with open(user_home+TOKEN_F_P, 'r') as f1:
        return f1.readline()
