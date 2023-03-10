import sys
import re

class Descriptor(object):
     def __init__(self, short_code: str, raw:str):
        self.code = short_code
        self.raw = raw
        self.learning_outcomes = None
        
        self.aim = None
        
        self.content = None
        
        self.full_name = None
        
        self.prequistes = None
        
        self.co_requisites = None
        
     def set_learning_outcomes(self,fn):
        self.learning_outcomes = fn(self.raw)
     def set_content(self,fn):
        self.content = fn(self.raw)
     def set_aim(self,fn):
        self.aim = fn(self.raw)
     def set_full_name(self,fn):
        self.full_name = fn(self.raw)        
     def set_pre_requisites(self,fn):
         self.prequistes = fn(self.raw)
     def set_co_requisites(self,fn):
         self.co_requisites = fn(self.raw)
        
def get_txt_between(raw:str, re1:re , re2:re ):
         whole_list = re.split(re1,raw)
         with_All = ""
         for index in range(1,len(whole_list)):
                with_All += whole_list[index]
         the_text = (re.split(re2,with_All))[0]
         return the_text
       
def PR5006_HV4701_BIT():
    #  Run with BASH
    #  pdf2txt -n ./PR5006-HV4701_BIT_Programme_descriptors.pdf | /usr/bin/python3 ./filterchars.py
    def get_learning_outcomes( raw:str) :
        #scan raw to accumulate learning outcomes 
        #return LOs
        re1 = r"(?i)Learning Outcomes[:]?"
        re2 = r"(?i)Indicative Content[:]?"
        return (get_txt_between(raw,re1,re2)).strip()
    
    def get_content( raw:str) :
        #scan raw to accumulate content
        #return content
        
        re1 = r"(?i)[Cc]ontent"
        re2 = r"(?i)Assessment Method"
        return get_txt_between(raw,re1,re2)
    
    def get_aim(raw:str):
        re1 = r"(?i)Aim[s]?"
        re2 = r"(?i)Learning Outcomes"
        return get_txt_between(raw,re1,re2)
    
    def get_full_name(raw:str):
        re1 = r"(?i)Title"
        re2 = r"(?i)Level"
        result = get_txt_between(raw,re1,re2)
        return result.strip()

    def get_pre_requisites(raw:str):
        re1 = r"(?i)Pre-requisites"
        re2 = r"(?i)Learning Hours"
        result = get_txt_between(raw,re1,re2)
        return result.strip()
    
    """ No Co_requisites - beware the following
        def get_co_requisites(raw:str):
            Pass 
            return ""
            """
    
    course_content = {}  # A dictionary of "Descriptors" by course
    # Read txt into pages
    instr = sys.stdin.read()
    page_list = instr.split('')
    
    current_module = ""
    raw_list = []
    # start match
    re_start = r".*Code Title [A-Z]{2}[0-9]{4}"
    for page in page_list:
        proposed_raw = (re.sub(r"PR5006 Bachelor of Information Technology  page [0-9][0-9]?[0-9]?","",page.strip())).strip()
        if proposed_raw != "":
            start_of_module = re.match(r"^[A-Z]{2}[0-9]{4}",proposed_raw )
            if start_of_module is not None:
                current_module = start_of_module.group()
                course_content[current_module] = Descriptor(current_module,proposed_raw)
            else:
                course_content[current_module].raw += page
    # Process raw
    for descriptor_code in course_content:
        course_content[descriptor_code].set_learning_outcomes(get_learning_outcomes)
        course_content[descriptor_code].set_content(get_content)
        course_content[descriptor_code].set_aim(get_aim)
        course_content[descriptor_code].set_full_name(get_full_name)
        course_content[descriptor_code].set_pre_requisites(get_pre_requisites)
           
    return course_content

def Ucol_Bachelor_of_Information_and_Communications_Technology_L7_Courses()-> dict:
    #Ucol get descriptors
    # Run with Bash command:
    # pdf2txt -n ./'UCOL Bachelor of Information and Communications Technology L7 Courses.pdf' | /usr/bin/python3 ./filterchars.py > UCOL.txt
    
    def get_learning_outcomes( raw:str) :
        #scan raw to accumulate learning outcomes 
        #return LOs
        re1 = r"(?i)Learning Outcomes[:]?"
        re2 = r"(?i)Content[:]?"
        return (get_txt_between(raw,re1,re2)).strip()
         
    
    def get_content( raw:str) :
        # #scan raw to accumulate content
        # #return content
        
        re1 = r"(?i)Content[:]?"
        re2 = r"(?i)Learning and Teaching[:]?"
        return get_txt_between(raw,re1,re2)
        
    def get_aim(raw:str):
        re1 = r"(?i)Course Aim[:]?"
        re2 = r"(?i)Learning Outcomes[:]?"
        return (get_txt_between(raw,re1,re2)).strip()
        

    def get_full_name(raw:str):
        re1 = r"[A-Z][0-9]{3}"
        re2 = r"(?i)Course Level[:]?"
        result = get_txt_between(raw,re1,re2)
        return result.strip()
        
    def get_pre_requisites(raw:str):
        result = ""
        re1 = r"(?i)Pre-requisite or Co-requisite"
        re2 = r"(?i)Course Aim"
        result = get_txt_between(raw,re1,re2)
        if result == "":
            re1 = r"(?i)Pre-requisite"
            re2 = r"(?i)Co-requisite"
            result = get_txt_between(raw,re1,re2)
        return result.strip()
    
    def get_co_requisites(raw:str):
        re1 = r"(?i)Co-requisite"
        re2 = r"(?i)Course Aim"
        result = get_txt_between(raw,re1,re2)
        return result.strip()
    
    course_content = {}  # A dictionary of "Descriptors" by course
    
    # Read txt into pages
    instr = sys.stdin.read()
    page_list = instr.split('')
    
    current_module = ""

    # Get descriptors - filter out page and start of modules, process for each descriptor 
    for page in page_list:
        
        # Bachelor of Information and Communications Technology Level 7 Version 21.2 Approved by: NZQA  Page 1 of 76 Master Copy: I/CAS/curriculum documents and programme file   
        repagestr = r"Bachelor.*Page [0-9]+ of [0-9]+ Master.*programme file"
        restart = r"[A-Z][0-9]{3}.*Course Level"
        proposed_output = (re.sub(repagestr,"",page)).strip()
        #test_filter_pages += [filtered_str]
             
        if proposed_output != "":
            # If a new course code
            the_module_match = re.match(r"[A-Z][0-9]{3}",proposed_output)
            if the_module_match is not None:
                current_module = the_module_match.group()
                # Create a descriptor with this proposed_output as "raw"
                descriptor = Descriptor(current_module,proposed_output)
                course_content[current_module] = descriptor
            else:
                # append the proposed output to raw
                course_content[current_module].raw += proposed_output
    
    # Process "RAW" data 
    for descriptor_code in course_content:
        course_content[descriptor_code].set_learning_outcomes(get_learning_outcomes)
        course_content[descriptor_code].set_content(get_content)
        course_content[descriptor_code].set_aim(get_aim)
        course_content[descriptor_code].set_full_name(get_full_name)
        course_content[descriptor_code].set_pre_requisites(get_pre_requisites)
        course_content[descriptor_code].set_co_requisites(get_co_requisites)
        
    return course_content
    
    
    
def Unitec_BSC_Prog_Descriptors(): # -> dict :
    # Unitec get course descriptors
    # Unitec process
    # Based on https://www.digitalocean.com/community/tutorials/how-to-perform-server-side-ocr-on-pdfs-and-images
    # BASH gs -o unitec_output/%05d.png -sDEVICE=png16m -r300 -dPDFFitPage=true 'Unitec BCS Prog Descriptors.pdf'
    # BASH for png in $(ls unitec_output); do tesseract -l eng unitec_output/$png unitec_output/$(echo $png | sed -e "s/\.png//g") pdf; done
    # BASH pdftk unitec_output/*.pdf cat output unitec_output/joined.pdf
    # Then Run with Bash command
    # pdf2txt ./unitec_output/joined.pdf 
    # Still have a mess with OCR'd text moving on to UCOL for now
    # 9/March/20223 With a new source
    # Run with Bash command
    #   pdf2txt -n ./'UNITEC Course Descriptor Sem2-2022 .pdf' | /usr/bin/python3 ./filterchars.py
    course_content = {}  # A dictionary of "Descriptors" by course
     
    # Read txt into pages
    instr = sys.stdin.read()
    #page_list = instr.split('')
    # Unitec has in consistent FF page delimiter from the pdf2txt
    # But it has a unique course start identifier
    # going straight to descriptors
    list_name_course = list(re.split(r"([A-Z]{4}[0-9]{4}):",instr))
    short_name = ""
    i = 0;
    for c in list_name_course:
        if(i % 2) != 0: 
            #print(i,list_name_course[i],list_name_course[i+1][:10])
            short_name = list_name_course[i]
            clean_raw =  re.sub(r"","",list_name_course[i+1]).strip() 
            course_content[short_name] =   Descriptor(short_name,clean_raw)
        i+=1
    
    # page list test
    return course_content
    
    
def Wintec_BAppliedIT_Vol2() -> dict : 
    # Wintec - get descriptors
    # Run with Bash command
    # pdf2txt -n ./'Wintec BAppliedIT(Vol2) (ModDesc).pdf' | /usr/bin/python3 ./filterchars.py > Wintec.txt
    
           
    def get_learning_outcomes( raw:str) :
        #scan raw to accumulate learning outcomes 
        #return LOs
        re1 = r"(?i)Learning Outcomes[:]?"
        re2 = r"(?i)Content[:]?"
        return get_txt_between(raw,re1,re2)
    
    def get_content( raw:str) :
        #scan raw to accumulate content
        #return content
        
        re1 = r"(?i)Content[:]?"
        re2 = r"(?i)Teaching Learning Methods[:]?"
        return get_txt_between(raw,re1,re2)
    
    def get_aim(raw:str):
        re1 = r"(?i)Aim[:]?"
        re2 = r"(?i)Learning Outcomes[:]?"
        return get_txt_between(raw,re1,re2)
    
    def get_full_name(raw:str):
        re1 = r"(?i)Module Name[:]?"
        re2 = r"(?i)Module Code[:]?"
        re3 = r"[A-Z]{4}[0-9]{3} [???]?"
        re4 = r"(?i)Credit Value[:]?"
        result = get_txt_between(raw,re1,re2)
        if (result == "") or (result is None):
            result =  get_txt_between(raw,re3,re4)
        return result.strip()
    
    def get_pre_requisites(raw:str):
        re1 = r"(?i)Pre-Requisites[:]?"
        re2 = r"(?i)Co-Requisites[:]?"
        return get_txt_between(raw,re1,re2)
    
    def get_co_requisites(raw:str):
        result = ""
        re1 = r"(?i)Co-requisites[:]?"
        
        re2 = r"(?i)Aim[:]?"
        mode =  get_txt_between(raw,re1,re2)
        if mode == None : 
            re2 = r"(?i)Mode of Delivery[:]?"
            result = get_txt_between(raw,re1,re2)
        else:
            result =  mode
        return result
        
    course_content = {}  # A dictionary of "Descriptors" by course
     
    # Read txt into pages
    instr = sys.stdin.read()
    page_list = instr.split('')

    current_module = ""
    
    # Get descriptors - filter out page and start of Wintec modules, process for each descriptor 
    for page in page_list:   
        repagestr = r"[0-9][0-9] \| Page ?? Copyright 2015, Waikato Institute of Technology"
        restart = r" MODULE DESCRIPTOR FOR:  [A-Z]{4}[0-9]{3}"
        if page.startswith(' MODULE DESCRIPTOR FOR:  '):
            
            proposed_output = re.sub( r"^1\s*","",(
                                    re.sub(
                                        restart,"",(
                                            re.sub(repagestr,"",page)
                                            )
                                        )
                                ).strip()
                            )
                    
            if proposed_output != "":
                # If a new course code
                the_module_match = re.match(r"[A-Z]{4}[0-9]{3}",proposed_output)
                if the_module_match is not None:
                    current_module = the_module_match.group()
                    # Create a descriptor with this proposed_output as "raw"
                    descriptor = Descriptor(current_module,proposed_output)
                    course_content[current_module] = descriptor
                else:
                    # append the proposed output to raw
                    course_content[current_module].raw += proposed_output
    
    # Process "RAW" data 
    for descriptor_code in course_content:
        course_content[descriptor_code].set_learning_outcomes(get_learning_outcomes)
        course_content[descriptor_code].set_content(get_content)
        course_content[descriptor_code].set_aim(get_aim)
        course_content[descriptor_code].set_full_name(get_full_name)
        course_content[descriptor_code].set_pre_requisites(get_pre_requisites)
        course_content[descriptor_code].set_co_requisites(get_co_requisites)
        
    return course_content

if __name__ == "__main__":
# test code
# UniTec
# Testing for pages
    #pages = Unitec_BSC_Prog_Descriptors()
    # count = 0
    # for apage in pages:
    #     print("Key? ",count,apage)
    #     count += 1
# Testing for Courses
    course_content = Unitec_BSC_Prog_Descriptors()
    for key in course_content:
        print(key,'  ',course_content[key].raw)

# WinTec
#    course_content = Wintec_BAppliedIT_Vol2()
#    for key in course_content:
#        if not ("none" in course_content[key].co_requisites.lower() or "nil" in course_content[key].co_requisites.lower()) :
#             print(key,":",course_content[key].aim,"\n","     pre_requisite:",course_content[key].prequistes,"\n","     co_requisite:",course_content[key].co_requisites)   

# UCol
    # course_content = Ucol_Bachelor_of_Information_and_Communications_Technology_L7_Courses()
    # for key in course_content:
    #     #if not ("none" in course_content[key].co_requisites.lower() or "nil" in course_content[key].co_requisites.lower()) :
    #          print(key,":",course_content[key].aim,"\n","     pre_requisite:",course_content[key].prequistes,"\n","     co_requisite:",course_content[key].co_requisites)   
              
# WandW
    #print(PR5006_HV4701_BIT())
    # course_content = PR5006_HV4701_BIT()
    # for key in course_content:
    #       print(key,":",course_content[key].aim,"\n","     pre_requisite:",course_content[key].prequistes)   
    