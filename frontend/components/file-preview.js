import { useEffect, useState } from 'react';
import { Worker, Viewer } from '@react-pdf-viewer/core';
import '@react-pdf-viewer/core/lib/styles/index.css';
import '@react-pdf-viewer/default-layout/lib/styles/index.css';

export default function FilePreview({ file, content }) {
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  if (!file) {
    return <p className="preview-placeholder">File Preview</p>;
  }

  if (isClient && file.type === 'application/pdf') {
    return (
      <div style={{ width: '100%', height: '600px' }}>
        <Worker workerUrl={`https://unpkg.com/pdfjs-dist@3.11.174/build/pdf.worker.min.js`}>
          <Viewer fileUrl={content} />
        </Worker>
      </div>
    );
  }

  if (file.type.includes('image')) {
    return <img src={content} alt="Preview" className="preview-image" />;
  }

  return <p>Unsupported file type.</p>;
}
