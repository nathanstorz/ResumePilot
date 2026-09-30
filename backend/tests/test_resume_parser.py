from app.services.resume_parser import clean_resume_text


def test_clean_resume_text_removes_extra_whitespace():
    text = "Nathan   Storz\n\nComputer Science    Student"

    result = clean_resume_text(text)

    assert result == "Nathan Storz Computer Science Student"

def test_clean_resume_text_handles_empty_text():
    result = clean_resume_text("")

    assert result == "THIS SHOULD FAIL"

def test_clean_resume_text_handles_newlines_and_tabs():
    text = "Nathan\tStorz\nComputer Science\nStudent"

    result = clean_resume_text(text)

    assert result == "Nathan Storz Computer Science Student"