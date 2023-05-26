import { Link } from 'react-router-dom';

export default function Navbar({page}: {page: string}) {
    return(
        <div id='navbar-wrapper'>
            <div className='flex-container-row'>
                <div className='left-side'>
                </div>

                <div className='right-side'>
                    <Link id={page === 'FileUpload' ? 'active' : ''} className='nav-element' to='/'>
                        Upload Files
                    </Link>  
                    <Link id={page === 'AskGPT' ? 'active' : ''} className='nav-element' to='/askgpt'>
                        Ask GPT
                    </Link>
                </div>
            </div>
        </div>
    );
}