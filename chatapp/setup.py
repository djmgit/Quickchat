from cx_Freeze import setup,Executable

setup(name='QuickChat',
      version='1.1',
      description='Quick and easy chat',
      executables = [Executable("chatapp.py")])
