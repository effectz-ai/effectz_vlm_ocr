import {Viewer, Worker} from "@react-pdf-viewer/core";
import '@react-pdf-viewer/default-layout/lib/styles/index.css';
import '@react-pdf-viewer/core/lib/styles/index.css'
import '@react-pdf-viewer/toolbar/lib/styles/index.css';

type HighlighterProps = {
    pdfUrl: string;
}

export function PdfPreviewer ({pdfUrl}:HighlighterProps)  {




    return(
        <div className="viewer h-[80vh] overscroll-auto">
            {pdfUrl && (
                <Worker workerUrl={`https://unpkg.com/pdfjs-dist@2.16.105/build/pdf.worker.js`}>
                        <Viewer fileUrl={pdfUrl}/>
                </Worker>
            )}
            {!pdfUrl && <>No Analyzed Files</>}
        </div>
    )
}