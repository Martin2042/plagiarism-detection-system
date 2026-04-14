#import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def vectorize(Text): return TfidfVectorizer().fit_transform(Text).toarray()
def similarity(doc1, doc2): return cosine_similarity([doc1, doc2])


def compare_file(doc1, doc2):
    txt1 = open(doc1, encoding='utf-8').read()
    txt2 = open(doc2, encoding='utf-8').read()

    vectors = vectorize([txt1,txt2])
    s_vectors = list(zip([doc1,doc2], vectors))
    plagiarism_results = set()


    for doc_a, text_vector_a in s_vectors:
        new_vectors = s_vectors.copy()
        current_index = new_vectors.index((doc_a, text_vector_a))
        del new_vectors[current_index]
        for doc_b, text_vector_b in new_vectors:
            sim_score = similarity(text_vector_a, text_vector_b)[0][1]
            doc_pair = sorted((doc_a, doc_b))
            score = (doc_pair[0], doc_pair[1], sim_score)
            plagiarism_results.add(score)
    return plagiarism_results

def compare_text(txt1, txt2):
    vectors = vectorize([txt1,txt2])
    s_vectors = list(zip(['doc1','doc2'], vectors))
    plagiarism_results = set()


    for doc_a, text_vector_a in s_vectors:
        new_vectors = s_vectors.copy()
        current_index = new_vectors.index((doc_a, text_vector_a))
        del new_vectors[current_index]
        for doc_b, text_vector_b in new_vectors:
            sim_score = similarity(text_vector_a, text_vector_b)[0][1]
            doc_pair = sorted((doc_a, doc_b))
            score = (doc_pair[0], doc_pair[1], sim_score)
            plagiarism_results.add(score)
    return plagiarism_results

def compare_file_text(doc1, txt2):
    txt1 = open(doc1, encoding='utf-8').read()
    #txt2 = open(doc2, encoding='utf-8').read()

    vectors = vectorize([txt1,txt2])
    s_vectors = list(zip([doc1,'doc2'], vectors))
    plagiarism_results = set()


    for doc_a, text_vector_a in s_vectors:
        new_vectors = s_vectors.copy()
        current_index = new_vectors.index((doc_a, text_vector_a))
        del new_vectors[current_index]
        for doc_b, text_vector_b in new_vectors:
            sim_score = similarity(text_vector_a, text_vector_b)[0][1]
            doc_pair = sorted((doc_a, doc_b))
            score = (doc_pair[0], doc_pair[1], sim_score)
            plagiarism_results.add(score)
    return plagiarism_results

if __name__ == '__main__':

    txt1 = '''Life is all about doing your best in trying to
find what works out for you and taking most time in
trying to pursue those skills '''

    data = compare_text(txt1, txt1)##compare_file("./fatma.txt","./juma.txt")
    print(data)
    d2 = list(data)
    print(d2[0][2])