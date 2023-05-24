# Image processing functions utilizing OCR
from libraryHeaders import *

# Converts pixmap buffer into numpy array
def pix2np(pix):
    # pix.samples = sequence of bytes of the image pixels like RGBA
    # pix.h = height in pixels
    # pix.w = width in pixels
    # pix.n = number of components per pixel (depends on the colorspace and alpha)
    im = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)

    try:
        im = np.ascontiguousarray(im[..., [2, 1, 0]])  # RGB To BGR
    except IndexError:
        # Convert Gray to RGB
        im = cv2.cvtColor(im, cv2.COLOR_GRAY2RGB)
        im = np.ascontiguousarray(im[..., [2, 1, 0]])  # RGB To BGR

    return im

# Loops through the captured text of an image and arranges this text line by line
# This function depends on the image layout
def generate_ss_text(ss_details, min_confidence):
    # Arrange the captured text after scanning the page
    parse_text = []
    word_list = []
    last_word = ''

    # Loop through the captured text of the entire page
    for seq in range(len(ss_details['text'])):
        word = ss_details['text'][seq]
        # If the word captured is not empty
        if word != '':
            # Only consider words with a confidence score of at least <min_confidence>
            if float(ss_details['conf'][seq]) <= min_confidence:
                continue
                
            # Add it to the line word list
            word_list.append(word)
            last_word = word
        if (last_word != '' and word == '') or (word == ss_details['text'][-1]):
            parse_text.append(word_list)
            word_list = []

    return parse_text

# Calculate the confidence score of the text grabbed from the scanned image
def calculate_ss_confidence(ss_details: dict):
    # page_num  --> Page number of the detected text or item
    # block_num --> Block number of the detected text or item
    # par_num   --> Paragraph number of the detected text or item
    # line_num  --> Line number of the detected text or item
    # Convert the dict to dataFrame
    df = pd.DataFrame.from_dict(ss_details)

    # Convert the field conf (confidence) to numeric
    df['conf'] = pd.to_numeric(df['conf'], errors='coerce')

    # Elliminate records with negative confidence
    df = df[df.conf != -1]

    # Calculate the mean confidence by page
    conf = df.groupby(['page_num'])['conf'].mean().tolist()

    return conf[0]