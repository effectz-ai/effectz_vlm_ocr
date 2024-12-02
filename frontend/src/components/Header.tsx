import Image from 'next/image'
import Link from 'next/link'

export default function Header() {
    return (
        <header className="bg-white shadow-md">
            <div className="container mx-auto px-4 py-4 flex justify-between items-center">
                <h1 className="text-2xl font-bold text-gray-800">
                    Effectz VLM OCR
                </h1>
                <div className="flex items-center space-x-4">
                    <p className="text-sm text-gray-600">
                        Built by{' '}
                        <Link href="https://www.effectz.ai/" className="text-blue-600 hover:underline">
                            Effectz.AI
                        </Link>
                    </p>
                    <Image
                        src="/app-logo.svg"
                        alt="Effectz.AI Logo"
                        width={32}
                        height={32}
                        className="w-8 h-8 object-contain"
                    />
                </div>
            </div>
        </header>
    )
}
