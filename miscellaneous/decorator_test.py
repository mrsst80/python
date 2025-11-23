#!/usr/bin/env python3.12
import functools
import inspect

def log(d):
   def decor(func):
     def inner_function(*args):
       args_for_log = ','.join(map(str, args))
       d.write("LOG: {}({})\n".format(func.__name__,args_for_log))
       print("LOG: {}{}".format(func.__name__,args))
       #return my
     return inner_function
   return decor

f = open("decorator.log",'a')
@log(f)
def my_max(a,b,c):
  return max(a, b, c)
 
my_max(1,2,3)

f.close()
