# -*- coding: utf-8 -*-
import os,sys  
import string
 
def suanfa(key):
    alp = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    jiami_key = {}
    jiemi_key = {}
 
    list0 = list(alp)
    list1 = list(key)
    list2 = list(alp)
    for n in list1:
        for m in list2:
            if m == n:
                list2.remove(m)
 
    alp1 = ''.join(list2)
    key1 = key + alp1
    list3 = list(key1)
 
    a = 0
    if a < len(list0):
        for m in list0:
            jiami_key[m] = list3[a]
            a = a + 1
    
    b = 0
    if b < len(list3):
        for n in list3:
            jiemi_key[n] = list0[b]
            b = b + 1
    
    #print jiami_key
    #print jiemi_key
    return jiami_key, jiemi_key  
 
def bianma(key_dic, data):
    list_data = list(data)
    data1 = []
    for a in list_data:
         if a == ' ':
             data1.append(a)
 
         elif a.islower():
             a = a.upper()
             if key_dic.has_key(a):
                 x = key_dic[a]
                 data1.append(x.lower())
 
         elif a.isupper():
             if key_dic.has_key(a):
                 x = key_dic[a]
                 data1.append(x)
         else:
             data1.append(a)
 
    data2 = ''.join(data1)
    #print data2
    return data2
 
def main():
    key = 'ZDFKJMNX'
    data = 'a bdcd sFDGDSGFDG113243 3'
    print(key)    
    print(data) 
    jiami_key, jiemi_key = suanfa(key)
    miwen = bianma(jiami_key, data)
    mingwen = bianma(jiemi_key, miwen)
    
    print(miwen)
    print(mingwen)
    return True
 
if __name__ == "__main__":
    main() 
