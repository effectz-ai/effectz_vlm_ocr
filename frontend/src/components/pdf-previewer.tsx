import {Worker, Viewer} from '@react-pdf-viewer/core';

type PdfPreviwerProps = {
    fileUrl: string
}

const PdfPreviwer = ({fileUrl}:PdfPreviwerProps) => {
  return (
    <div className='border-black overflow-y-auto'>
        <Worker workerUrl='https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.4.120/pdf.worker.min.js'>
            <Viewer fileUrl={fileUrl} />
        </Worker>
    </div>
  )
}

export default PdfPreviwer