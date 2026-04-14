import docx

def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)
if __name__ == '__main__':
    st = getText('test.docx')
    print(st.strip())