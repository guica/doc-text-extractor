import io
import json

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


def convert_pdf_to_txt(path):
    result = {}
    result['full'] = ''

    fp = None

    try:
        try:
            fp = open(path.replace('\\','/'), 'rb')
            print('Sucessfuly opened file')
        except:
            print('Could not open presentation')
            raise

        password = ""
        maxpages = 0
        caching = True
        pagenos = set()

        for i, page in enumerate(PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                        password=password,
                                        caching=caching,
                                        check_extractable=False)):

            rsrcmgr = PDFResourceManager()
            retstr = io.StringIO()
            codec = 'utf-8'
            laparams = LAParams()
            device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            interpreter.process_page(page)
            text = retstr.getvalue()
    #                 print('Text is:\n\n{}'.format(text.replace('\n\n',' ')))
            result[str(i+1)] = text
            result['full'] += text
            # p.page_content = text
            # p.page_num = i+1

            device.close()
            retstr.close()

        fp.close()
    #             print('Done with presentation {}'.format(path))

    except Exception as e:
        print('error on {}'.format(path))
        print(e)

    return result