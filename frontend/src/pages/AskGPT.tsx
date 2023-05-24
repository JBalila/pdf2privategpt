// Library imports
import { useState } from 'react';
import axios from 'axios';

// Component imports
import Navbar from '../components/Navbar';
import QueryResponse from '../components/QueryResponse';
import { buildPath } from '../components/BuildPath';

enum QueryStatusTypes {
    IDLE = 'Idle',
    PROCESSING = 'Processing query...'
}

export default function AskGPT() {
    const [query, setQuery] = useState<string>('');
    const [queryStatus, setQueryStatus] = useState<QueryStatusTypes>(QueryStatusTypes.IDLE);
    const [queryResponse, setQueryResponse] = useState<string>('');

    // Send <query> to <privateGPT.py> on the Flask server
    const askQuery = async (): Promise<void> => {
        // Store <query> as JSON payload
        const jsonPayload = JSON.stringify(query);

        // Reset <query>
        setQuery('');
        setQueryStatus(QueryStatusTypes.PROCESSING);

        // Hit Flask backend
        try {
            const response = await axios.post(buildPath('askgpt'), 
                jsonPayload, {
                    headers: {
                        "Content-type": "application/json"
                    }
                });

            setQueryResponse(queryResponse + response.data);
            setQueryStatus(QueryStatusTypes.IDLE);
        }
        catch(error) {
            setQueryStatus(QueryStatusTypes.IDLE);
            console.log(error);
        }
    }

    return(
        <div>
            <Navbar page={'AskGPT'} />

            <h1>Ask GPT</h1>

            <div id='query-wrapper'>
                <div id='query-output'>
                    <QueryResponse queryResponse={queryResponse} />
                </div>
                <input id='query-input' placeholder='Enter a query...' 
                    value={query !== null ? query : ''} onChange={(e) => setQuery(e.target.value)}
                    autoFocus />
                { queryStatus === QueryStatusTypes.IDLE ?
                    <button className='button' onClick={askQuery}>Ask Query</button>
                :
                    <p>{queryStatus}</p>
                }
            </div>
        </div>
    );
}