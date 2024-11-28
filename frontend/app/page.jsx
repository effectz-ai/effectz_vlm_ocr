"use client"
import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import Header from '../components/header';
import FilePreview from '../components/file-preview';

export default function Home() {
  const [file, setFile] = useState(null);
  const [markdownModelType, setMarkdownModelType] = useState('');
  const [previewContent, setPreviewContent] = useState(null);
  const [result, setResult] = useState(null);
  const [markdown, setMarkdown] = useState('');
  const [loading, setLoading] = useState(false);

  const API_URL = process.env.NEXT_PUBLIC_API;

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);

    if (selectedFile) {
      if (selectedFile.type === 'application/pdf') {
        setPreviewContent(URL.createObjectURL(selectedFile)); 
      } else if (selectedFile.type.includes('image')) {
        setPreviewContent(URL.createObjectURL(selectedFile)); 
      } else if (selectedFile.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
        setPreviewContent('Word file selected'); 
      } else {
        setPreviewContent(null);
      }
    }
  };

  const handleSubmit = async () => {
    if (!file) {
      alert('Please upload a file.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('markdownModelType', markdownModelType);

    setLoading(true);

    try {
      const response = await fetch(`${API_URL}get_markdown`, {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setMarkdown(data.markdown);
      setResult(JSON.stringify(data, null, 2));
    } catch (error) {
      console.error('Error:', error);
      setResult('Failed to fetch the result.');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    const blob = new Blob([markdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'result.md';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="container">
      <Header />
      <div className="form">
        <div className="form-group">
        <label htmlFor="fileInput" className="upload-button">
          <i className="fas fa-upload"></i>Upload File
        </label>
        <input
          id="fileInput"
          type="file"
          accept=".pdf,.jpg,.png"
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />
        </div>
        <div className="form-group">
          <label htmlFor="markdownModelType">Model Type</label>
          <select id="markdownModelType" value={markdownModelType} onChange={(e) => setMarkdownModelType(e.target.value)}>
            <option value="ollama">Ollama: llama3.2-vision</option>
            <option value="openai">OpenAI: gpt-4o-mini</option>
          </select>
        </div>
        <button className='generate-button' onClick={handleSubmit}><i className="fas fa-gear"></i>Generate</button>
      </div>
      <div className="output">
        <div className="preview">
          <FilePreview file={file} content={previewContent} />
        </div>
        <div className={`result${loading || !result ? '-no' : ''}`}>
          {loading ? (
              <div className="spinner"></div>
          ) : result ? (
            <>
              <ReactMarkdown>{markdown}</ReactMarkdown>
              <button className='download-button' onClick={handleDownload}><i className="fas fa-download"></i>Download .md</button>
            </>
          ) : (
              <p className="result-placeholder">Markdown View</p>
          )}
        </div>
      </div>
    </div>
  );
}