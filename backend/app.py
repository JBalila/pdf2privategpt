# Library imports
import os
import sys
import typing
from flask import Flask, request
from werkzeug.utils import secure_filename
from flask_cors import CORS #comment this on deployment

# Import functions from child directories
sys.path.append('pdf2txt')
from pdf2text import pdf2text
sys.path.append('privateGPT')
from ingest import feedToGPT
from privateGPT import askQuery

NUM_PROCESSES = 4
PDF_FOLDER = os.path.join(os.getcwd(), 'PDF_Folder')
PDF2TXT_FOLDER = os.path.join(os.getcwd(), 'pdf2txt')
TXT_FOLDER = os.path.join(os.getcwd(), 'TXT_Folder')
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}
MEGABYTE = 1024 * 1024

app = Flask(__name__)
app.secret_key = "jiodasjfidsahnifpokndkalsfnddsahfuihdas"
CORS(app) #comment this on deployment

# Set settings for file-uploads
app.config['UPLOAD_FOLDER'] = PDF_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 35 * MEGABYTE

# Returns true if <filename> is allowed in this program, returns false otherwise
def allowedFile(filename: str) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Formats <messages> into a single string so that it can be returned as a response
def formatIntoReturnString(messages: [str]) -> str:
    returnMessage = ''

    for message in messages:
        returnMessage += message
        returnMessage += '\n'

    return returnMessage

# Full pipeline from uploading PDF file -> converting to .txt -> feeding to PrivateGPT
@app.route('/api/processFiles', methods=['POST'])
def processFiles() -> str:
    uploadFileRes = uploadFiles()
    print('Done uploading files...')
    pdf2txtRes = pdf2txt()
    print('Done converting files to .txt...')
    txt2gptRes = txt2gpt()
    print('Done feeding files to PrivateGPT...')
    return 'Done processing files'

# Uploads PDF/Image files to PDF_Folder
@app.route('/api/upload', methods=['POST'])
def uploadFiles() -> str:
    # User didn't use POST method (somehow)
    if request.method != 'POST':
        return 'Error: Only allows POST method'

    # Check if the post request has the file part
    if 'file' not in request.files:
        return 'No file part'

    # Get the file
    files = request.files.getlist('file')
    messages = []

    # Iterate through all files
    for file in files:
        # User did not select a file
        if file.filename == '':
            message = file.filename + ': File not selected'
            messages.append(message)
            continue

        # This type of file is not allowed
        if not allowedFile(file.filename):
            message = file.filename + ': File type not allowed'
            messages.append(message)
            continue
        
        # Try saving file to 'PDF_Folder/'
        savePath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        if os.path.exists(savePath):
            message = file.filename + ': File already uploaded'
            messages.append(message)
            continue
        
        file.save(savePath)
        message = file.filename + ': File successfully saved'
        messages.append(message)

    return formatIntoReturnString(messages)

# Runs <pdf2txt.py> on 'PDF_Folder/' and outputs resulting .txt files into 'TXT_Folder/'
# Deletes the converted PDF files from 'PDF_Folder/'
@app.route('/api/pdf2txt', methods=['POST'])
def pdf2txt() -> str:
    # Get list of files in 'PDF_Folder/'
    pdfList = os.listdir(PDF_FOLDER)

    # Unallowed file somehow got saved to 'PDF_Folder/', delete it
    for pdf in pdfList:
        if not allowedFile(pdf):
            print('Error: This should not have been saved in the first place')
            os.remove(os.path.join(PDF_FOLDER, pdf))
            pdfList.remove(pdf)
    
    # Iterate through each file in <pdfList>
    for pdf in pdfList:
        # Convert to .txt file
        pdf2text(pdf)

    # Remove from 'PDF_Folder/'
    for pdf in pdfList:
        os.remove(os.path.join(PDF_FOLDER, pdf))

    return 'Finished converting files'

# Runs <ingest.py> on 'TXT_Folder/', feeding the text files into PrivateGPT
# Deletes the ingested .txt files from 'TXT_Folder/'
@app.route('/api/txt2gpt', methods=['POST'])
def txt2gpt() -> str:
    # Get list of files in 'TXT_Folder/'
    txtList = os.listdir(TXT_FOLDER)

    # Run <ingest.py> on each .txt file in <txtList>
    feedToGPT(TXT_FOLDER)

    # Remove files from 'TXT_Folder/'
    for txt in txtList:
        os.remove(os.path.join(TXT_FOLDER, txt))

    return 'Finished feeding files to PrivateGPT'

@app.route('/api/askgpt', methods=['POST'])
def askgpt() -> str:
    # User didn't use POST method (somehow)
    if request.method != 'POST':
        return 'Error: Only allows POST method'

    query = request.get_json()
    queryResponse = askQuery(query)

    if queryResponse is None:
        return 'An unexpected error has occurred'

    return queryResponse