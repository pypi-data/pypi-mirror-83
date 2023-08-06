class ThaiNumberConverter:
    
    def __init__(self):
        pass

    '''
    parameter: number
    return: Thai Text
    '''
    def ToText(self,number):
        result = ''
        try:
            inumber = int(number)     
            if inumber < 0:
                raise ValueError
        except ValueError:
            print(str(number) + ' is not a valid number')
        else:
            dic = self.__GroupNumber(number)
            for k in sorted(dic.keys(),reverse=True):
                if k != 1:
                    result = result + self.__NumtoWord(dic[k]) + 'ล้าน'
                else:
                    result = result + self.__NumtoWord(dic[k])
        return result
    
    '''
    parameter: Arabic number
    return: Thai number
    '''
    def ToThaiNumber(self,number):
        try:
            inumber = int(number)
            if inumber < 0:
                raise ValueError
        except ValueError:
            print(str(number) + ' is not a valid number')
        else:
            txt = ''
            thainum = {'0':'0','1':'๑','2':'๒','3':'๓','4':'๔','5':'๕','6':'๖','7':'๗','8':'๘','9':'๙'}
            for n in str(inumber):
                txt = txt + thainum[n]
            return txt
    
    '''
    parameter: Thai text 
    return: Number in regard of given Thai text
    '''
    def ToNum(self,thaiTxt):
        try:
            result = ''
            for t in self.__SplitNumber(thaiTxt,'ล้าน'):
                result = result + self.__THBToNumMain(t)
            return result
        except:
            print('Check if text contains excluded word')

    def __GroupNumber(self,number):    
        snumber = str(number)
        i = -1;
        j = 1
        d = {}
        while len(snumber[i:i-6:-1]) > 0:
            d[j] = snumber[i:i-6:-1][::-1]
            j = j+1
            i = i-6
        return d

    def __NumtoWord(self,number):
        if len(str(number)) == 1:
            return self.__FirstToTHB(number)
        elif len(str(number)) == 2:
            return self.__SecondToTHB(number)
        elif len(str(number)) == 3:
            return self.__ThirdToTHB(number) 
        elif len(str(number)) == 4:
            return self.__FourthToTHB(number) 
        elif len(str(number)) == 5:
            return self.__FifthToTHB(number) 
        else:
            return self.__SixthToTHB(number)  

    def __FirstToTHB(self,first):
        firstDict = {1:'หนึ่ง',2:'สอง',3:'สาม',4:'สี่',5:'ห้า',6:'หก',7:'เจ็ด',8:'แปด',9:'เก้า',0:'ศูนย์'}
        return firstDict[int(first)]

    def __SecondToTHB(self,second):
        secondDict = {1:'เอ็ด',2:'ยี่'}
        result = 'สิบ'
        if str(second)[0] == '1':
            result = result
        elif str(second)[0] == '2':
            result = secondDict[2] + result
        elif str(second)[0] == '0':
            result = ''
        else:
            result = self.__FirstToTHB(int(str(second)[0])) + result
        
        if str(second)[1] == '1':
            result = result + secondDict[1]
        elif str(second)[1] == '0':
            result = result
        else:
            result = result + self.__FirstToTHB(int(str(second)[1]))
        
        return result

    def __ThirdToTHB(self,third):
        if int(str(third)[0]) > 0:
            return self.__FirstToTHB(int(str(third)[0])) + 'ร้อย' + self.__SecondToTHB(str(third)[-1:-3:-1][::-1])
        else:
            return self.__SecondToTHB(str(third)[-1:-3:-1][::-1])

    def __FourthToTHB(self,fourth):
        if str(fourth)[0] != '0':
            return self.__FirstToTHB(int(str(fourth)[0])) + 'พัน'+ self.__ThirdToTHB(str(fourth)[-1:-4:-1][::-1])
        else:
            return self.__ThirdToTHB(str(fourth)[-1:-4:-1][::-1])

    def __FifthToTHB(self,fifth):
        if str(fifth)[0] != '0':
            return self.__FirstToTHB(int(str(fifth)[0])) + 'หมื่น' + self.__FourthToTHB(str(fifth)[-1:-5:-1][::-1])
        else:
            return self.__FourthToTHB(str(fifth)[-1:-5:-1][::-1])

    def __SixthToTHB(self,sixth):
        if str(sixth)[0] != '0':
            return self.__FirstToTHB(int(str(sixth)[0])) + 'แสน' + self.__FifthToTHB(str(sixth)[-1:-6:-1][::-1])
        else:
            return self.__FifthToTHB(str(sixth)[-1:-6:-1][::-1])

    def __THBToNumMain(self,txt):
        dictionary = {0:'ล้าน',1:'แสน',2:'หมื่น',3:'พัน',4:'ร้อย',5:'สิบ'}
        digit = {'':1,'เอ็ด':1, 'หนึ่ง':1,'สอง':2,'ยี่':2,'สาม':3,'สี่':4,'ห้า':5,'หก':6,'เจ็ด':7,'แปด':8,'เก้า':9}
        desc = {'แสน':'00000','หมื่น':'0000','พัน':'000','ร้อย':'00','สิบ':'0'}
    
        s = ''; 
        kindex = ''
        for k in dictionary:    
            l = self.__SplitNumber(txt,dictionary[k])
            if len(l) > 1:
                txt = l[1]
                s = s + str(digit[l[0]])
            elif len(l) == 1:
                s = s + '0'
            if txt == '':
                kindex = str(dictionary[k])
                break

        if txt != '':
            s = s + str(digit[txt])

        if kindex != '':
            s = s + desc[kindex]
    
        return str(int(s))

    def __SplitNumber(self,numDesc,unit):
        return numDesc.split(unit)