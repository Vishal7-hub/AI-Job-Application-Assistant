import fitz

def extract_text_from_pdf(file_bytes : bytes) -> str :
    # Extracting readable text from the pdf file

    text_parts =[]
    with fitz.open(stream = file_bytes,filetype = "pdf") as pdf:
        for page in pdf:
            text_parts.append(page.get_text())

    extracted_text = "\n".join(text_parts).strip()

    if not extracted_text:
        raise ValueError(
            "No readable text found. The pdf may be scanned or image-based"

        )
    return extracted_text
