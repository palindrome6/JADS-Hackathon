import PyPDF2


def pdf_to_text(path_file):
	reader=PyPDF2.pdf.PdfFileReader(path_file)
	eachPageText=[]
	for i in range(0,reader.getNumPages()):
		pageText=reader.getPage(i).extractText()
		eachPageText.append(pageText)
		completePDF = ' '.join(eachPageText)
		completePDF = completePDF.replace('\n','')
	return(completePDF)