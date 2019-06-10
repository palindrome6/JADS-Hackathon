from tika import parser
import pandas as pd
import io

def convert_pdf_to_text(row):
    path_to_pdfs = "../data/"
    path_to_save_text = "../data/text_files/"

    pdf_names = eval(row['PDFs'])
    pub_name = row['News']
    text_file_names = []

    if len(pdf_names) == 0:
        return text_file_names
    else:
        for file_name in pdf_names:
            path_to_open = path_to_pdfs + file_name
            raw = parser.from_file(path_to_open)
            file_to_save = path_to_save_text + file_name.strip('.pdf') + ".txt"

            with io.open(file_to_save, "w", encoding="utf-8") as outfile:
                outfile.write(raw['content'])
            text_file_names.append(file_name.strip('.pdf') + ".txt")
        return text_file_names


if __name__ =="__main__":
    df = pd.read_csv("../data/data.csv", delimiter='\t')
    df['text_file_names'] = df.apply(lambda row: convert_pdf_to_text(row), axis=1)
    df.drop(['Unnamed: 0', 'Misc'], axis=1, inplace=True)
    df.to_csv("../data/data.csv", sep='\t', index=False)