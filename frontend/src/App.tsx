
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
    <>
      <FileUploader onFileSelect={handleFileSelect}/>
      <PdfPreviwer fileUrl={pdfUrl}/>
    </>
  )
}

export default App
