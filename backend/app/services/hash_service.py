import hashlib


def hash_resume(resume_text):
    return hashlib.sha256(resume_text.encode("utf-8")).hexdigest()