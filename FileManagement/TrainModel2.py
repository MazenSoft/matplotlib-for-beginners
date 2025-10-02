from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import os
import joblib
import pandas as pd

from ArabicDataAnalysis import settings
from FileManagement.Father import clean_poetry, load_classified_data, load_model

# قائمة لتخزين البيانات
train_data = []

def train_poetry_model(model, text, label, datapath):
    # تحميل البيانات المصنفة من ملف CSV
    existing_data = load_classified_data(datapath)

    # التحقق مما إذا كان النص موجودًا مسبقًا
    for existing_text, existing_label in existing_data:
        if existing_text == text:
            return "تم تدريب النص مسبقاً. لن يتم تدريبه مرة أخرى."

    # إضافة النص الجديد للبيانات
    existing_data.append((text, label))
    texts = [item[0] for item in existing_data]
    labels = [item[1] for item in existing_data]

    # توليد التضمينات
    embeddings = model.encode(texts)
    # ترميز التسميات
    le = LabelEncoder()
    encoded_labels = le.fit_transform(labels)

    # التدريب مباشرة على جميع العينات
    classifier = RandomForestClassifier()
    classifier.fit(embeddings, encoded_labels)

    # حفظ النموذج
    save_model(classifier, datapath)
    # حفظ بيانات التدريب
    save_classified_data(existing_data, datapath)

    return "تم تدريب النموذج"

def save_model(classifier, model_Data_directory):
    """حفظ النموذج المدرب."""
    model_path = os.path.join(settings.BASE_DIR, model_Data_directory, 'poetry_classifier.pkl')
    joblib.dump(classifier, model_path)

def save_classified_data(data, model_Data_directory):
    """حفظ البيانات المصنفة في ملف CSV."""
    output_path = os.path.join(settings.BASE_DIR, model_Data_directory, 'classified_data.csv')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # تحويل البيانات إلى DataFrame وحفظها
    df = pd.DataFrame(data, columns=['Text', 'Label'])

    try:
        df.to_csv(output_path, index=False, encoding='utf-8')
    except PermissionError:
        print(f"خطأ: لا يمكن الكتابة إلى {output_path}. تحقق من الأذونات.")
    except Exception as e:
        print(f"خطأ غير متوقع: {str(e)}")

def StartModel2(sentences, text, name):  
    app_name = 'FileManagement'  
    model_path = os.path.join(settings.BASE_DIR, app_name, 'static', 'model', 'DownloadModel')  
    model_Data_directory = os.path.join(settings.BASE_DIR, app_name, 'static', 'model', 'modelSave')  
    
    # تحميل النموذج  
    model = load_model(model_path)  
    
    grtResult = None  # إنشاء متغير لتخزين النتائج  

    if sentences is None and text:  # إذا لم يكن هناك جمل ولكن يوجد نص  
        text_cleaned = clean_poetry(text)  
        name_cleaned = clean_poetry(name)  
        grtResult = train_poetry_model(model, text_cleaned, name_cleaned, model_Data_directory)  
    elif sentences:  # إذا كان هناك جمل  
        for sentence in sentences:   
            cleaned_sentence = clean_poetry(sentence)  
            grtResult = train_poetry_model(model, cleaned_sentence, name, model_Data_directory)  
            # يمكنك جمع النتائج هنا إذا لزم الأمر 
    elif sentences and text:
        for sentence in sentences:   
            cleaned_sentence = clean_poetry(sentence)  
            grtResult = train_poetry_model(model, cleaned_sentence, name, model_Data_directory)
        grtResult = train_poetry_model(model, text, name, model_Data_directory)

    return grtResult