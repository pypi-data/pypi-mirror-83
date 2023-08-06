import pandas as pd
import math
def rmnan(arr):
    cleanedset = arr
    rmarr = list()
    for i in range(len(cleanedset)):
        if math.isnan(cleanedset[i]):
            rmarr.append(i-len(rmarr))
    for i in rmarr:
        cleanedset.pop(i)
    return cleanedset

def mean(arr):
    return sum(arr)/len(arr)

def median(arr):
    arr = sort(arr)
    return (arr[math.ceil(len(arr)/2)]+arr[math.floor(len(arr)/2)])/2

def vartype(arr):
    catquant = list()
    for i in range(len(arr[0])):
        if(type(arr[0][i]) == int):
            catquant.append("Quantitative")
        elif(type(arr[0][i]) == float):
            catquant.append("Quantitative")
        else:
            catquant.append("Categorical")
    return catquant

def stdev(arr):
    avg = mean(arr)
    total = 0;
    for i in arr:
        total += math.pow(i-avg,2)
    return math.sqrt(total/(len(arr)-1))

def IQR(arr):
    arr = sort(arr)
    q1 = (arr[math.ceil(len(arr)/4)]+arr[math.floor(len(arr)/4)])/2
    q3 = (arr[math.ceil(3*len(arr)/4)]+arr[math.floor(3*len(arr)/4)])/2
    return q3-q1;

def split(arr):
    arr1 = list()
    arr2 = list()
    for i in range(0,int(len(arr)/2)):
        arr1.append(arr[i])
    for i in range(int(len(arr)/2),len(arr)):
        arr2.append(arr[i])
    return arr1, arr2

def merge(arr1, arr2):
    for i in arr2:
        for j in range(len(arr1)):
            if(arr1[j]>i):
                arr1.insert(j,i)
    return arr1

def sort(arr):
    if len(arr) == 1:
        return arr
    a, b = split(arr)
    return merge(sort(a),sort(b))

def favstats(arr):
    q1 = (arr[math.ceil(len(arr)/4)]+arr[math.floor(len(arr)/4)])/2
    q3 = (arr[math.ceil(3*len(arr)/4)]+arr[math.floor(3*len(arr)/4)])/2
    med = median(arr)
    return [min(arr),q1,med,q3,max(arr)]

def quantile(arr,num=4):
    arr = sort(arr)
    out = list();
    for i in range(num):
        print(arr[int(len(arr)*i/num)])
        out.append(arr[int(len(arr)*i/num)])
    out.append(arr[len(arr)-1])
    return out