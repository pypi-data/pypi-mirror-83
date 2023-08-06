### IMPORTS             ###
### IMPORTS             ###
### EXCEPTIONS          ###
class ArgumentException(Exception):
    def __init__(self, arg): super().__init__(
        f'{arg} is unrecognized. Please use "setup"'
    )
### EXCEPTIONS          ###