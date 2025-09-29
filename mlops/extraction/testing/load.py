from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
import os
import re


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "pdfs")

def load_pdf_files(data):
    loader = DirectoryLoader(
        data,
        glob='*.pdf',
        loader_cls=PyPDFLoader
    )
    documents = loader.load()
    return documents

documents = load_pdf_files(data=DATA_PATH)


full_text = "\n".join([doc.page_content for doc in documents])

# Regex patterns
phone_pattern = r'(\+?\d[\d\s-]{7,}\d)'   # matches phone numbers like +92 3094503679, 123-456-7890
# url_pattern = r'(https?://\S+|www\.\S+)'  # matches URLs

# Extract matches
phones = re.findall(phone_pattern, full_text)
# urls = re.findall(url_pattern, full_text)

# Remove duplicates
phones = list(set(phones))
# urls = list(set(urls))

# Print results
print("Phone Numbers Found:")
for p in phones:
    print("-", p)

# print("\n URLs Found:")
# for u in urls:
#     print("-", u)

print(f"Total Documents Loaded: {len(documents)}\n")

for i, doc in enumerate(documents, start=1):
    print(f"--- Document {i} ---")
    print(f"Source: {doc.metadata.get('source', 'N/A')}")
    print(f"Page: {doc.metadata.get('page', 'N/A')+1} of {doc.metadata.get('total_pages', 'N/A')}")
    print("\nPage Content:\n")
    print(doc.page_content.strip())
    print("\n" + "="*80 + "\n")


