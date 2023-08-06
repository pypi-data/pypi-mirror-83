# -*- coding: utf-8 -*-
import spacy
import pandas as pd
import numpy as np
import nltk
from nltk import word_tokenize
nltk.download('stopwords')
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from nltk.corpus import stopwords
import re

# load pre-trained model
nlp = spacy.load('en_core_web_sm')

class NlpDrivenPart:
    def __init__(self):
        self.__nlp = spacy.load('en_core_web_sm')
        
#---------------------------Extracting names----------------------------------------------
# extract names--- Method1
    def extract_person_name(self, resume_text):
        doc = self.__nlp(resume_text)
    
        from spacy.matcher import Matcher
        matcher = Matcher(self.__nlp.vocab)
            
        # First name and Last name are always Proper Nouns
        pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
        matcher.add ('NAME', None, pattern)
        matches = matcher(doc)
    
        name=[]
        for match_id, start, end in matches:
            span = doc[start:end]
            name.append(span.text)
        
        #print('Name from method 1: '+name[0])
        return name[0]
    

# extract names--- Method2
    def extract_person_name2(self,resume_text):
        nlp = spacy.load("en_core_web_sm")
        doc=nlp(resume_text)
        name=[]
        for ent in doc.ents:
            if(ent.label_=='PERSON'):
                name.append(ent.text)
               
        #print('Name from method 2: '+name[0])
        return name[0]


#----------------------------Extracting School Name-------------------------------------
#extract school--- Method1
    def extract_school(self,resume_text):
    
        #text=resume_text.lower()
        nlp = spacy.load("en_core_web_sm")
        doc=nlp(resume_text)
       
        nouns=[]       
        try:
            for chunk in doc.noun_chunks:
                ##print(chunk.text)
                nouns.append(chunk.text)
            
            lowered_nouns=[]
            for l in nouns:    
                l=l.lower()
                l=l.strip("\n\npage")
                lowered_nouns.append(l)
                
            ##print(lowered_nouns)
            school=[]
            pattern=re.compile(r'[a-zA-Z-\.\s-]+([.]?\s?)+(public|school|vidyalaya)+[\s-]*[a-zA-z0-9-\.\s-]*')
            for ent in lowered_nouns:
           
                matches = pattern.finditer(ent)
           
                for match in matches:
                    school.append(match.group())
            #print('\n')      
            #print("School name from method 1 is : ")
            #print(school[0])
            return school[0]
        except:
            print('No details found for School')
    
#extract school--- Method2

    def extract_school2(self,resume_text):

        import nltk
        sentences1 = nltk.sent_tokenize(resume_text)
        ##print(sentences1)    
        org = [nltk.word_tokenize(sent) for sent in sentences1]
        exp=[]
        new = []
        for items in org:
          for item in items:
            item= item.strip()
            new.append(item)
           
        ##print(new)
       
        for n in new:
            if n=='EDUCATION':
                m=new.index(n)
               
                for i in range(m,len(new)):
                    exp.append(new[i])
            elif n=='Academic':
                m=new.index(n)
               
                for i in range(m,len(new)):
                    exp.append(new[i])
                   
        exp1 = " ".join(exp)
        a=[]
       
        exp2=exp1.lower()
        nlp = spacy.load("en_core_web_sm")
        doc=nlp(exp2)
                 
        for chunk in doc.noun_chunks:
            a.append(chunk.text)
           
        school=[]
                   
        for i in a:
            if i == 'EXPERIENCE':
                break
            pattern=re.compile(r'[a-zA-Z-\.\s-]+([.]?\s?)+(public|school|vidyalaya)+[\s-]*[a-zA-z0-9-\.\s-]*')
            matches = pattern.finditer(i)
       
            for match in matches:
                school.append(match.group())
        for i in school:
            #print("\n")
            #print("School name from method 2 is :")
            #print(i)
            return school
        
#----------------------------Extracting skills------------------------------------------
    def extract_skills(self, resume_text,path):
        #csv_path = 'MetaData/Skill_Set.csv' 
        csv_path = path
        ##print("csvpath:",csv_path) 
        df=pd.read_csv(csv_path,encoding= 'unicode_escape')
        ##print(df.head())
        
        #convert dataframe to numpy array
        skill_arr=np.array(df)
        
        #convert list of noun chunks to numpy array
        nlp_doc=nlp(resume_text).noun_chunks
        l1=[]
        for token in nlp_doc:
            l1.append(token.text)
        #sl1 = [x.upper() for x in l1]
    
        arr=np.asarray(l1)
        
        #find common elements in both numpy arrays
        a=np.intersect1d(arr,skill_arr[:, 1])
        l=list(a)
        ##print(l)
        
        #rearrgaing columns of dataframe, later will be used in dictionary
        df2=df[["SkillName", "Category"]]

        #creating list from above dataframe
        sk_arr=list(df2.values)
        
        #creating final dictionary
        d1=dict(sk_arr)
        skill_dict ={}
        skill_count=1
        word_list=[]
        n=0
        
        for i in l: #common skills found in file and resume
            for k,v in d1.items(): #new dictionary of skills
                if i==k:
                    skill_dict[n]=['Category: '+v] 
                    skill_dict[n].append('Skill: '+k)
                    #print('Category = ' +v)
                    #print('Skill = '+k)
                    if i not in word_list:
                        word_list.append(i)
                    else:
                        skill_count=skill_count+1
                        #print('No. of mentions : ',skill_count)
                    skill_dict[n].append('mentioned: '+str(skill_count))
                    n=n+1
        
        
        return skill_dict
        #return skill_count
    
                   
    def extract_qualification(self,resume_text):
        
        #declaring demo list
        qual_list=['Bachelor','Degree','Science','Master','Engineering', 'Masters']

        edu_list=[]
        doc=nlp(resume_text)
        for token in doc.ents:
            edu_list.append(token.text)
        ##print(edu_list)

        edu=[]
        for element in edu_list:
            tokens=word_tokenize(element)
            for item in tokens:
                for ele in qual_list:
                    if item==ele:
                        edu.append(element)

        #print(edu[:2])
        return(edu[:2])
        
        
#-----------------EXTRACTING COLLEGE NAMES----------------------------------

# extract college--- Method1
    def extract_institutes(self,resume_text):

        text1=resume_text.lower()
       
        nlp = spacy.load("en_core_web_sm")
        doc=nlp(text1)
       
        a=[]    
        try:
            for chunk in doc.noun_chunks:
                #print(chunk.text)
                a.append(chunk.text)
            institute=[]
            pattern=re.compile(r'[a-zA-Z-\.\s-]+([.]?\s?)+(college|university|institute|vishwavidyalaya)+[\s-]*[a-zA-z0-9-\.\s-]*')
            for ent in a:
           
                matches = pattern.finditer(ent)
           
                for match in matches:
                    institute.append(match.group())
            #print('\n')      
            #print("College name from method 1 is : ")
            #print(institute[0])
            return institute[0]
        
        except:
            print('Institute Info NA')
    
# extract college--- Method2
    def extract_institutes2(self,resume_text):
        
        csv_path='Metadata/dataset.csv'
        df=pd.read_csv(csv_path,encoding='latin-1')
        
        #split dataset into training testing dataset
        X_train, X_test, y_train, y_test = train_test_split(df['Name'], df['Label'], random_state = 0)
        
        count_vect = CountVectorizer()
        X_train_counts = count_vect.fit_transform(X_train)
        tfidf_transformer = TfidfTransformer()
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
        
        #apply model on training dataset
        model = MultinomialNB().fit(X_train_tfidf, y_train)
        
        education=[]
        try:        
            nlp_doc=nlp(resume_text)
            for chunks in nlp_doc.ents:
                if chunks.label_=='ORG':
                    ##print(chunks.text)
                    education.append(chunks.text)
            
            #creating an empty list
            institutes1=[]
            #institute=[]
            for token in education:
                token=" ".join(token.split())
                token=token.upper()
                ##print(token,'-->',model.predict(count_vect.transform([token])))
                if model.predict(count_vect.transform([token]))==['Institute']:
                    institutes1.append(token)
        
            #print("College name from method 2 is : ")    
            #print('Institutes : ')
            #print(institutes1[0])
            
            return institutes1[0]
        except:
            print('College Info not found')
    
# extract college--- Method3
    def extract_institutes3(self,resume_text):
    
        import nltk
        sentences1 = nltk.sent_tokenize(resume_text)
        ##print(sentences1)    
        org = [nltk.word_tokenize(sent) for sent in sentences1]
        exp1=[]
        exp=[]
        a=[]  
        exp2=[]
        new = []
        for items in org:
          for item in items:
            item= item.strip()
            new.append(item)
           
        ##print(new)
       
        for n in new:
            if n=='EDUCATION' or n=='Education':
                m=new.index(n)
               
                for i in range(m,len(new)):
                    exp.append(new[i])
            elif n=='ACADEMIC' or n=='Academic' :
                m=new.index(n)
               
                for i in range(m,len(new)):
                    exp.append(new[i])
                   
        exp1 = " ".join(exp)
       
        exp2=exp1.lower()
        nlp = spacy.load("en_core_web_sm")
        doc=nlp(exp2)
                 
        for chunk in doc.noun_chunks:
            a.append(chunk.text)
           
        institute=[]
                   
        for i in a:
            if i == 'EXPERIENCE':
                break
            pattern=re.compile(r'[a-zA-Z-\.\s-]+([.]?\s?)+(institute|university|college|vishwavidyalaya)+[\s-]*[a-zA-z0-9-\.\s-]*')
            matches = pattern.finditer(i)
       
            for match in matches:
                institute.append(match.group())
        for i in institute:
            #print("\n")
            #print("College name from method 3 is :")
            #print(i)
            return institute[0]
    
    
#--------------------------Extracting education details-----------------------------------

    def extract_education(self,resume_text):
        EDUCATION = [
                'BE','B.E.', 'B.E', 'BS', 'B.S', 
                'ME', 'M.E', 'M.E.', 'MS', 'M.S', 
                'BTECH', 'B.TECH', 'M.TECH', 'MTECH', 
                'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII',
                'BACHELOR', 'MASTERS'
            ]
        
        STOPWORDS = set(stopwords.words('english'))
        
        nlp_text = nlp(resume_text)
    
        # Sentence Tokenizer
        nlp_text = [sent.string.strip() for sent in nlp_text.sents]
    
        edu = {}
        try:
            # Extract education degree
            for index, text in enumerate(nlp_text):
                for tex in text.split():
                    # Replace all special symbols
                    tex = re.sub(r'[?|$|.|!|,]', r'', tex)
                    if tex.upper() in EDUCATION and tex not in STOPWORDS:
                        edu[tex] = text + nlp_text[index + 1]
        
            # Extract year
            education = []
            for key in edu.keys():
                year = re.search(re.compile(r'(((20|19)(\d{2})))'), edu[key])
                if year:
                    education.append((key, ''.join(year[0])))
                else:
                    education.append(key)
            #print('Education is : ')
            #print(education)
            return education
        
        except:
            print('No Education Details found')

#------------------------------Extracting Previous Companies---------------------------
# extract company--- Method1          
    def extract_companies(self,resume_text):    
        doc=nlp(resume_text)
        
        comp=[]  
        for ent in doc.ents:
            if(ent.label_=='ORG'):
                   comp.append(ent.text)
                           
        pattern = re.compile(r'[a-zA-Z0-9-\.\]*[\s-]+(co\.|Company|Companys|ltd|llc|inc|corp|Corporation|sia|pte|Infotech|Ventures|Solutions|Partners|tech|Isnnovations|Development|Technologies|Bureau|Logistics|Companies|Unlimited|Ventures|Labs|Consulting)+[a-zA-Z0-9-\.]*')
        
        com=set()
        for ele in comp:
            matches = pattern.finditer(ele)
            for match in matches:
                com.add(match.group())
                ##print(match.group())
        companys=list(com) 
        #print("Company name from method 1 is : ") 
        #print(companys)
        return companys

# extract company--- Method2
    def extract_companies2(self,resume_text):
        
        sentences1 = nltk.sent_tokenize(resume_text)
        ##print(sentences1)    
        org = [nltk.word_tokenize(sent) for sent in sentences1]
        exp1=[]
        exp=[]
        new = []
        b=[]
        for items in org:
          for item in items:
            item= item.strip()
            new.append(item)
           
        ##print(new)
       
        for n in new:
            if n=='EXPERIENCE':
                m=new.index(n)
               
                for i in range(m,len(new)):
                    exp.append(new[i])
                   
                   
            elif n=='EMPLOYMENT':
                m=new.index(n)
               
                for i in range(m,len(new)):
                    exp.append(new[i])
                           
        exp1 = " ".join(exp)
       
        #exp2=exp1.lower()
        ##print(exp2)
        nlp = spacy.load("en_core_web_sm")
        doc=nlp(exp1)
        b=[]  
        
        for ent in doc.ents:
            ##print(ent.text, ent.label_)
            if(ent.label_=='ORG' or ent.label_=='PERSON'):
           
                   b.append(ent.text)
        ##print(b)
        
        csv_path='Metadata/dataset.csv'
        df=pd.read_csv(csv_path,encoding='latin-1')
        
        #split dataset into training testing dataset
        X_train, X_test, y_train, y_test = train_test_split(df['Name'], df['Label'], random_state = 0)
        
        count_vect = CountVectorizer()
        X_train_counts = count_vect.fit_transform(X_train)
        tfidf_transformer = TfidfTransformer()
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
        
        #apply model on training dataset
        model = MultinomialNB().fit(X_train_tfidf, y_train)
        
        #creating an empty list
        comp=[]
        #institute=[]
        for token in b:
            token=" ".join(token.split())
            ##print(token,'-->',model.predict(count_vect.transform([token])))
            if model.predict(count_vect.transform([token]))==['Company']:
                comp.append(token)
    
        #print("Company name from method 2 is : ")    
        #print('Companies : ')
        #print(comp)
        
        return comp

# extract company--- Method3
    def extract_companies3(self,resume_text): 
   
        sentences1 = nltk.sent_tokenize(resume_text)
        ##print(sentences1)    
        org = [nltk.word_tokenize(sent) for sent in sentences1]
        exp1=[]
        exp=[]
        new = []
        b=[]
        for items in org:
          for item in items:
            item= item.strip()
            new.append(item)
           
        ##print(new)
       
        for n in new:
            if n=='EXPERIENCE':
                m=new.index(n)
               
                for i in range(m,len(new)):
                    exp.append(new[i])
                   
                   
            elif n=='EMPLOYMENT':
                m=new.index(n)
               
                for i in range(m,len(new)):
                    exp.append(new[i])
                           
        exp1 = " ".join(exp)
       
        exp2=exp1.lower()
        nlp = spacy.load("en_core_web_sm")
        doc=nlp(exp2)
        b=[]  
        for ent in doc.ents:
            if(ent.label_=='ORG'):
           
                   b.append(ent.text)
       
        org=[]        
        for i in b:
            pattern = re.compile(r'[a-zA-Z0-9-\.\s-]+(co\.|company|companys|ltd|sa|ag|nv|llc|inc|corp|corporation|sia|pte|infotech|ventures|soltions|partners|tech|innovations|development|technologies|bureau|worlwide|online|digital|logistics|companies|creative|production|productions|workd|unlimited|ventures|captial|labs|direct|dynmaics|consulting)+[a-zA-Z0-9-\.]*')
            matches = pattern.finditer(i)
            for match in matches:
                org.append(match.group())
        #print("\n")
        #print("Company name from method 2 is : ")
        #print(org)
        return org


#-------------------------------Extracting Work Exp--------------------------------------
    def extract_workexp2(self,resume_text):
        import nltk, datetime
        sentences1 = nltk.sent_tokenize(resume_text)
         
        org = [nltk.word_tokenize(sent) for sent in sentences1]
        exp1=[]
        exp=[]
        new = []
        for items in org:
          for item in items:
            item= item.strip()
            new.append(item)
           
       
        for n in new:
            if n=='EXPERIENCE':
                m=new.index(n)
               
                for i in range(m,len(new)):
                    exp.append(new[i])
            elif n=='EMPLOYMENT':
                m=new.index(n)
               
                for i in range(m,len(new)):
                    exp.append(new[i])
                   
       
                   
        for i in exp:
            if i == 'EDUCATION':
                break
            pattern = re.compile(r'\d{4}')
            match = pattern.findall(i)
            for mat in match:
                exp1.append(mat)
       
        for j in exp:
            subs='Present'
            if re.search(subs, j):
           
                now = datetime.datetime.now()
                present=now.year
                exp1.append(str(present))
       
       
        exp1.sort()
        if len(exp1)!=0:
            years=int(exp1[-1])-int(exp1[0])
            #print("\n")
            #print("The number of experienced years = ")
            #print(years)
        else:
            print("NO experience")
       
    #-----------------------------Extracting Work Exp----------------------------------------
    def extract_workexp(self,resume_text):
            import nltk, datetime
            sentences1 = nltk.sent_tokenize(resume_text)
             
            org = [nltk.word_tokenize(sent) for sent in sentences1]
            exp1=[]
            exp=[]
            new = []
            for items in org:
              for item in items:
                item= item.strip()
                new.append(item)
               
           
            for n in new:
                if n=='EXPERIENCE':
                    m=new.index(n)
                   
                    for i in range(m,len(new)):
                        exp.append(new[i])
                elif n=='EMPLOYMENT':
                    m=new.index(n)
                   
                    for i in range(m,len(new)):
                        exp.append(new[i])
                       
                                 
            for i in exp:
                if i == 'EDUCATION':
                    break
                pattern = re.compile(r'\d{4}')
                match = pattern.findall(i)
                for mat in match:
                    exp1.append(mat)
           
            for j in exp:
                subs='Present'
                if re.search(subs, j):
               
                    now = datetime.datetime.now()
                    present=now.year
                    exp1.append(str(present))
           
           
            exp1.sort()
            if len(exp1)!=0:
                years=int(exp1[-1])-int(exp1[0])
                #print("\n")
                #print("The number of experienced years = ")
                #print(years)
                return years
            else:
                return 0
                
            
           
