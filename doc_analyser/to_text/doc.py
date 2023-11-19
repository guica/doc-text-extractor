import docx
import json

def convert_docx_to_txt(filename):
    try:
        doc = docx.Document(filename.replace('\\','/'))
        print('Sucessfuly opened file')
    except Exception as e:
        print('Could not open docx {}'.format(filename))
        print(e)
        return ''

    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)

    return {'full': ''.join(fullText)}