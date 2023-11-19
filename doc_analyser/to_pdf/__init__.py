import subprocess
from doc_analyser import settings


def convert_file_to_pdf(doc_path):
    cmd = 'libreoffice --headless --invisible --convert-to pdf'.split() + [doc_path, '--outdir', settings.DOC_PREVIEW_PATH]
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    p.wait(timeout=60*20)
    stdout, stderr = p.communicate()
    if stderr:
        raise subprocess.SubprocessError(stderr)
