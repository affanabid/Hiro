import fitz  # PyMuPDF

pdf_path = "AffanAbid-DS.pdf"
doc = fitz.open(pdf_path)

urls = []

for page_num in range(len(doc)):
    page = doc[page_num]
    links = page.get_links()
    for link in links:
        if "uri" in link:
            urls.append(link["uri"])

print("🔗 URLs found in PDF annotations:")
for u in urls:
    print("-", u)