"use client"
import { useState } from 'react';
import {PdfPreviewer} from "@/components/PdfPreviwer";

interface FileUploaderProps {
    onFileChange: (file: File) => void;
}

export default function FileUploader({ onFileChange }: FileUploaderProps) {
    const [file, setFile] = useState<File | null>(null);
    const [preview, setPreview] = useState<string >('');

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            const selectedFile = e.target.files[0];
            setFile(selectedFile);
            onFileChange(selectedFile);

            if (selectedFile.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = (e) => setPreview(e.target?.result as string);
                reader.readAsDataURL(selectedFile);
            } else if (selectedFile.type === 'application/pdf') {
                setPreview(URL.createObjectURL(selectedFile));
            } else {
                setPreview('');
            }
        }
    };


    return (
        <div className="flex flex-col items-center space-y-4">
            <label htmlFor="file-upload" className="px-4 py-2 bg-green-900 text-white rounded cursor-pointer hover:bg-green-600 transition-colors">
                Upload File
            </label>
            <input
                id="file-upload"
                type="file"
                accept=".pdf,.jpg,.jpeg,.png,.doc,.docx"
                onChange={handleFileChange}
                className="hidden"
            />
            {file && (
                <div className="w-full max-h-[600px] overflow-y-auto border border-gray-300 rounded p-4">
                    {file.type.startsWith('image/') && (
                        <img src={preview!} alt="Uploaded file" className="max-w-full h-auto" />
                    )}
                    {file.type === 'application/pdf' && preview !== '' && (
                        <PdfPreviewer pdfUrl={preview}/>
                    )}
                    {file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' && (
                        <p className="text-gray-600">Word document uploaded: {file.name}</p>
                    )}
                </div>
            )}
        </div>
    );
}

