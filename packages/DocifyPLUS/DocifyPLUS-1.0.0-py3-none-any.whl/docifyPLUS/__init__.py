### DOCUMENTATION           ###
"""
A module containing objects for documentating Lambdas, Fucntions, Methods, etc.
"""
### DOCUMENTATION           ###
### IMPORTS                 ###
    ## Dependencies             ##
    ## Dependencies             ##
### IMPORTS                 ###
### CONSTANTS               ###
_LAMBDA = type(lambda: "hello")     # Lambda Type
### CONSTANTS               ###
### FUNCS                   ###
def document(obj: "Object (Lambda, Function, Method, Decorator, ...)", doc: "Documentation"):
    """
    Function for non-dynamic documentation
    """
    try: obj.__doc__ = doc
    except AttributeError as E:
        print("""
        Builtin Python Datatypes including but not limited to (int, float str, bool, None)
        Are not able to have doc-strings
        """)
### FUNCS                   ###