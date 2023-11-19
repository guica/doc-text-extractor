from doc_analyser import app
from doc_analyser.tasks import convert_file_to_text
from doc_analyser.tasks import convert_to_pdf
from doc_analyser.settings import FULL_DOCS_PATH
from doc_analyser.settings import DOC_PREVIEW_PATH
from doc_analyser.document import TempDocument

from responses import RESPONSE_ERROR_FILE_SAVE
from responses import RESPONSE_ERROR_NO_FILE
from responses import RESPONSE_ERROR_DOC_ID

import json
from flask import request
from flask import Response
import os


@app.route('/to_text', methods=['POST'])
def test():
    content = None
    tmp_file = None

    if request.files.get('data', None): 
        content = json.load(request.files['data'])
    else:
        return RESPONSE_ERROR_NO_FILE

    if request.files['file'] and type(content["file_extention"]) == str:
        file = request.files['file']
        tmp_file = TempDocument(file, content["file_extention"])
    else:
        return RESPONSE_ERROR_NO_FILE

    if tmp_file:
        if type(content.get("id", None)) == int:
            id = convert_file_to_text.delay(
                content["id"],
                tmp_file.file_path_to_text,
                file_type=content["file_extention"]
            ).id
            convert_to_pdf.apply_async(
                queue='pdf',
                kwargs={'content': content, 'file_name': tmp_file.file_path_to_pdf},
            )
            return Response(json.dumps({'uuid': id}), status=201, mimetype='application/json')
        else:
            return RESPONSE_ERROR_DOC_ID
    else:
        return RESPONSE_ERROR_FILE_SAVE

@app.route('/doc_to_text', methods=['POST'])
def dispatch_doc_to_text():
    content = None
    tmp_file = None

    if request.files.get('data', None): 
        content = json.load(request.files['data'])
    else:
        return RESPONSE_ERROR_NO_FILE

    if request.files['file'] and type(content["file_extention"]) == str:
        file = request.files['file']
        tmp_file = TempDocument(file, content["file_extention"])
    else:
        return RESPONSE_ERROR_NO_FILE

    if tmp_file:
        if type(content.get("id", None)) == int:
            id = convert_file_to_text.delay(
                content["id"],
                tmp_file.file_path_to_text,
                file_type=content["file_extention"]
            ).id
            return Response(json.dumps({'uuid': id}), status=201, mimetype='application/json')
        else:
            return RESPONSE_ERROR_DOC_ID
    else:
        return RESPONSE_ERROR_FILE_SAVE

@app.route('/generate_doc_preview', methods=['POST'])
def dispatch_generate_doc_preview():
    content = None
    tmp_file = None

    if request.files.get('data', None): 
        content = json.load(request.files['data'])
    else:
        return RESPONSE_ERROR_NO_FILE

    if request.files['file'] and type(content["file_extention"]) == str:
        file = request.files['file']
        tmp_file = TempDocument(file, content["file_extention"])
    else:
        return RESPONSE_ERROR_NO_FILE

    if tmp_file:
        if type(content.get("id", None)) == int:
            id = convert_to_pdf.apply_async(
                queue='pdf',
                kwargs={'content': content, 'file_name': tmp_file.file_path_to_pdf},
            ).id
            return Response(json.dumps({'uuid': id}), status=201, mimetype='application/json')
        else:
            return RESPONSE_ERROR_DOC_ID
    else:
        return RESPONSE_ERROR_FILE_SAVE

@app.route('/get_result/<uuid>', methods=['GET'])
def bla(uuid):
    try:
        return convert_file_to_text.AsyncResult(uuid).get()
    except Exception as e:
        return e


if __name__ == "__main__":
    def create_dir(dir):
        if not os.path.exists(dir):
            os.mkdir(dir)

    create_dir(os.path.dirname(DOC_PREVIEW_PATH))
    create_dir(os.path.dirname(FULL_DOCS_PATH))
    create_dir(DOC_PREVIEW_PATH)
    create_dir(FULL_DOCS_PATH)


    app.run(debug=True, port=5000, host="0.0.0.0")