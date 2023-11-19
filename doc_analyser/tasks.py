from doc_analyser import celery
from doc_analyser.document.document import TempDocument
from doc_analyser.settings import CATEGORIZER_API_URL
from doc_analyser.settings import CATEGORIZER_API_AUTH_TOKEN
from doc_analyser.settings import DOC_PREVIEW_PATH
from doc_analyser.to_pdf import convert_file_to_pdf
from doc_analyser.get_key_words import generate_key_words

import json
import requests
import os
import spacy

def raise_for_status(r):
    if r.status_code >=300:
        print(r.content)
        raise requests.exceptions.HTTPError(f"Status code error: {r.status_code}, response: {r.content}")

class NlpModelTask(celery.Task):
    _nlp_model = None

    @property
    def get_nlp_model(self):
        if not self._nlp_model:
            self._nlp_model = spacy.load("pt_core_news_lg")
        return self._nlp_model

@celery.task(name='doc_analyser.tasks.get_keywords_from_text', base=NlpModelTask)
def get_keywords_from_text(doc_id, doc_text):
    nlp_model = get_keywords_from_text.get_nlp_model
    tags = generate_key_words(nlp_model, doc_text)

    data = json.dumps({'tags' : tags})
    headers = {
            'content-type': 'application/json',
            'Authorization': 'Token ' + CATEGORIZER_API_AUTH_TOKEN
        }
    res = requests.patch(CATEGORIZER_API_URL+str(doc_id)+'/',
        headers=headers,
        data=data,
        verify=False,
    )
    raise_for_status(res)

@celery.task(name='doc_analyser.tasks.convert_file_to_text')
def convert_file_to_text(file_id, file_name, file_type='PDF'):
    tmp_file = TempDocument(file_ext=file_type)

    try:
        doc_text = tmp_file.convert_to_text(file_name)

        if doc_text is not '':
            data = json.dumps({'full_text': doc_text['full']})
            headers = {
                    'content-type': 'application/json',
                    'Authorization': 'Token ' + CATEGORIZER_API_AUTH_TOKEN
                }
            res = requests.patch(CATEGORIZER_API_URL+str(file_id)+'/',
                headers=headers,
                data=data,
                verify=False,
            )
            raise_for_status(res)
            #get_keywords_from_text.delay(content['id'], doc_text['full'])
        
        tmp_file.remove_file(file_name)

    except Exception as e:
        tmp_file.remove_file(file_name)
        raise e

@celery.task(name='doc_analyser.tasks.convert_to_pdf')
def convert_to_pdf(content, file_name):
    tmp_file = TempDocument()
    doc_path = DOC_PREVIEW_PATH + os.path.basename(file_name).split('.')[0] + '.pdf'

    try:
        if content["file_extention"] == 'PDF':
            doc_path = file_name
        else:
            convert_file_to_pdf(file_name)
            tmp_file = TempDocument(file_path=doc_path)

        headers = {
                'Accept': 'application/json',
                'Authorization': 'Token ' + CATEGORIZER_API_AUTH_TOKEN
            }

        res = requests.patch(
            CATEGORIZER_API_URL+str(content['id'])+'/',
            headers=headers,
            files = {'preview_file': open(doc_path,'rb')},
            verify=False,
        )
        raise_for_status(res)

        tmp_file.remove_file([doc_path, file_name])

    except Exception as e:
        tmp_file.remove_file([doc_path, file_name])
        raise e
