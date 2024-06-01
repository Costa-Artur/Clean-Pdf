import pikepdf

def redact_text(pdf_path, output_path, search_text, replacement_text=""):
    try:
        # Open the original PDF document
        pdf = pikepdf.open(pdf_path)
        
        # Iterate through each page and perform find and replace
        for page in pdf.pages:
            # Check if the page has contents
            if '/Contents' in page:
                contents = page['/Contents']
                
                # Handle case where contents is a single stream
                if isinstance(contents, pikepdf.Stream):
                    content_stream = contents.read_bytes().decode('latin1')
                    content_stream = content_stream.replace(search_text, replacement_text)
                    page['/Contents'] = pikepdf.Stream(pdf, content_stream.encode('latin1'))
                
                # Handle case where contents is an array of streams
                elif isinstance(contents, pikepdf.Array):
                    new_contents = pikepdf.Array()
                    for content in contents:
                        content_stream = content.read_bytes().decode('latin1')
                        content_stream = content_stream.replace(search_text, replacement_text)
                        new_contents.append(pikepdf.Stream(pdf, content_stream.encode('latin1')))
                    page['/Contents'] = new_contents

        # Save the modified PDF to a new file
        pdf.save(output_path)
        print(f"Redaction complete. Output saved to {output_path}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    redact_text("teste.pdf", "output.pdf", "<TEXT TO REPLACE>")
