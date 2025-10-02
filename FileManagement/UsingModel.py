import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from ArabicDataAnalysis import settings


def load_model_and_embeddings(model_directory, embeddings_file_name):
    
    model = SentenceTransformer(model_directory)
    # تحميل التضمينات المحفوظة
    embeddings_file = os.path.join(model_directory, embeddings_file_name)
    previous_embeddings = load_embeddings(embeddings_file)
    # تحميل الجمل السابقة
    previous_sentences_file = os.path.join(model_directory, 'previous_sentences.npy')
    previous_sentences = load_sentences(previous_sentences_file)

    return model, previous_embeddings, previous_sentences


def load_embeddings(embeddings_file):
    """تحميل التضمينات المحفوظة من الملف."""
    return np.load(embeddings_file)


def load_sentences(sentences_file):
    """تحميل الجمل المحفوظة من الملف."""
    return np.load(sentences_file, allow_pickle=True)  # تأكد من استخدام allow_pickle لتحميل الجمل بشكل صحيح


def compare_input_with_model(model, input_text, previous_embeddings, dim=None):
    """مقارنة نص إدخالي مع النموذج المدرب وحساب التشابه."""
    input_embedding = model.encode([input_text])

    # تحديد الأبعاد
    if dim and dim <= input_embedding.shape[1]:
        input_embedding = input_embedding[:, :dim]
        previous_embeddings = previous_embeddings[:, :dim]

    similarity_scores = cosine_similarity(input_embedding, previous_embeddings)
    return similarity_scores[0]

def StartModel(user_input, top_n):  
 
    getmess = None  
    app_name = 'FileManagement'  
    model_path = os.path.join(settings.BASE_DIR, app_name, 'static', 'model', 'completeTrainModel')  
    embeddings_file_name = 'previous_embeddings.npy'  
    model, previous_embeddings, previous_sentences = load_model_and_embeddings(model_path, embeddings_file_name)  

    # إدخال عدد الأبعاد  
    dim = 768  
    dim = dim if dim > 0 else None  

    # مقارنة النص المدخل بالنموذج  
    similarity_scores = compare_input_with_model(model, user_input, previous_embeddings, dim)  

# عدد الجمل الأكثر تشابهاً  
    results = []  

    # الحصول على مؤشرات الجمل الأكثر تشابهاً  
    most_similar_indices = similarity_scores.argsort()[::-1]  # الحصول على مؤشرات الجمل مرتبة من الأعلى إلى الأدنى  

    # تصفية النتائج بناءً على العتبة المحددة  
    similarity_threshold = 0.7  # عتبة اعتبار التشابه قوي  

    for i in most_similar_indices:  
        similarity_score = similarity_scores[i]  
        if similarity_score >= similarity_threshold:  
            results.append([previous_sentences[i], similarity_score])  

    # التحقق من عدد الجمل المتشابهة الموجودة  
    if len(results) == 0:  
        getmess = "لا توجد جمل مشابهة."  
    elif len(results) > top_n:  
        results = results[:top_n]  # احتفظ بالعدد المحدد فقط  
    # إذا لم يكن هناك شرط، يتم الاحتفاظ بجميع النتائج  

    print(results)  
    return results, getmess