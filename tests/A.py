# -*- coding: utf-8 -*-


class A(object):
    def __init__(self):
        self.A = "aa"
        self.C = "CC"
        del self.C

    def __setattr__(self, name, value):
        '''
        @summary: 每当属性被赋值的时候都会调用该方法，因此不能在该方法内赋值 self.name = value 会死循环
        '''
        print "__setattr__:Set %s Value %s" % (name, value)
        self.__dict__[name] = value

    def __getattr__(self, name):
        '''
        @summary: 当访问不存在的属性时会调用该方法
        '''
        print "__getattr__:No attribute named '%s'" % name
        return None

    def __delattr__(self, name):
        '''
        @summary: 当删除属性时调用该方法
        '''
        print "__delattr__:Delect attribute '%s'" % name
        del self.__dict__[name]
        print self.__dict__


if __name__ == "__main__":
    X = A()
    a = X.aa
    print "=============="
    b = X.A
    print b
