
def deconstruct(Object,*keys):
    newDict = dict([param for param in Object.items() if param[0] in keys])
    return newDict

