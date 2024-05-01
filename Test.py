
import json
import sys
import re

import xmltodict
from functools import reduce
from operator import getitem

def xpathToRegX(strPath):
    while strPath.startswith('/'):
        strPath=strPath[1:]
    xpath="<{}</{}>".format(strPath[:strPath.rfind('/')+1].replace('/','.*'),strPath[strPath.rfind('/')+1:])
    return xpath

def NodeArrayFromXpath(xpath):
    while xpath.startswith('/'):
        xpath=xpath[1:]
    tags=[]
    Ch=""
    opSqBr=0
    for apCh in xpath:
        if apCh =='/' and opSqBr==0:
            tags.append(Ch)
            Ch=""
            continue
        if apCh=='[':
            opSqBr+=1
        if apCh==']':
            opSqBr-=1
        Ch+=apCh
    tags.append(Ch)
    return tags

def solveCondition(JSN,ConditionPath):
    pathStr=""
    CurrentJSN=JSN
    baseTag=ConditionPath[:ConditionPath.find('[')]
    SubNodes=NodeArrayFromXpath((ConditionPath[ConditionPath.find('[')+1:ConditionPath.find('=')]))
    SubNodes.insert(0,baseTag)
    CompareItem=ConditionPath[ConditionPath.find('=')+1:-1].replace("'",'').replace('"','')
    if isinstance(CurrentJSN,list):
        for k,rec in enumerate(CurrentJSN):
            unModrec=rec
            for tag in SubNodes[:-1]:
                if tag in rec:
                    rec=rec[tag]
            if SubNodes[-1] in rec.keys():
                if rec[SubNodes[-1]]==CompareItem:
                    return unModrec[baseTag],[k,baseTag]
    else:

        CurrentJSN=CurrentJSN[SubNodes[0]]
        if isinstance(CurrentJSN,list):
            for k,rec in enumerate(CurrentJSN):
                unModrec=rec

                for tag in SubNodes[1:-1]:
                    if tag in rec:
                        rec=rec[tag]
                if SubNodes[-1] in rec.keys():
                    if rec[SubNodes[-1]]==CompareItem:
                        return unModrec,[baseTag,k]
    if SubNodes[-1] in CurrentJSN.keys():
        if CurrentJSN[SubNodes[-1]]==CompareItem:
            return CurrentJSN,[baseTag]
    return None

def findValueByPath(JSN,PathArray):
    pthStrArray=[]
    CurrentJSN=JSN
    for tag in PathArray[:-1]:
        if tag.count('[')>0:
            CurrentJSN,Strpt=solveCondition(CurrentJSN,tag)
            pthStrArray+=Strpt
        elif tag in CurrentJSN.keys():
            pthStrArray.append(tag)
            CurrentJSN=CurrentJSN[tag]

    if isinstance(CurrentJSN,list):
        CurrentJSN=CurrentJSN[0]
        pthStrArray.append(0)
    if PathArray[-1] in CurrentJSN.keys():
        pthStrArray.append(PathArray[-1])
        return pthStrArray,CurrentJSN[PathArray[-1]]
    else:
        print('$$$$$$$$$$$$$$ Issue $$$$$$$$$$$')
        return None


def jsonPutTxt(dataDict, mapList, val):
    reduce(getitem, mapList[:-1], dataDict)[mapList[-1]] = val
    return dataDict

def jsonGetTxt(dataDict, mapList):
    for itm in mapList:
        dataDict=dataDict[itm]
    return dataDict

def xmlGetText(xmlText,xpath):
    rtVal=None
    try:
        JSN = xmltodict.parse(xmlText)
        NodeArray=NodeArrayFromXpath(xpath)
        if xpath.count('[')>0:
            NodeArray,rtVal=findValueByPath(JSN,NodeArray)
        else:
            rtVal=jsonGetTxt(dataDict, mapList)
    except Exception as e:
            print(str(e))
            raise
    return rtVal

def xmlPutText(xmlText,xpathValueArray):
    try:
        JSN = xmltodict.parse(xmlText)
        for xpathValue in xpathValueArray:
            if xpathValue[0].count('[')>0:
                NodeArray,rtVal=findValueByPath(JSN,NodeArrayFromXpath(xpathValue[0]))
            else:
                NodeArray=NodeArrayFromXpath(xpathValue[0])

            JSN=jsonPutTxt(JSN, NodeArray, xpathValue[1])
        xmlText=xmltodict.unparse(JSN, pretty=True)
    except Exception as e:
            print(str(e))
            raise
    return xmlText

def xmlAddNone(xmlText,xpathValueArray):
    try:
        for xpath,AddDt in xpathValueArray:
            regXpath=xpathToRegX(xpath)
            mtList=re.findall(regXpath,xmlText,re.S)
            if len(mtList):
                xmlText=xmlText.replace(mtList[0],"{}\n{}".format(mtList[0],AddDt))
        return xmlText
    except:
        raise
