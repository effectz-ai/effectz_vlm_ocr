'use client'

import { useState } from 'react'
import Header from '@/components/Header'
import FileToHTML from './tabs/file-to-html/page'
import FileToJSON from './tabs/file-to-json/page'
import FileToMarkdown from './tabs/file-to-markdown/page'
import FileToXML from './tabs/file-to-xml/page'
import UrlToMarkdown from './tabs/url-to-markdown/page'
import { File, FileCode, FileJson, FileText, FileXIcon, Link, ArrowRight } from 'lucide-react'

const tabs = [
  { id: 'file_to_html', label: 'File to HTML', component: FileToHTML, icon1: File, icon2: FileCode },
  { id: 'file_to_json', label: 'File to JSON', component: FileToJSON, icon1: File, icon2: FileJson },
  { id: 'file_to_markdown', label: 'File to Markdown', component: FileToMarkdown, icon1: File, icon2: FileText },
  { id: 'file_to_xml', label: 'File to XML', component: FileToXML, icon1: File, icon2: FileXIcon },
  { id: 'url_to_markdown', label: 'URL to Markdown', component: UrlToMarkdown, icon1: Link, icon2: FileText },
]

export default function Home() {
  const [activeTab, setActiveTab] = useState(tabs[0].id)

  return (
    <div className="min-h-screen bg-gray-100">
      <Header />
      <nav className="bg-white shadow-md w-full overflow-x-auto custom-scroll">
        <ul className="flex justify-between">
          {tabs.map((tab) => (
            <li key={tab.id} className="flex-1">
              <button
                onClick={() => setActiveTab(tab.id)}
                className={`w-full px-4 py-2 font-bold transition-colors flex items-center justify-center ${
                  activeTab === tab.id
                    ? 'bg-green-900 text-white'
                    : 'bg-white text-green-900 hover:bg-green-600 hover:text-white'
                }`}
              >
                <span className="hidden md:inline">{tab.label}</span>
                <span className="md:hidden flex items-center space-x-2"><tab.icon1 /><ArrowRight /><tab.icon2 /></span>
              </button>
            </li>
          ))}
        </ul>
      </nav>
      <main className="container mx-auto mt-8 px-4">
        {tabs.map((tab) => (
          activeTab === tab.id && <tab.component key={tab.id} />
        ))}
      </main>
    </div>
  )
}

