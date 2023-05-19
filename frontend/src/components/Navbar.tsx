export default function Navbar({page}: {page: string}) {
    return(
        <div id='navbar-wrapper'>
            <div className='flex-container-row'>
                <div className='left-side'>
                    <a id={page === 'Home' ? 'active' : ''} className='nav-element' href='/'>
                        <p>Home</p>
                    </a>
                </div>

                <div className='right-side'>
                    <a id={page === 'FileUpload' ? 'active' : ''} className='nav-element' href='/uploadfiles'>
                        <p>Upload Files</p>
                    </a>
                    
                    <a id={page === 'AskGPT' ? 'active' : ''} className='nav-element' href='/askgpt'>
                        <p>Ask GPT</p>
                    </a>
                </div>
            </div>
        </div>
    );
}