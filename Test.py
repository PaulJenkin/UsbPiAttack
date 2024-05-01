import re
import sys

def _create_shift_arr(step):
    shift = ['\n']
    ix = 0
    space = ' '*step if type(step) is int else step
    while ix < 100:
        shift.append(shift[ix]+space)
        ix = ix + 1
    return shift;

def Formatxml(text, step=4):
    ar = re.sub('>\s{0,}<', "><", text)
    ar = re.sub('<', "~::~<", ar)
    ar = re.sub('\s*xmlns\:', "~::~xmlns:", ar)
    ar = re.sub('\s*xmlns\=', "~::~xmlns=", ar)
    ar = ar.split('~::~')
    length = len(ar)
    inComment = False
    deep = 0
    str = ''
    ix = 0
    shift = _create_shift_arr(step)
    while ix < length:
        if re.search('<!', ar[ix]):
            str += shift[deep] + ar[ix]
            inComment = True
            if (re.search('-->', ar[ix]) or
                re.search('\]>', ar[ix]) or
                re.search('!DOCTYPE',ar[ix])
                ):
                inComment = False
        elif re.search('-->',ar[ix]) or re.search('\]>',ar[ix]):
            str += ar[ix]
            inComment = False
        elif ( re.search(r'^<\w',ar[ix-1]) and
               re.search(r'^</\w', ar[ix]) and
               (
                 re.search('^<[\w:\-\.\,]+',ar[ix-1]).group(0) ==
                 re.sub('/','', re.search(r'^</[\w:\-\.\,]+', ar[ix]).group(0))
                )
            ):
            str += ar[ix]
            if not inComment:
                deep -= 1
        elif (re.search('<\w',ar[ix]) and not re.search('<\/',ar[ix])
                                      and not re.search('\/>', ar[ix])):
            if not inComment:
                str += shift[deep]+ar[ix]
                deep += 1
            else:
                str += ar[ix]
        elif re.search('<\w', ar[ix]) and re.search(r'</',ar[ix]):
            str = str + shift[deep]+ar[ix] if not inComment else str + ar[ix]
        elif re.search(r'</', ar[ix]):
            if not inComment:
                deep -= 1
                str += shift[deep]+ar[ix]
            else:
                str += ar[ix]
        elif re.search('\/>', ar[ix]):
            str = str + shift[deep]+ar[ix] if not inComment else str + ar[ix]
        elif re.search('<\?', ar[ix]):
            str += shift[deep]+ar[ix]
        elif re.search('xmlns\:', ar[ix]) or re.search('xmlns\=',ar[ix]):
            str += shift[deep]+ar[ix];
        else:
            str += ar[ix];
        ix += 1
    return str[1:] if str[0] in ['\n','\r'] else str


def xpathToRegX(strPath):
    while strPath.startswith('/'):
        strPath=strPath[1:]
    xpath="<{}<{}>.*?</{}>".format(strPath[:strPath.rfind('/')+1].replace('/','.*?').replace('[','.*?').replace("='",'>').replace("'",'<').replace("'",'').replace("]",''),strPath[strPath.rfind('/')+1:],strPath[strPath.rfind('/')+1:])
    RegXOpenStr=""
    for ele in xpath.split('.*?'):
        RegXOpenStr+=ele
        if ele.endswith('<'):
            RegXOpenStr+="/{}".format(ele[:ele.find('>')])
        RegXOpenStr+='.*?'
    RegXOpenStr=RegXOpenStr[:-3]
    while strPath.count('[') and strPath.count(']'):
        strPath=strPath.replace(strPath[strPath.find('['):strPath.find(']')+1],'')
    splitTg=strPath.split('/')
    splitTg.reverse()
    xpathClose=""
    for tg in splitTg[1:]:
        xpathClose+="</{}>.*?".format(tg)
    return RegXOpenStr,xpathClose[:-3]

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

def xmlGetText(xmlText,xpath):
    rtVal=None
    try:
        RegXOpenStr,RegXCloseStr=xpathToRegX(xpath)
        RegXVerify="{}.*?{}".format(RegXOpenStr,RegXCloseStr)
        ChkMtchLst=re.findall(RegXVerify,xmlText,re.S)
        if len(ChkMtchLst):
            DtMtchLst=re.findall(RegXOpenStr,xmlText,re.S)
            TageName=xpath[xpath.rfind('/')+1:]
            TagStart="<{}>".format(TageName)
            TagEnd="</{}>".format(TageName)
            FullTag=DtMtchLst[-1][DtMtchLst[-1].rfind(TagStart):]
            FinalValue=FullTag.replace(TagStart,'').replace(TagEnd,'').strip()
            if FinalValue.count('<') and FinalValue.count('>'):
                print("Not an Element")
            else:
                rtVal=FinalValue
    except Exception as e:
            print(str(e))
            raise
    return rtVal

def xmlPutText(xmlText,xpathValueArray):
    try:
        for xpathValue in xpathValueArray:
            RegXOpenStr,RegXCloseStr=xpathToRegX(xpathValue[0])
            RegXVerify="{}.*?{}".format(RegXOpenStr,RegXCloseStr)
            ChkMtchLst=re.findall(RegXVerify,xmlText,re.S)
            if len(ChkMtchLst):
                DtMtchLst=re.findall(RegXOpenStr,xmlText,re.S)
                TageName=xpathValue[0][xpathValue[0].rfind('/')+1:]
                TagStart="<{}>".format(TageName)
                TagEnd="</{}>".format(TageName)
                FullTag=DtMtchLst[-1][DtMtchLst[-1].rfind(TagStart):]
                FinalValue=FullTag.replace(TagStart,'').replace(TagEnd,'').strip()
                if FinalValue.count('<') and FinalValue.count('>'):
                    print("Not an Element")
                else:
                    dtWithoutTag=DtMtchLst[-1][:DtMtchLst[-1].rfind(TagStart)+1]
                    NewDtToAdd="{}{}{}".format(TagStart,xpathValue[1],TagEnd)
                    ModDt=dtWithoutTag+NewDtToAdd
                    xmlText=xmlText.replace(DtMtchLst[-1],ModDt)
            else:
                raise
    except Exception as e:
            print(str(e))
            raise
    return xmlText
