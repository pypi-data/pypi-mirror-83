# THIS FILE IS GENERATED FROM PADDLEPADDLE SETUP.PY
#
full_version    = '2.0.0-rc0'
major           = '2'
minor           = '0'
patch           = '0-rc0'
rc              = '0'
istaged         = True
commit          = '97227e6d508a8f152c2f8dae05fc8432c45748a3'
with_mkl        = 'OFF'

def show():
    if istaged:
        print('full_version:', full_version)
        print('major:', major)
        print('minor:', minor)
        print('patch:', patch)
        print('rc:', rc)
    else:
        print('commit:', commit)

def mkl():
    return with_mkl
