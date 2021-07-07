""""
Patient_PDF_file_folder_sort_main
"""


import PyPDF2
import docx
import os
import shutil
import configparser
import sys


def word_search(words, text):
    """Returns True if all items in a str iterable object are in str text. Else returns False. Ignores case."""

    for word in words:
        if not str(word.lower()) in str(text.lower()):
            return False
    return True



def get_text(file):
    """Returns extracted text as string from either a .docx or .pdf file."""

    extracted_text = ""
    
    if file.endswith('.pdf'):
        pdffileobj = open(file, 'rb')
        pdfreader = PyPDF2.PdfFileReader(pdffileobj)
        for pdfpage in range(pdfreader.numPages):
            pageobj = pdfreader.getPage(pdfpage)
            extracted_text = extracted_text + str(pageobj.extractText())
        pdffileobj.close()
        extracted_text = extracted_text.replace('\n','')
            
    elif file.endswith('.docx'): #TODO: find a way for this to get the text box text too!! or not
        doc = docx.Document(file)
        doc_text = []
        for para in doc.paragraphs:
            doc_text.append(para.text)
        extracted_text = '\n'.join(doc_text)
            
    return extracted_text



def move_file(file_path, destination_path):
    """Moves a file from current location to another destination."""
    
    file_name = os.path.basename(file_path)
    destination_file_path = os.path.join(destination_path, file_name)

    if os.path.isfile(destination_file_path):
        print("File '" + file_name + "' already exists in destination.")
        file_name_copy =  "Copie_de_" + str(file_name)
        file_copy_at_destination = os.path.join(destination_path, file_name_copy)
        shutil.move(file_path, file_copy_at_destination)
        print("Document '" + file_name + "' renamed to '" + file_name_copy + "' and moved to folder '" + os.path.basename(destination_path) + "'.")
    
    else:
        shutil.move(file_path, destination_path)
        print("Document '" + file_name + "' moved to folder '" + os.path.basename(destination_path) + "'.")



def get_doc_filepaths(directory_path, file_ext):
    """Returns a list of file paths in specified directory with specified file paths."""
    
    file_paths = []
    for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path):
                if item.endswith(file_ext):
                    file_paths.append(item_path)
            else:
                continue
    return file_paths


def enter_to_exit():
    print("\nPress ENTER to exit the program.")
    input()
    sys.exit()



if __name__=="__main__":

    # get details from config.ini file
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')

        patient_file_folder = config['DIRECTORIES']['PatientFileDir']
        patient_folder_dir = config['DIRECTORIES']['PatientFolderDir']
    
    except:
        print("There was a problem accessing data from the config.ini file. Please check it has not been moved and restart the program.")
        enter_to_exit()


    # iterate over folders in patient folder directory
    for foldername in os.listdir(patient_folder_dir):
    
        # determine if item in patient folder directory is a directory
        if os.path.isdir(os.path.join(patient_folder_dir, foldername)):         
            
            # get new list of patient file paths updated for every for loop iteration
            file_paths_list = get_doc_filepaths(directory_path=patient_file_folder, file_ext='.pdf')
            
            # get list of file path-text pairs
            fileTextPairs = []
            for filePath in file_paths_list:
                fileText = get_text(filePath)
                fileTextPairs.append([filePath, fileText])
           
            # get split folder name
            splitFolderName = foldername.split()
             

            # match split folder name to list of file path-text pairs and move files
            for fileTextPair in fileTextPairs:
                
                if word_search(words=splitFolderName, text=fileTextPair[1]):
                    
                    # specify destination folder for matching file
                    patientFolder = os.path.join(patient_folder_dir, foldername)
                    move_file(file_path=fileTextPair[0], destination_path=patientFolder)

                else:
                    continue
    
    # print list of pdf files still remaining in patient file directory
    remainingPDFs = get_doc_filepaths(directory_path=patient_file_folder, file_ext='.pdf')

    if len(remainingPDFs) > 0:
        print("\nThe following PDF files could not be moved to a folder: \n")
        for item in remainingPDFs:
                print(os.path.basename(item))
    
    else:
        print("No more files to be moved.")
                
    print("\nProgram complete.")
    # enable perusal of messages by having user action end program
    enter_to_exit()
