import colorama
colorama.init()

blue = colorama.Fore.BLUE
red = colorama.Fore.RED
orange = colorama.Fore.YELLOW
cyan = colorama.Fore.CYAN
green  = colorama.Fore.GREEN

bright = colorama.Style.BRIGHT
dim = colorama.Style.DIM

_fores = (blue,red,orange,cyan,green)
_styles = (bright,dim)
_reset = colorama.Style.RESET_ALL


def _format_single(s,modes):
    if modes is None:
        return s
    return "".join(list(modes)+[str(s)]+[_reset])

def _format(s,tuples,default):
    parts = s.split("{}")
    a = []
    for part,t in zip(parts,tuples):
        if default is None:
            a.append(part)
        else :
            a.append(_format_single(part,default))
        a.append(_format_single(t[0],t[1:]))
    if len(parts)>len(tuples):
        for part in parts[len(tuples):]:
            if default is None:
                a.append(part)
            else :
                a.append(_format_single(part,default))
    return "".join(a)

# s = lc.format("a",red,dim)
# s = lc.format("a: {} , {}",("b",red,dim),("c",blue),default=dim)
def format(s,*args,default=None):
    if default is not None:
        if default in _fores or default in _styles:
            default = (default)
    if not args:
        return _format_single(s,default)
    if isinstance(args[0],tuple):
        return _format(s,args,default)
    return _format_single(s,args)
    
