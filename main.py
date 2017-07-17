
import sys
import os
import types
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import ObeuBonn

def hello_world():
    print('from ObeuBonn')

if __name__ == '__main__':
    hello_world()
    print([a for a in dir(ObeuBonn) if isinstance(ObeuBonn.__dict__.get(a), types.FunctionType)])


