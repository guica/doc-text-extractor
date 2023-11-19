import json
from flask import Response

RESPONSE_ERROR_NO_FILE = Response(json.dumps({
        'status': 'File "file" or file "data[file_extension]" not present in request.'
    }), status=400, mimetype='application/json',
)

RESPONSE_ERROR_FILE_SAVE = Response(json.dumps({
        'status' : 'Error while saving received file.'
    }), status=400, mimetype='application/json',
)

RESPONSE_ERROR_DOC_ID = Response(json.dumps({
        'status' : 'No document ID received or ID not of type Int.'
    }), status=400, mimetype='application/json',
)