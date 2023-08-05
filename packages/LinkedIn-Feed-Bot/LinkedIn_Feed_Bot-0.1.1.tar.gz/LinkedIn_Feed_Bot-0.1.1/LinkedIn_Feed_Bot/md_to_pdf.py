import markdown
from xhtml2pdf import pisa 

def convert(input_md_filepath, output_pdf_filename=None):
    """Simply convert an md file to pdf. You can choose the output name,
    but the default is the name of the input. 

    Args:
        input_md_filepath (str)
        output_pdf_filename (str, optional)

    Returns:
        [Boolean]: False means success and True means errors.
    """
    
    with open(input_md_filepath, "r", encoding="utf-8") as input_file:
        text = input_file.read()

    source_html = markdown.markdown(text)


    if(output_pdf_filename == None):
        str_split = output_pdf_filename.split('.')
        output_pdf_filename = str_split[0] + '.pdf'
    # open output file for writing (truncated binary)
    result_file = open(output_pdf_filename, "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
            source_html,                # the HTML to convert
            dest=result_file)           # file handle to recieve result

    # close output file
    result_file.close()                 # close output file

    # return False on success and True on errors
    return pisa_status.err