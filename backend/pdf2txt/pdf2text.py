from libraryHeaders import *
from imagePreprocessing import *
from imageProcessing import *
from multiprocessing import Pool
import time
import os

NUM_PROCESSES = os.cpu_count() // 2
PDF_FOLDER = os.path.join('PDF_Folder')
TXT_FOLDER = os.path.join('TXT_Folder')

# Scans an image buffer or an image file
# Pre-processes the image
# Calls the Tesseract engine with pre-defined parameters
# Calculates the confidence score of the image grabbed content
# Generates the text content of the image
# Prints a summary to the console
def ocr_img(img: np.array, inputFile: str):
    # If image source file is inputted as a parameter
    if inputFile:
        # Reading image using opencv
        inputPath = os.path.join(PDF_FOLDER, inputFile)
        img = cv2.imread(inputPath)

    # Convert image to binary
    bin_img = convert_img2bin(img)

    # Calling Tesseract
    # Tesseract Configuration parameters
    # oem --> OCR engine mode = 3 >> Legacy + LSTM mode only (LSTM neutral net mode works the best)
    # psm --> page segmentation mode = 6 >> Assume as single uniform block of text (How a page of text can be analyzed)
    config_param = r'--oem 3 --psm 6'

    # Feeding image to tesseract
    details = pytesseract.image_to_data(bin_img, output_type=Output.DICT, config=config_param, lang='eng')
 
    # Generates the text content of the image with at least 40.0 confidence
    output_data = None
    if details:
        output_data = generate_ss_text(details, 40.0)
    
    # This means the image was passed directly as a parameter
    # Textify this and save it to 'TXT_Folder/'
    if inputFile:
        outputFile = os.path.splitext(inputFile)[0] + '_(textified).txt'
        outputPath = os.path.join(TXT_FOLDER, outputFile)

        # Save string data in <outputText>
        outputText = ''
        for strList in output_data:
            for string in strList:
                outputText += (string + ' ')
            outputText += '\n'
        outputText += '\n'

        # Save to text file
        with open(outputPath, 'w') as textFile:
            textFile.write(outputText)
        
    # Return summary of image-processing and output-data
    return output_data

# Converts an image into a byte array
def image_to_byte_array(image: Image):
    imgByteArr = BytesIO()
    image.save(imgByteArr, format=image.format if image.format else 'JPEG')
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

# Converts <page> to text
def convertPage(inputPath: str, pg_num: int):
    pdfIn = fitz.open(inputPath)
    page = pdfIn[pg_num]

    # Rotation angle
    rotate = int(0)

    # PDF Page is converted into a whole picture 1056*816 and then for each picture a screenshot is taken
    # zoom = 1.33333333 -----> Image size = 1056*816
    # zoom = 2 ---> 2 * Default Resolution (text is clear, image text is hard to read)    = filesize small / Image size = 1584*1224
    # zoom = 4 ---> 4 * Default Resolution (text is clear, image text is barely readable) = filesize large
    # zoom = 8 ---> 8 * Default Resolution (text is clear, image text is readable)        = filesize large
    zoom_x = 8
    zoom_y = 8

    # The zoom factor is equal to 2 in order to make text clear
    # Pre-rotate is to rotate if needed
    mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)

    # Get a screen-shot of the PDF page
    # alpha -> Transparancy indicator
    # Colorspace -> represents the color space of the pixmap (csRGB, csGRAY, csCMYK)
    pix = page.get_pixmap(matrix=mat, alpha=False, colorspace="csGRAY")

    # Convert the screen-shot pix to numpy array
    img = pix2np(pix)

    # Erode image to omit or thin the boundaries of the bright area of the image
    # We apply Erosion on binary images
    kernel = np.ones((2,2), np.uint8)
    img = cv2.erode(img, kernel, iterations=1)
    pg_output_data = ocr_img(img=img, inputFile=None)
    
    return pg_num, pg_output_data

# Opens the input PDF File
# Creates a DataFrame for storing pages statistics
# Iterates throughout the chosen pages of the input PDF file
# Converts the screen-shot pix to a numpy array
# Scans the grabbed screen-shot
# Collects the statistics of the screen-shot(page)
# Prints a summary to the console
def ocr_file(inputFile: str):
    # Opens the input PDF file
    inputPath = os.path.join(PDF_FOLDER, inputFile)
    pdfIn = fitz.open(inputPath)

    # Set default save location
    outputFile = os.path.splitext(inputFile)[0] + '_(textified).txt'
    outputPath = os.path.join(TXT_FOLDER, outputFile)

    # Get list of page numbers to iterate through
    pageInfo = list(map(lambda pageNum: (inputPath, pageNum), list(range(pdfIn.page_count))))

    # pageResults[0] -> <pg_num>
    # pageResults[1] -> <pg_output_data>
    with Pool(NUM_PROCESSES) as pool:
        # Use multiprocessing to speed up .txt conversion
        pageResults = pool.starmap(convertPage, pageInfo)

        # End pool workers
        pool.close()
        pool.join()
    print('Done converting pages...')

    # Sort <pageResults> by <pg_num>
    pageResults.sort(key=lambda x: x[0])

    # Iterate through <pageResults> and output data
    outputText = ''
    for page in pageResults:
        pg_num = page[0]
        pg_output_data = page[1]

        for strList in pg_output_data:
            for string in strList:
                outputText += (string + ' ')
        outputText += '\n'

    # Save to text file
    with open(outputPath, 'w') as textFile:
        textFile.write(outputText)
    
    # Close input file
    pdfIn.close()

def pdf2text(inputFile: str):
    startTime = time.time()

    # Process a PDF
    if os.path.splitext(inputFile)[1] == '.pdf':
        ocr_file(inputFile=inputFile)
    # Process an image
    else:
        ocr_img(img=None, inputFile=inputFile)

    endTime = time.time()
    runtime = endTime - startTime

    print("Converting text files: {:.4f} seconds".format(runtime))