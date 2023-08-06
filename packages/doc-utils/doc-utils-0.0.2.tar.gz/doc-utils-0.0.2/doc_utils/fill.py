import json
import os
from hashlib import sha1
from typing import Dict

from doc_utils.formats.docx import DocxDocument
from doc_utils.formats.pdf import PdfDocument
from doc_utils.formats.xlsx import XlsxDocument


def fill_document_cached(template_path, data: Dict[str, str], cache_dir: str):
    with open(template_path, 'rb') as source:
        source_hash = sha1(source.read()).hexdigest()
        data_hash = sha1(json.dumps(data, sort_keys=True, default=str).encode()).hexdigest()

    cache_file_dir = f"{cache_dir}/{source_hash}/{data_hash}"
    cache_file = os.path.join(cache_file_dir, os.path.basename(template_path))

    if os.path.exists(cache_file):
        return cache_file

    if not os.path.exists(cache_file_dir):
        os.makedirs(cache_file_dir)

    _fill_document(template_path, data, cache_file)
    print(cache_file)

    return cache_file


def _fill_document(template_path, data, target):
    if template_path.endswith(".docx"):
        document = DocxDocument(template_path)

    elif template_path.endswith(".xlsx"):
        document = XlsxDocument(template_path)

    elif template_path.endswith(".pdf"):
        document = PdfDocument(template_path)
    else:
        raise NotImplementedError(f"Unknown file format: {template_path}")

    print("Looking for variables")
    for var in document.find_variables():
        print(var.name)
        var.replace(data.get(var.name, ""))

    document.save(target)
