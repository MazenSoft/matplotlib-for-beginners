from pdfminer.high_level import extract_text  
import docx2txt  
import re  

def split_sentences(text):
    """
    تقسيم النص إلى جمل باستخدام تعبيرات عادية.
    """
    # تحديد نهايات الجمل (نقطة، علامة استفهام، علامة تعجب)
    sentence_endings = re.compile(r'(?<=[.!?]) +')
    sentences = sentence_endings.split(text)
    return [s.strip() for s in sentences if s.strip()]  # إزالة الفراغات الزائدة وإرجاع الجمل غير الفارغة

def clean_text(text):
    """
    تنظيف النص عن طريق إزالة علامات الترقيم غير المطلوبة.
    """
    # الاحتفاظ بالعربية والفراغات والرموز الضرورية
    text = re.sub(r'[^\w\s#.,!?;]', '', text)
    text = re.sub(r'\n+', ' ', text)  # إزالة الأسطر الجديدة
    text = re.sub(r'\s+', ' ', text)  # إزالة الفراغات الزائدة
    return text.strip()  # إزالة الفراغات من البداية والنهاية

def DataAnalysis(file, content_type):
    """
    تحليل البيانات من ملف معين وتنظيف النص وتقسيمه إلى جمل.
    """
    text = Processfile(file, content_type)
    print(text)

    # تنظيف النص
    cleaned_text = clean_text(text)

    # تقسيم النص إلى جمل
    sentences = split_sentences(cleaned_text)

    print("عدد الجمل:", len(sentences))
    print(sentences)
    return sentences

def Processfile(file, content_type):  
    if content_type == 'application/pdf':  
       text = get_text_from_pdf(file)  
    elif content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':  
       text = get_text_from_docx(file)   
    else:  
       text = None   
    return text  

def get_text_from_pdf(file):  
    # تحويل ملف PDF إلى نص  
    text = extract_text(file)  
    return text  

def get_text_from_docx(file):  
    # تحويل ملف Word إلى نص  
    text = docx2txt.process(file)  
    return text