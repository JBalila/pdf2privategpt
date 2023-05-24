// Library imports
import React from 'react';
import { BrowserRouter, Routes, Route} from 'react-router-dom';

// Component imports
import FileUpload from './pages/FileUpload';
import AskGPT from './pages/AskGPT';

// CSS imports
import './App.css';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route index element={<FileUpload />} path="/" />
          <Route element={<AskGPT />} path="/askgpt" />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
