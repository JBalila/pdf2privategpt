// Library imports
import { useState } from 'react';
import axios from 'axios';

// Component imports
import Navbar from '../components/Navbar';

export default function AskGPT() {
    const [query, setQuery] = useState<string>('');
    const [queryResponse, setQueryResponse] = useState<string>('');

    // Send <query> to <privateGPT.py> on the Flask server
    const askQuery = async (): Promise<void> => {
        // Store <query> as JSON payload
        const jsonPayload = JSON.stringify(query);

        // Reset <query>
        setQuery('');

        // Hit Flask backend
        try {
            const response = await axios.post('http://localhost:5000/askgpt', 
                jsonPayload, {
                    headers: {
                        "Content-type": "application/json"
                    }
                });

            setQueryResponse(queryResponse + response.data);
        }
        catch(error) {
            console.log(error);
        }
    }

    return(
        <div>
            <Navbar page={'AskGPT'} />

            <h1>Ask GPT</h1>

            <div id='query-wrapper'>
                <div id='query-output'>
                    <p>{queryResponse}</p>
                </div>
                <input id='query-input' placeholder='Enter a query...' 
                    value={query !== null ? query : ''} onChange={(e) => setQuery(e.target.value)}
                    autoFocus />
                <button className='button' onClick={askQuery}>Ask Query</button>
            </div>
        </div>
    );
}