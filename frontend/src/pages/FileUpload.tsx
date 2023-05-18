// Library imports
import { useState, useRef } from 'react';
import axios from 'axios';

// Component imports
import Navbar from '../components/Navbar';

enum FileStatusTypes {
    IDLE = 'Idle',
    PROCESSING = 'Processing file(s)...'
}

export default function FileUpload() {
    // Store file information uploaded by User
    const [files, setFiles] = useState([]);
    const [fileStatus, setFileStatus] = useState(FileStatusTypes.IDLE);

    // For determining drag-and-drop functionality
    const [dragActive, setDragActive] = useState(false);
    const fileUploadRef = useRef<HTMLLabelElement>(null);

    // Handles whenever drag-event happens
    const handleDrag = function(e: any) {
        e.preventDefault();
        e.stopPropagation();

        if (e.type === "dragenter" || e.type === "dragover")
            setDragActive(true);
        else if (e.type === "dragleave")
            setDragActive(false);
    }

    // User drops file into box
    const handleDrop = function(e: any) {
        e.preventDefault();
        e.stopPropagation();

        setDragActive(false);

        // We have the file
        if (e.dataTransfer.files && e.dataTransfer.files[0])
            setFiles(e.dataTransfer.files);
    }

    // User clicks on the form to manually upload a file
    const handleManualUpload = function(e: any) {
        e.preventDefault();

        // We have the file
        if (e.target.files && e.target.files[0])
            setFiles(e.target.files);
    }

    // User clicks on the button to manually upload a file
    const handleClick = () => {
        if (fileUploadRef && fileUploadRef.current)
            fileUploadRef.current.click();
    }

    // Uses OCR to turn these PDFs into .txt files
    // Runs <pdf2text.py> on a Flask webserver
    const processFiles = async function() {
        let formData = new FormData();
        Object.values(files).forEach(file => {
            formData.append('file', file);
        });

        try {
            setFileStatus(FileStatusTypes.PROCESSING);
            const response = await axios.post('http://localhost:5000/processFiles',
                formData, {
                    headers: {
                        "Content-type": "multipart/form-data"
                    }
                });
            setFileStatus(FileStatusTypes.IDLE);

            console.log(response.data);
        }
        catch(error) {
            console.log(error);
            setFileStatus(FileStatusTypes.IDLE);
        }
    }

    return(
        <div>
            <Navbar page={'FileUpload'} />
            <h1>Upload File(s)</h1>

            {/* Handles the drag-and-drop or manual uploading of files */}
            <form id='file-upload-form' onDragEnter={handleDrag} onSubmit={(e) => e.preventDefault()}>
                <input type='file' id='file-upload-input' multiple={true} onChange={handleManualUpload} />
                <label ref={fileUploadRef} id='file-upload-label' htmlFor='file-upload-input' className={dragActive ? "drag-active" : ""}>
                    <div>
                        <p>Drag and drop or</p>
                        <button id='upload-button' onClick={handleClick}>Upload one or more files</button>
                    </div>
                </label>
                { dragActive === true && <div id="drag-file-element" onDragEnter={handleDrag} onDragLeave={handleDrag} onDragOver={handleDrag} onDrop={handleDrop}></div> }
            </form>

            {/* Display 'Process File(s)' button or status of files */}
            { fileStatus === FileStatusTypes.IDLE && <button className='button' onClick={processFiles}>Process file(s)</button> }
            { fileStatus !== FileStatusTypes.IDLE && <p>{ fileStatus }</p> }
        </div>
    );
}