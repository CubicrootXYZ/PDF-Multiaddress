# !/usr/bin/python3
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import tkinter.font as font
import tkinter.scrolledtext as scrolledtext
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from PyPDF2 import PdfFileMerger, PdfFileReader
import io
import shutil
from pathlib import Path


top = Tk()
top.geometry("800x600")
top.title("PDF Inserter")
orig = "-"
dest="-"
def setOriginal():
    global orig
    orig = filedialog.askopenfilename()
    var2.set(orig)
def setDestination():
    global dest
    dest = filedialog.askdirectory()
    var4.set(dest)
def convert():
    global orig
    global dest
    addresses_list = addresses.get('0.0', END)
    addresses_ = addresses_list.split("---")
    addresses_ = list(set(addresses_))

    print(orig)
    print(dest)
    if(len(orig) < 3 or len(dest) < 3):
        messagebox.showinfo("Fehler", "Keine Ein- oder Ausgabedatei oder keine Adressen")
        return
    

    i = 0
    out = []
    for adress in addresses_:
        if (len(adress) < 2):
            continue

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
        try:
            existing_pdf = PdfFileReader(open(orig, "rb"))
            output = PdfFileWriter()
            num = existing_pdf.getNumPages()
        except Exception as e:
            messagebox.showinfo("Fehler", e)
            return

        for j in range(num):       
            # add the "watermark" (which is the new pdf) on the existing page
            page = existing_pdf.getPage(j)
            if j == 0:
                page.mergePage(new_pdf.getPage(0))
            output.addPage(page)
        # finally, write "output" to a real file
        try:
            Path(dest+"/temp").mkdir(parents=True, exist_ok=True)
            outputStream = open(dest+"/temp/output"+str(i)+".pdf", "wb")
            output.write(outputStream)
            outputStream.close()
        except Exception as e:
            messagebox.showinfo("Fehler", e)
            return
        i+=1

    merger = PdfFileMerger()
    for j in range(i):
        try:
            file_ = open(dest+"/temp/output"+str(j)+".pdf", 'rb')
            merger.append(PdfFileReader(file_))
            file_.close()
        except Exception as e:
            messagebox.showinfo("Fehler", e)
            return

    try:
        merger.write(dest+"/document-output.pdf")
        shutil.rmtree(dest+'/temp')
    except Exception as e:
        messagebox.showinfo("Fehler", e)
        return



B1 = Button(top, text = "Original-PDF-Datei auswählen", command = setOriginal, font=('Helvetica', '14')).grid(row=0,column=1, pady=10)

var1 = StringVar()
label1 = Message(top, textvariable=var1, width=100).grid(row=1, column=0, pady=10)
var1.set("Datei gewählt:")

var2 = StringVar()
label2 = Message(top, textvariable=var2, width=300).grid(row=1, column=1, pady=10)
var2.set(orig)

B2 = Button(top, text = "Ziel-Ordner auswählen", command = setDestination, font=('Helvetica', '14')).grid(row=2,column=1, pady=10)

var0 = StringVar()
label0 = Message(top, textvariable=var0, width=100).grid(row=2, column=0, pady=10)
var0.set("Das Programm nutzt einen Unterordner temp, sollte dieser bereits vorhanden sein wird er gelöscht.")

var3 = StringVar()
label3 = Message(top, textvariable=var3, width=100).grid(row=3, column=0, pady=10)
var3.set("Ordner gewählt:")

var4 = StringVar()
label4 = Message(top, textvariable=var4, width=300).grid(row=3, column=1, pady=10)
var4.set(dest)

addresses =  scrolledtext.ScrolledText(top, height=8)
addresses.insert(END,'Vorname Nachname\nStraße Hsnr\nPLZ Stadt\n---')
addresses.grid(column=1, row=4)

var5 = StringVar()
label5 = Message(top, textvariable=var5, width=300).grid(row=4, column=0, pady=10, sticky=N)
var5.set("Adressen eingeben:")

B3 = Button(top, text = "PDF generieren", command = convert, font=('Helvetica', '14')).grid(row=5,column=1, pady=10)



top.mainloop()