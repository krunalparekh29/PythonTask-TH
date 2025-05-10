import pip
import subprocess
import sys

def install(name, ver):
    subprocess.call([sys.executable, '-m', 'pip', 'install', f'{name}=={ver}'])
    import requests
    if requests.__version__ != ver:
        print('Version missmatch')
    else:
        print('Module imported successfully')


version = input('provide version of requests: ')

install('requests',version)