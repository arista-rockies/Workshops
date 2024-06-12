# this function uses the mako context to output a formatted string
#  for cvp to process the generated configuration it's important
#  that the string be newLine terminated.  rather than requiring
#  the user to specify that manually on every line we append it here
#  unless asked not to. this method of indenting will almost certainly
#  not behave as intended for complex types
def output(outStr: str, indent: int=2, level: int=0, flush: bool=True):
    # if the input is not a string, let's just use the default converter
    #  for whatevever it is and hope for the best.
    if not isinstance(outStr, str):
        outStr = f'{outStr}'
    if not outStr:
        return

    context.write(f'{outStr.rjust((indent*level)+len(outStr))}')
    if flush:
        context.write("\n")
