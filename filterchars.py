import sys
import re

class Descriptor(object):
     def __init__(self, short_code: str, raw:str):
        self.code = short_code
        self.raw = raw
        self.learning_outcomes = None
        
        self.aim = None
        
        self.content = None
        
     def set_learning_outcomes(self,fn):
        self.learning_outcomes = fn(self.raw)
     def set_content(self,fn):
        self.content = fn(self.raw)
     def set_aim(self,fn):
        self.aim = fn(self.raw)
        
def get_txt_between(raw:str, re1:re , re2:re ):
         whole_list = re.split(re1,raw)
         with_All = ""
         for index in range(1,len(whole_list)):
                with_All += whole_list[index]
         the_text = (re.split(re2,with_All))[0]
         return the_text  
     
def Ucol_Bachelor_of_Information_and_Communications_Technology_L7_Courses()-> dict:
    course_content = {}  # A dictionary of "Descriptors" by course
     
    # Read txt into pages
    instr = sys.stdin.read()
    page_list = instr.split('')
    return page_list
    pass
    
def Unitec_BSC_Prog_Descriptors() -> dict :
    # Unitec get course descriptors
    # Unitec process
    # Based on https://www.digitalocean.com/community/tutorials/how-to-perform-server-side-ocr-on-pdfs-and-images
    # BASH gs -o unitec_output/%05d.png -sDEVICE=png16m -r300 -dPDFFitPage=true 'Unitec BCS Prog Descriptors.pdf'
    # BASH for png in $(ls unitec_output); do tesseract -l eng unitec_output/$png unitec_output/$(echo $png | sed -e "s/\.png//g") pdf; done
    # BASH pdftk unitec_output/*.pdf cat output unitec_output/joined.pdf
    # Then Run with Bash command
    # pdf2txt ./unitec_output/joined.pdf 
    # Still have a mess with OCR'd text moving on to UCOL for now
    pass 
    
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
        
    course_content = {}  # A dictionary of "Descriptors" by course
     
    # Read txt into pages
    instr = sys.stdin.read()
    page_list = instr.split('')

    current_module = ""
    
    # Get descriptors - filter out page and start of Wintec modules, process for each descriptor 
    for page in page_list:   
        repagestr = r"[0-9][0-9] \| Page © Copyright 2015, Waikato Institute of Technology"
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
        
    return course_content

if __name__ == "__main__":
 # test code
 # WinTec
 #   course_content = Wintec_BAppliedIT_Vol2()
 #   for key in course_content:
 #       print(key,":",course_content[key].aim)
    print(Ucol_Bachelor_of_Information_and_Communications_Technology_L7_Courses())                  
            
           