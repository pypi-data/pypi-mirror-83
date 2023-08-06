class Idcard_Malaysia(): 
    def __init__(self): 
        self.MY_REGION_LIST = ['KUALA LUMPUR','KUALA ', 
                                'W.P. KUALA LUMPUR', "W. PERSEKUTUAN(KL)",
                                'W. PERSEKUTUANIKL)', 'W. PERSEKUTUAN(KL', 
                                'W. PERSEKUTUANIKL', 'W PERSEKUTUAN(KL)',
                                'JOHOR', "KEDAH", "PERAK", "PAHANG", "PERSEKUTUAN",
                                "SABAH", "SELANGOR", "SARAWAK", "TERENGGANU", 
                                "KELANTAN", "PULAU PINANG", "MELAKA", 
                                "NEGERI SEMBILAN", "PERLIS", "LABUAN"]


    def __get_ic(self, text_list): 
        selected_ic = None
        ic_index = None
        get = False

        for idx, i in enumerate(text_list): 
            if len(i.split('-')) == 3:
                selected_ic = re.sub('\D', '', i)
                ic_index = idx
                get = True 
                break

        return selected_ic, ic_index, get


    def __get_dob(self, ic_number):
        year = int(ic_number[:2])
        month = ic_number[2:4]
        day = ic_number[4:6]
        actualyear = year

        if year >= 50:
            actualyear = actualyear + 1900
        else:
            actualyear = actualyear + 2000

        return day+'/'+month+'/'+ str(actualyear)


    def __get_gender(self, ic_number):
        last_digit = int(ic_number[-1])
        if last_digit%2 == 0:
            return 'F'
        else:
            return 'M'

    
    def __get_address(self, text_list):
        """[summary]
        Arguments:
            response {[type]} -- [description]
        Returns:
            [type] -- [description]
        """    
        address = ''
        state = ''

        for idx, i in enumerate(text_list): 
            if i in self.MY_REGION_LIST: 
                address = text_list[idx -5] + " " + text_list[idx-4] + " " + text_list[idx-3] + " " + text_list[idx-2]
                state = i
                break

        return address, state

    
    def __get_fullname(self, text_list, ic_index):
        """[summary]
        Arguments:
            response {[type]} -- [description]
            ic_index {[type]} -- [description]
        Returns:
            [type] -- [description]
        """    
        selected_name = ''

        for idx, i in enumerate(text_list): 
            if idx > ic_index: 
                suku_kata = i.split(" ")

                if len(suku_kata) >= 2 or ('BIN' in i or "Bin" in i or "BINTI" in i or "Binti" in i): 
                    selected_name = i
                    break

        return selected_name

    
    def process(self, text_list): 
        ic_number, ic_index, get_ic = self.__get_ic(text_list)
        full_name = None 
        gender = None 
        dob = None 
        address = None 

        if get_ic: 
            full_name = self.__get_fullname(text_list, ic_index)
            print (full_name)
            gender = self.__get_gender(ic_number)
            print (gender)
            dob = self.__get_dob(ic_number)
            print (dob)
            address, state = self.__get_address(text_list)
            print (address)
            print (ic_number)
            
        return ic_number, full_name, gender, dob, address, state


class Idcard_Singapore(): 
    def __init__(self): 
        a = None 

    
    def process(self, text_list): 
        name = "-" 
        num_ic = "-" 
        dob = "-"
        gender = "-"
        address = "-"
        state = "-"

        for idx, i in enumerate(text_list): 
            if "Nama" in i or "Name" in i or "Nam" in i or "ame" in i : 
                name = text_list[idx + 1]
            if "IDENTITY" in i or "CARD NO" in i: 
                num_ic = i.split(" ")[-1]
            if "Date" in i: 
                dob = text_list[idx + 2] 
                gender = text_list[idx + 3]
                if gender != "M" and gender != "F": 
                    gender = "unknown"

        print (name)
        print (num_ic) 
        print (dob)
        print (gender)
        return name, num_ic, dob, gender, address, state


class Idcrad_Vietnam(): 
    def __init__(self): 
        self.DOB_CHARS = ["Sinh ngay", "Sinh ingay", 
                            "Sinh nga", "Sin ingay", 
                            "inh ngay"]

    def process(self, text_list): 
        name = "-"
        num_ic = "-"
        dob = "-"
        gender = "-"
        address = "-"
        state = "-"

        for idx, i in enumerate(text_list): 
            if  "Ho ten" in i: 
                name = text_list[idx + 1]

            for j in self.DOB_CHARS: 
                if j in i: 
                    dob = text_list[idx + 1]

            if "Nguyen quan" in i: 
                address = text_list[idx + 1] + ", " + text_list[idx + 2]

        print (name)
        print (num_ic)
        print (dob)
        print (gender)
        print (address)
        print (state)
        return name, num_ic, dob, gender, address, state


class Idcard_Thailand(): 
    def __init__(self): 
        a = None 

    
    def process(self, text_list): 
        name = "-"
        num_ic = text_list[1]
        dob = "-"
        gender = "-"
        address = "-"
        state = "-"

        for idx, i in enumerate(text_list): 
            if "Name" in i: 
                name = i.split(" ")[-1]
                if "Miss" in i or "Mrs" in i: 
                    gender = 'F'
                elif "Mr" in i: 
                    gender = "M"

            if "Last name" in i: 
                name = name + " " + i.split(" ")[-1]
            
            if "Date of Birth" in i: 
                dob = i.split(" ")[-3] + " " + i.split(" ")[-2] + i.split(" ")[-1]
                dob = dob.replace('.', "")

        print (name)
        print (num_ic)
        print (dob)
        print (gender)
        print (address)
        print (state)
