import pdfrw
from typing import List

from doc_utils.formats.base import BaseVariable, BaseDocument


def encode_pdf_string(value, ftype):
    if ftype == 'string':
        return pdfrw.objects.pdfstring.PdfString.encode(value or '')
    elif ftype == 'checkbox':
        if value == 'True' or value is True:
            return pdfrw.objects.pdfname.BasePdfName('/Yes')
        else:
            return pdfrw.objects.pdfname.BasePdfName('/No')
    return ''


class Variable(BaseVariable):
    def __init__(self, name, annotation, ftype):
        self.name = name
        self.annotation = annotation
        self.ftype = ftype

    def replace(self, value):
        self.annotation.update(pdfrw.PdfDict(V=encode_pdf_string(value, self.ftype)))
        self.annotation.update(pdfrw.PdfDict(Ff=1))
        self.annotation.update(pdfrw.PdfDict(AP=''))


def find_variables(doc) -> List[Variable]:
    variables_found = []

    for page in doc.pages:
        annotations = page['/Annots']

        for annotation in annotations:
            try:
                key = annotation['/T'][1: -1]
                ftype = 'checkbox' if annotation['/FT'] == '/Btn' else 'string'
                variables_found.append(Variable(key, annotation, ftype))
            except TypeError:
                pass

    return variables_found


class PdfDocument(BaseDocument):
    def __init__(self, file_or_path):
        super().__init__(file_or_path)
        self.doc = pdfrw.PdfReader(file_or_path)

    def find_variables(self) -> List[BaseVariable]:
        return find_variables(self.doc)

    def save(self, target):
        self.doc.Root.AcroForm.update(
            pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
        pdfrw.PdfWriter().write(target, self.doc)



