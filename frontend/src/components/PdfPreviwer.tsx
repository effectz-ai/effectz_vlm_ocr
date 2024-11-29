import { Viewer, Worker} from "@react-pdf-viewer/core";
import '@react-pdf-viewer/default-layout/lib/styles/index.css';
import '@react-pdf-viewer/core/lib/styles/index.css'
import '@react-pdf-viewer/toolbar/lib/styles/index.css';
import type {ToolbarSlot, TransformToolbarSlot} from '@react-pdf-viewer/toolbar'
import {toolbarPlugin} from "@react-pdf-viewer/toolbar";

type HighlighterProps = {
    pdfUrl: string;
}
export function PdfPreviewer ({pdfUrl}:HighlighterProps)  {
    const toolBarPluginInstance = toolbarPlugin()
    const {renderDefaultToolbar, Toolbar} = toolBarPluginInstance
    const transform: TransformToolbarSlot = (slot: ToolbarSlot) => ({
        ...slot,
        Download: () => <></>,
        DownloadMenuItem: () => <></>,
        EnterFullScreen: () => <></>,
        EnterFullScreenMenuItem: () => <></>,
        SwitchTheme: () => <></>,
        SwitchThemeMenuItem: () => <></>,
        Open: () => <></>,
        Print: () => <></>,
    });



    return(
        <div className="viewer h-[80vh] overscroll-auto">
            {pdfUrl && (
                // eslint-disable-next-line @typescript-eslint/ban-ts-comment
                // @ts-expect-error
                <Worker workerUrl="https://unpkg.com/pdfjs-dist@3.4.120/build/pdf.worker.min.js">
                    <Toolbar>{renderDefaultToolbar(transform)}</Toolbar>
                    {/* eslint-disable-next-line @typescript-eslint/ban-ts-comment */}
                    {/*// @ts-expect-error*/}
                    <Viewer fileUrl={pdfUrl}/>
                </Worker>
            )}
            {!pdfUrl && <>No Analyzed Files</>}
        </div>
    )
}