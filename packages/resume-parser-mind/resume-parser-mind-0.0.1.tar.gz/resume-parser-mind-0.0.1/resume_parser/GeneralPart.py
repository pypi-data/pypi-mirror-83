from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import re
#import find_job_titles

class GeneralPart:
    def read_resume_text(self, fileName):        
        #print("Reading of file started.")
        # Reading sample resume pdf file
        fh=open(fileName,'rb')
        
        PDFPage.get_pages(fh)
        
        # iterate over all pages of PDF document
        resume_text = ''
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
    
            # creating a resoure manager
            resource_manager = PDFResourceManager()
            
            # create a file handle
            import io
            fake_file_handle = io.StringIO()
            
            # creating a text converter object
            converter = TextConverter(resource_manager, fake_file_handle, 
                                      laparams=LAParams())

            # creating a page interpreter
            page_interpreter = PDFPageInterpreter(resource_manager, 
                                                  converter)

            # process current page
            page_interpreter.process_page(page)
                
            # extract text
            page_text = fake_file_handle.getvalue()
            resume_text = resume_text +'\n'+ page_text

            # close open handles
            converter.close()
            fake_file_handle.close()
            
        #print(resume_text)
            
        return resume_text
    
    
    # Extract phone numbers in document
    def extract_phone_numbers(self, resume_text):
        phone_numbers=set()
        #define the regular expression
        regex = re.compile(r'(\+[0-9]+\s*)?(\([0-9]+\))?[\s0-9\-]+[0-9]+')
        resume_text="".join(resume_text.split())
        resume_text=resume_text[:2000]
        matches = regex.finditer(resume_text)
        try:
            for match in matches:
                if len(match[0])>=10:
                #print(match[0])
                    phone_numbers.add(match[0])
                    ph_no=list(phone_numbers)
            
            #print('Phone No: '+phone_numbers[0])
            #print(ph_no)
            return ph_no
        except:
            print('No Contact Info')
                
    # Extract email ids
    def extract_email_ids(self, resume_text):
        email_ids = []
        try:
            emailregex = re.findall('\S+@\S+',resume_text)
            
            #print("Email ID: "+emailregex[0])
            email_ids.append(emailregex[0])
            
            return email_ids
        except:
            print('No Email Address available')
    
#--------------------------------Extracting Designation----------------------------------
'''   def extract_jobtitles(self,resume_text):
        from find_job_titles import FinderAcora
       
        try:
            finder=FinderAcora()
           
            titles=finder.findall(resume_text)
            print('\n')
            print("Job Titles are : ")
            for m in titles:
               print(m)
               return m
        except:
            StopIteration
 '''
            
       