"""
A module for chaining lambdas
"""
### IMPORTS                 ###
    ## Dependencies             ##
import docifyPLUS
    ## Dependencies             ##
### IMPORTS                 ###
### FUNCS                   ###
b = bind = binding = binding_lambda = lambda x, f=(lambda x: x): f(x)
    ## Documentation            ##
docifyPLUS.document(
    b, """
    Primary lambda for binding and chaining lambdas
    """
)
    ## Documentation            ##
### FUNCS                   ###