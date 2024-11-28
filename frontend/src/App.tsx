
import { useState } from 'react';
import './App.css'
import FileUploader from './components/file-uploader'
import PdfPreviwer from './components/pdf-previewer';

function App() {
  const [pdfUrl, setPdfUrl] = useState<string>('');

  const handleFileSelect = (file: File) => {
    const url = URL.createObjectURL(file);
    setPdfUrl(url);
    console.log(url);
  }

  return (
    <div className='max-h-screen'>
      <FileUploader onFileSelect={handleFileSelect}/>
      {pdfUrl && <PdfPreviwer fileUrl={pdfUrl}/>}
      
    </div>
  )
}

export default App
