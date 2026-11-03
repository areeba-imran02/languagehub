import './globals.css';
import type { Metadata } from 'next';
export const metadata:Metadata={title:'LanguageHub — Every Language, One Platform',description:'AI-powered multilingual language learning'};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body>{children}</body></html>}
