import os  
from torch.nn.functional import cosine_similarity  # تصحيح: استيراد الدالة بشكل صحيح  

from ArabicDataAnalysis import settings  
from FileManagement.Father import clean_poetry, load_classified_data, load_classifier_model, load_model  

import torch  
from torch.nn.functional import cosine_similarity  # تأكد من هذا الاستيراد  

def find_poet(input_text, embed_model, classifier_model, classified_data):  
    """البحث عن الشاعر بناءً على البيت الشعري المدخل."""  
    # توليد تضمين للبيت المدخل  
    input_embedding = embed_model.encode([input_text])  
    input_embedding_tensor = torch.tensor(input_embedding)  # تحويل إلى Tensor  
    
    max_similarity = 0  
    poet = "لا توجد معلومات عن الشاعر"  # القيمة الافتراضية  

    for text, label in classified_data:  
        # توليد تضمين لكل بيت شعري في البيانات  
        text_embedding = embed_model.encode([text])  
        text_embedding_tensor = torch.tensor(text_embedding)  # تحويل إلى Tensor  
        
        # حساب نسبة التشابه باستخدام cosine_similarity   
        similarity = cosine_similarity(input_embedding_tensor, text_embedding_tensor).item()  

        # إذا كان نسبة التطابق أكبر، نقوم بتحديث الشاعر  
        if similarity > max_similarity:  
            max_similarity = similarity  
            poet = label  # تحديث الشاعر  

    # حساب نسبة النسبة بين 0 و 1  
    similarity_percentage = max_similarity * 100  

    return poet, similarity_percentage

 # نسبة التشابه تكون 0 إذا كان أقل من العتبة  
def StartUsingModel2(user_input):  
    # تحميل نموذج التضمين   
    app_name = 'FileManagement'  
    model_path = os.path.join(settings.BASE_DIR, app_name, 'static', 'model', 'DownloadModel')  
    model = load_model(model_path)  

    model_Data_directory = os.path.join(settings.BASE_DIR, app_name, 'static', 'model', 'modelSave')  
    classifier_model = load_classifier_model(model_Data_directory)  
    classified_data = load_classified_data(model_Data_directory)  

    # تنظيف الإدخال من المستخدم  
    user_input = clean_poetry(user_input)  

    # البحث عن الشاعر  
    poet, similarity_percentage = find_poet(user_input, model, classifier_model, classified_data)  

    # تنسيق النتائج  
    print(poet)  
    print(similarity_percentage)  
    
    if similarity_percentage < 80:  
        results = []  # لا توجد نتائج  
        getmessage = "لا توجد نتائج لعرضها."  
    else:  
        results = [{"poet_name": poet, "similarity_score": similarity_percentage}]  # ترتيب البيانات بصيغة مناسبة  
        getmessage = ""  # لا توجد رسالة هنا لأن النتائج موجودة  

    return {"results": results, "getmess": getmessage}