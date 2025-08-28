from langchain_community.document_loaders import PyPDFLoader
import fitz as pymupdf


def read_pdf_to_text(file_path):
    doc = pymupdf.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text
# print(read_pdf_to_text("resume0.pdf"))


def lang_pdfreader(file_path):

    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents

# print(lang_pdfreader("resume0.pdf"))