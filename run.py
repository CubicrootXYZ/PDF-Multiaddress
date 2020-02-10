from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from PyPDF2 import PdfFileMerger, PdfFileReader

address_file = open("D://github_repos/pdf-inserter/addresses.txt", "r", encoding='utf-8')

addresses = address_file.read().split("---")
addresses = list(set(addresses))

i = 0
for adress in addresses:

    rows = adress.split("\n")
    rows = list(filter(None, rows))
    height = 23.6
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFont("Helvetica", 12)
    for row in rows:
        row = row.replace("*", "")
        if len(row)>34:
            spaces = row.rfind(" ", 0,34)
            if spaces != -1:
                can.drawString(2.5*cm, height*cm, row[:spaces])
                height -= 0.6
                can.drawString(2.5*cm, height*cm, row[spaces+1:])
                height -= 0.6
            else:
                can.drawString(2.5*cm, height*cm, row[:34])
                height -= 0.6
                can.drawString(2.5*cm, height*cm, row[34:])
                height -= 0.6
        else:
            can.drawString(2.5*cm, height*cm, row)
            height -= 0.6
 
    # create a new PDF with Reportlab
    
    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open("D://github_repos/pdf-inserter/original.pdf", "rb"))
    output = PdfFileWriter()
    num = existing_pdf.getNumPages()
    for j in range(num):       
        # add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.getPage(j)
        if j == 0:
            page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
    # finally, write "output" to a real file
    
    outputStream = open("D://github_repos/pdf-inserter/output"+str(i)+".pdf", "wb")
    output.write(outputStream)
    outputStream.close()
    i+=1

merger = PdfFileMerger()
for j in range(i):
    merger.append(PdfFileReader(open("D://github_repos/pdf-inserter/output"+str(j)+".pdf", 'rb')))

merger.write("D://github_repos/pdf-inserter/document-output.pdf")