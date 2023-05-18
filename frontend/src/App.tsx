// Library imports
import React from 'react';
import { BrowserRouter, Routes, Route} from 'react-router-dom';

// Component imports
import Home from './pages/Home';
import FileUpload from './pages/FileUpload';
import AskGPT from './pages/AskGPT';

// CSS imports
import './App.css';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/">
            <Route index element={<Home />} />
            <Route element={<FileUpload />} path="uploadfiles" />
            <Route element={<AskGPT />} path="askgpt" />
          </Route>
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
