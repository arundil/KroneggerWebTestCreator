class GenerationFactory(object):
    """description of class"""

    def buildDictionaryfromPostRequest(form):
        numrows = form['numrows'] 
        dictionary = {}
        counter_group = 1
        for j in form.items():
           num_row = j[0][3]
           if j[0][4].isnumeric():
               num_row =j[0][3]+ j[0][4]
           if num_row.isnumeric():
               order = form['row' + num_row + '_order']
               if order not in dictionary:
                    dictionary[order] = {}
              # else:
               #     dictionary[order+"."+str(counter_group)] = {}
                #    counter_group = counter_group +1
               dictionary_aux={}
               dictionary_aux = dictionary[order]

               if "payload" in j[0]:
                    last_position = len(j[0])-1
                    order_list = int(j[0][last_position])-1

                    if  dictionary_aux.__contains__("Payload"):
                        size= len(dictionary_aux["Payload"])-1
                        if (size<=order_list):
                            if (order_list-size>1):
                                for k in range(size,order_list):
                                    list_aux.append("")
                                dictionary_aux["Payload"].append(j[1])
                            else:
                                dictionary_aux["Payload"].append(j[1])
                        else:
                            dictionary_aux["Payload"][order_list]=j[1]
                    else:
                        list_aux = []
                        size= 0
                        if (size<=order_list):
                            if (order_list-size>=1):
                                for k in range(size,order_list):
                                    list_aux.append("")
                                list_aux.append(j[1])
                            else:
                                list_aux.append(j[1])
                        else:
                            list_aux[order_list]=j[1]

                        dictionary_aux["Payload"] = list_aux

               elif "response" in j[0]:
                    last_position = len(j[0])-1
                    order_list = int(j[0][last_position])-1

                    if  dictionary_aux.__contains__("Response"):
                        size= len(dictionary_aux["Response"])-1
                        if (size<=order_list):
                            if (order_list-size>1):
                                for k in range(size,order_list):
                                    list_aux.append("")
                                dictionary_aux["Response"].append(j[1])
                            else:
                                dictionary_aux["Response"].append(j[1])
                        else:
                            dictionary_aux["Response"][order_list]=j[1]
                    else:
                        list_aux = []
                        size= 0
                        if (size<=order_list):
                            if (order_list-size>=1):
                                for k in range(size,order_list):
                                    list_aux.append("")
                                list_aux.append(j[1])
                            else:
                                list_aux.append(j[1])
                        else:
                            list_aux[order_list]=j[1]

                        dictionary_aux["Response"] = list_aux

               elif "command" in j[0]:
                    dictionary_aux["Command"] = GenerationFactory.getCommandbyName(j[1])
               elif "error" in j[0]:
                    dictionary_aux["Error"] = j[1]
               dictionary[order] = dictionary_aux     

        return dictionary

    def generateManualTestFile(dictionary,counter):

        testfile = """import unittest
import uartdevice
import log
import sys
import msvcrt
import xmlhandler
import os

#disable traceback
__unittest = True

class Run(unittest.TestCase):
    def setUp(self):
        xml = xmlhandler.Xml(os.path.dirname(os.path.abspath(__file__)), "testsettings.xml")
        self.baudrate = xml.getBaudrate()
        self.comport = xml.getComport()
        uartdevice.open_com(self.comport, self.baudrate)


    def tearDown(self):
        if comport is not None:
            uartdevice.close_com()  

    """
        testloop=""
        try:
            for i in range(0,counter):
                if str(i) in dictionary:
                    dictionary_aux = {}
                    dictionary_aux = dictionary[str(i)]
                    testloop= testloop+"""
    def test__E_0"""+str(i)+"""(self):
    """
                    testloop= testloop+"""    success, response = uartdevice.send_uart_cmd(["""
                    for j in range(0,len(dictionary_aux['Command'])):
                         testloop= testloop+ """ord(\""""+dictionary_aux['Command'][j]+"""\"), """

                    if 'Payload' in dictionary_aux:
                        for itemlist in dictionary_aux['Payload']:
                            for i in GenerationFactory.my_range (1,len(itemlist),2):
                                testloop = testloop+"""0x"""+itemlist[i-1]+itemlist[i]+""", """

                    testloop=testloop.rstrip(' ')
                    testloop=testloop.rstrip(',')
                    testloop=testloop+ """])"""
            
                    testloop= testloop+"""
        log.printline_ascii(''.join('%02x '%i for i in response))
        """
                    if 'Response' in dictionary_aux:
                        testloop = testloop+"""self.assertEqual(response,["""
                        for itemlist in dictionary_aux['Response']:
                            i=0
                            while i < len(itemlist):
                                if GenerationFactory.is_hex(itemlist[i]):
                                    testloop = testloop+"""0x"""+itemlist[i]+itemlist[i+1]+""", """
                                    i = i+2
                                else:
                                    testloop = testloop+"""ord(\""""+itemlist[i]+"""\"), """
                                    i=i+1
                                    
                                    

                        testloop=testloop.rstrip(' ')
                        testloop=testloop.rstrip(',')
                        testloop=testloop+ """])"""

                    if 'Error' in dictionary_aux and not dictionary_aux['Error']=="":
                        testloop = testloop+"""self.assertEqual(response,[ord(\""""+dictionary_aux['Error']+"""\")])"""
                testloop+="\n"
            testfile = testfile+testloop
        except Exception:
            print(dictionary)
        return testfile

    def getCommandbyName(name):

        if name == "Reset":
            return "x"
        elif name == "Select":
            return "s"
        elif name == "Transfer":
            return "t"
        elif name == "Transfer Layer 4":
            return "t4"
        elif name == "Get Version":
            return "v"
        elif name == "RF-Field On":
            return "pon"
        elif name == "RF-Field Off":
            return "poff"
        elif name == "Set User Ports":
            return "pp"
        elif name == "Read User Ports":
            return "pr"
        elif name == "Write User Ports":
            return "pw"
        elif name == "Login":
            return "l"
        elif name == "Read Block":
            return "rb"
        elif name == "Read Multiple Block":
            return "rd"
        elif name == "Read Value Block":
            return "rv"
        elif name == "Write Block":
            return "wb"
        elif name =="Write Multiple Block":
            return "wd"
        elif name == "Write Value Block":
            return "wv"
        elif name == "Increment Value Block":
            return "+"
        elif name == "Decrement Value Block":
            return "-"
        elif name == "Copy Value Block":
            return "="

    def my_range(start, end, step):
        while start <= end:
            yield start
            start += step

    def is_hex(s):
        try:
            int(s, 16)
            return True
        except ValueError:
            return False