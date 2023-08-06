# Copyright 2020 @ Max Planck Gesellschaft

import os
from lightargs import lightcoloring as lc


def _check_class(name,class_):
    if not isinstance(name,class_):
        error = str("operation {} "+
                    "should be a {} (it is a  {})")
        raise TypeError(error.format(name,class_,name.__class__))


class FileExists:

    def __init__(self):
        pass
        
    def __str__(self):
        return "checks if the file exists"

    def help(self):
        return str(self)
        
    def check(self,value):
        if not os.path.isfile(value):
            raise ValueError("{} could not be found",value)
        if not os.access(value,os.R_OK):
            raise ValueError("{} is not readable",value)


class Positive:

    def __init__(self):
        pass

    def __str__(self):
        return "value must be positive"

    def help(self):
        return str(self)

    def check(self,value):
        try :
            ok = value>=0
        except TypeError:
            raise ValueError("{} could not be compared with 0",value)
        if not ok:
            raise ValueError("{} must be positive",value)

        
class Range:

    def __init__(self,min_v,max_v):
        self._min_v = min_v
        self._max_v = max_v

    def __str__(self):
        return repr([self._min_v,self._max_v])

    def help(self):
        s = "value should be between {} and {}"
        return s.format(self._min_v,self._max_v)
        
    def check(self,value): 
        try :
            smaller = value < self._min_v
        except:
            error = str("failed to compare value {}"+
                        " with range {}")
            raise ValueError(error.format(value,str(self)))
        if smaller:
            error = str("value {} is too small "+
                        "(range:{})")
            raise ValueError(error.format(value,str(self)))
        try :
            bigger = value > self._max_v
        except:
            error = str("failed to compare value {}"+
                        " with range {}")
            raise ValueError(error.format(value,str(self)))
        if bigger:
            error = str("value {} is too big "+
                        "(range:{})")
            raise ValueError(error.format(value,str(self)))

        
class Set:
    
    def __init__(self,*authorized):
        self._authorized = authorized

    def __str__(self):
        return ",".join([str(a) for a in self._authorized])

    def help(self):
        return "value should be in: {}".format(str(self))
    
    def check(self,value):
        if value not in self._authorized:
            error = str("{} not in authorized values ({})")
            raise ValueError(error.format(value,str(self)))

        
class BrightArgs:

    help_args = ("-h","help","-help","--h","--help")
    
    def __init__(self,help_str):
        self._help = help_str
        self._helps = {}
        self._classes = {}
        self._integrity_checks = {}
        self._options = set()
        self._operations = set()
        self._defaults = {}

    def _get_str(self,enum):
        r = ["\n"]
        args = sorted(self._options.union(self._operations))
        for index,arg in enumerate(args):
            if enum :
                r.append("\t{} | {}:\t{}".format(lc.format(str(index),lc.bright,lc.green),
                                                 arg,
                                                 lc.format(getattr(self,arg),lc.bright)))
            else:
                r.append("\t{}:\t{}".format(arg,getattr(self,arg)))
        r.append("\n")
        return "\n".join(r)

    def __str__(self):
        return self._get_str(enum=False)
    
    def _dialog_operation(self,name):
        s = self._str_operation_help(name)
        print(s)
        value = None
        while value is None:
            value = input(lc.format("\t\tuse ? (y, n, default:n): ",lc.bright))
            value = value.lower()
            value = value.strip()
            if value in ('y','n'):
                if value=='y':
                    return True
                if value=='n':
                    return False
            if value=='':
                return False

    def _dialog_option(self,name):
        formating = (lc.bright,lc.red)
        s = self._str_option_help(name)
        print(s)
        value = None
        while value is None:
            value = input(lc.format("\t\tenter value (default:{}): ",
                                    (self._defaults[name],lc.bright,lc.green),
                                    default=lc.bright))
            value = value.strip()
            if value=='':
                value = self._defaults[name]
                return value
            try :
                value = self._cast(name,value)
            except ValueError as e:
                print(lc.format("\t\t\t"+str(e),*formating))
                value = None
            if value is not None:
                try :
                    self._check_integrity(name,value)
                    return value
                except ValueError as e:
                    print(lc.format("\t\t\tvalue {} was not accepted: {}",
                                    (value,*formating),
                                    (str(e),*formating),
                                    default=formating))
                    value=None
        return None

    def _dialog_propose_defaults(self):
        def _is_bool(v):
            if type(v)==type(True):
                return True
        def _is_int(v):
            if type(v)==type(1):
                return True
        def _change_value(index):
            args = sorted(self._options.union(self._operations))
            arg = args[index]
            if arg in self._options:
                value = self._dialog_option(arg)
                self._set_option_value(arg,value)
            else:
                value = self._dialog_operation(arg)
                self._set_operation_value(arg,value)
        def _get_value():
            print(self._get_str(True))
            value = input(lc.format("\t\tuse these values ? ['y', index to change, 'h' for help]: ",
                                    lc.bright))
            value = value.strip()
            value = value.lower()
            if value=='y':
                return True
            if value=='h':
                return False
            try:
                index = int(value)
            except:
                raise ValueError(str(value))
            if index<0 or index>=(len(self._options)+len(self._operations)):
                raise ValueError(index)
            return index
        while True:
            try :
                v = _get_value()
            except ValueError as e:
                print(lc.format("\t\t\tinvalid value: {}, accepted values: {}",
                                (e,lc.bright),
                                ("'y','h',index (int)",lc.bright),
                                default=lc.red))
                continue
            except KeyboardInterrupt as ki:
                raise ki
            if _is_int(v):
                print("\n")
                _change_value(v)
            else:
                if v:
                    return v
                else:
                    print()
                    self.print_help()
                
    def dialog(self,change_all,args=None):
        if args :
            try :
                done = self.parse(args)
                if not done:
                    return False
            except ValueError as e:
                print()
                print(lc.format(e,lc.bright,lc.red))
                print()
                return False
            return True
        if change_all:
            for option in self._options:
                value = self._dialog_option(option)
                self._set_option_value(option,value)
                print("\n")
            for operation in self._operations:
                value = self._dialog_operation(operation)
                self._set_operation_value(operation,value)
                print("\n")
            return True
        else:
            try :
                self._dialog_propose_defaults()
            except KeyboardInterrupt:
                return False
            return True
                
    def _check_duplicate(self,arg_type,name):
        if name in self.help_args:
            error = str("{} is reserved and can not be used".format(name))
        if name in self._helps:
            error = str("{} {} added more than once")
            raise ValueError(error.format(arg_type,name))
        
    def _check_valid(self,arg_type,name):
        if not hasattr(self,name):
            error = str("{} is not a known {}")
            raise ValueError(error.format(name,arg_type))

    def _is_operation(self,arg):
        if arg.startswith("--"):
            if arg[2:] in self._operations:
                return arg[2:]
        return False

    def _is_option(self,arg):
        if arg.startswith("--"):
            return False
        if arg.startswith("-"):
            if arg[1:] in self._options:
                return arg[1:]
        return False

    def _cast(self,name,value):
        try:
            value = self._classes[name](value)
            return value
        except:
            error = "failed to cast {} to {} (option {})"
            raise ValueError(error.format(value,
                                          self._classes[name],name))
    
    def _check_integrity(self,name,value):
        checks = self._integrity_checks[name]
        if not checks:
            return
        for check in checks:
            check.check(value)
    
    def add_operation(self,name,help_str):
        _check_class(name,str)
        self._check_duplicate("operation",name)
        setattr(self,name,False)
        self._helps[name]=str(help_str)
        self._operations.add(name)
        self._integrity_checks[name]=None
        
    def add_option(self,name,default,help_str,class_,
                   integrity_checks=[]):
        _check_class(name,str)
        self._check_duplicate("option",name)
        setattr(self,name,default)
        self._helps[name]=str(help_str)
        self._classes[name]=class_
        self._integrity_checks[name]=integrity_checks
        self._options.add(name)
        self._defaults[name]=default
        
    def _set_operation_value(self,name,value):
        if not isinstance(value,bool):
            error = "{} should be set a boolean value ({} is {})"
            raise ValueError(error.format(name,value,value.__class__))
        setattr(self,name,value)
        
    def _set_option_value(self,name,value):
        value = self._cast(name,value)
        self._check_integrity(name,value)
        setattr(self,name,value)

    def _complain_unknown(self,unknown):
        error = "unkown argument: {}.\nKnown arguments: {}"
        known_options = ", ".join(["-"+o for o in self._options])
        known_operations = ", ".join(["--"+o for o in self._operations])
        known_arguments = ", ".join([known_options,known_operations])
        raise ValueError(error.format(unknown,known_arguments))
        
    def _parse_single(self,args,index):
        operation = self._is_operation(args[index])
        if operation:
            self._set_operation_value(operation,True)
            return False # do not skip next argment
        option = self._is_option(args[index])
        if option:
            if index>=len(args):
                error = "failed to read value for option {}"
                raise ValueError(error.format(option))
            value = args[index+1]
            self._set_option_value(option,value)
            return True # skip next argument (value of the option)
        self._complain_unknown(args[index])
        
    def parse(self,args):
        if any([arg in self.help_args for arg in args]):
            self.print_help()
            return False
        skip=False
        for index in range(len(args)):
            if skip:
                skip=False
            else:
                skip = self._parse_single(args,index)
        return True
                
    def _str_option_help(self,name):
        name_str = "-"+name
        s = str("\t\t{} ({}, default:{})\t{}{}")
        class_ = str(self._classes[name])
        if "'" in class_:
            class_ = class_[class_.find("'")+1:class_.rfind("'")]
        default = self._defaults[name]
        help_ = self._helps[name]
        if help_ is None:
            help_ = ""
        integrity_str = self._integrity_checks_str(name)
        return lc.format(s,
                         (name_str,lc.green,lc.bright),
                         (class_,lc.cyan,lc.dim),
                         (default,lc.cyan,lc.dim),
                         (help_,lc.bright),
                         (integrity_str,lc.cyan,lc.dim),
                         default=(lc.cyan,lc.dim))
    
    def _print_option_help(self,name):
        s = self._str_option_help(name)
        print(s)
        
    def _integrity_checks_str(self,name):
        integrity_checks = self._integrity_checks[name]
        if not integrity_checks :
            return ""
        r = ["\t\t\t\t"]
        for ic in integrity_checks:
            r.append(ic.help())
        return "\n\t\t\t\t".join(r)
        
    def _str_operation_help(self,name):
        name_str = "--"+name
        s = str("{}\t{}")
        help_ = self._helps[name]
        if help_ is None:
            help_ = ""
        return lc.format(s,
                         (name_str,lc.green,lc.bright),
                         (help_,lc.bright))

    def _print_operation_help(self,name):
        s = self._str_operation_help(name)
        print("\t\t"+s)
        
    def print_help(self):
        if self._help :
              print(lc.format("\n\t{}\n",(self._help,lc.bright)))
        else:
              print("\n")
        for operation in self._operations:
            self._print_operation_help(operation)
        for option in self._options:
            self._print_option_help(option)
        print()

    def print_status(self):
        print(str(self))
