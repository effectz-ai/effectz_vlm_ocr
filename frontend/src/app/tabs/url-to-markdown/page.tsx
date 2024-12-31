"use client"
import MarkdownViewer from "@/components/MarkdownViewer";
import {useState} from "react";
import axios from "axios";

export default function UrlToMarkdown() {
  const [url, setUrl] = useState<string>('');
  const [options, setOptions] = useState({
    headers: true,
    footers: true,
    tables: false,
    images: false,
    ads: true,
    buttons: true,
  });

  const handleOptionChange = (option: keyof typeof options) => {
    setOptions((prevOptions) => ({
      ...prevOptions,
      [option]: !prevOptions[option],
    }));
  };

  const handleApiCall = async (): Promise<string> => {
    if (!url) {
      throw new Error('Please enter a URL');
    }

    const formData = new FormData();
    formData.append('url', url);
    formData.append('options', JSON.stringify(options));

    try {
      const {data} = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/url_to_markdown`, formData);
      return data.markdown;
    } catch (error) {
      console.error('Error:', error);
      throw new Error('Failed to fetch the result.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4 text-green-950">Settings</h2>
            <div className="mt-4 w-full mb-2 text-center">
              <label htmlFor="url" className="block text-sm font-bold text-gray-700 mb-6">
                URL
              </label>
              <input
                id="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-md text-black mb-6"
                placeholder="Enter a URL"
              />
              <label htmlFor="options" className="block text-sm font-bold text-gray-700 mb-6">Ignore Options</label>
              {Object.keys(options).map((key) => (
                <div key={key} className="flex items-center ml-12 mb-6">
                  <input
                    type="checkbox"
                    id={key}
                    checked={options[key as keyof typeof options]}
                    onChange={() => handleOptionChange(key as keyof typeof options)}
                    className="mr-2 hidden"
                  />
                  <div
                    className="w-5 h-5 border-2 border-gray-300 rounded flex justify-center items-center cursor-pointer"
                    onClick={() => handleOptionChange(key as keyof typeof options)}
                  >
                    <svg
                      className={`w-3 h-3 ${options[key as keyof typeof options] ? 'text-green-900' : 'text-transparent'}`}
                      xmlns="http://www.w3.org/2000/svg"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                      stroke="currentColor"
                    >
                      <path
                        fillRule="evenodd"
                        d="M16.293 4.293a1 1 0 011.414 1.414L9 14.414 5.293 10.707a1 1 0 011.414-1.414L9 11.586l7.293-7.293z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </div>
                  <label htmlFor={key} className="text-sm font-medium text-gray-700 ml-4 cursor-pointer">
                    {key.charAt(0).toUpperCase() + key.slice(1)}
                  </label>
                </div>
              ))}
            </div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4 text-green-950">Markdown Viewer</h2>
            <MarkdownViewer onApiCall={handleApiCall} />
          </div>
        </div>
      </main>
    </div>
  );
}
