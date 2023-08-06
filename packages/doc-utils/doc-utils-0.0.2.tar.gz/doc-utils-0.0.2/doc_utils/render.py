from hashlib import sha1

import os

import requests

from doc_utils.fill import fill_document_cached


def render_docx_to_pdf(server, docx_file, with_callback=None):
    data = None

    if with_callback:
        data = {"webhookURL": with_callback}

    r = requests.post(
        f"{server}/convert/office",
        files={'file.docx': docx_file},
        data=data
        # headers={'Content-Type': 'multipart/form-data'}
    )
    if with_callback:
        return

    if r.status_code != 200:
        raise Exception(f"Can not convert document: {r.content}")

    return r


def merge_pdf_documents(server, files, cache_dir):
    files_data = {}

    hash = sha1()

    for idx, file in enumerate(files):
        with open(file, 'rb') as f:
            data = f.read()
            hash.update(data)
            files_data[f"{idx:03}_{os.path.basename(file)}"] = data

    cache_file_dir = f"{cache_dir}/{hash.hexdigest()}"
    cache_file_name = f"{cache_file_dir}/all.pdf"

    if os.path.exists(cache_file_name):
        return cache_file_name

    if not os.path.exists(cache_file_dir):
        os.makedirs(cache_file_dir)

    r = requests.post(
        f"{server}/merge",
        files=files_data,
        # headers={'Content-Type': 'multipart/form-data'}
    )
    if r.status_code != 200:
        raise Exception(f"Can not convert document: {r.content}")

    with open(cache_file_name, 'wb') as f:
        f.write(r.content)

    return cache_file_name


def render_document_cached(server, source, data, cache_dir, with_callback=None):
    source_file_path = fill_document_cached(source, data, cache_dir)
    if source_file_path.endswith(".pdf"):
        return source_file_path

    pdf_file_path = f"{source_file_path}.pdf"

    if not with_callback and os.path.exists(pdf_file_path):
        return pdf_file_path

    with open(source_file_path, 'rb') as source:
        pdf = render_docx_to_pdf(server, source, with_callback=with_callback)

    if with_callback:
        return

    with open(pdf_file_path, 'wb') as target:
        for chunk in pdf:
            target.write(chunk)

    return pdf_file_path
