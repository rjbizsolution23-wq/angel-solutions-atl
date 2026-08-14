import type { Metadata } from 'next'
import { Inter, Playfair_Display } from 'next/font/google'
import './globals.css'
import { Header } from '@/components/layout/header'
import { Footer } from '@/components/layout/footer'
import { ThemeProvider } from '@/components/providers/theme-provider'
import { Toaster, ToastProvider } from '@/components/ui/toast'
import { ClientChatWidget } from '@/components/layout/client-chat-widget'

const inter = Inter({ 
  subsets: ['latin'],
  variable: '--font-sans',
  display: 'swap',
})

const playfair = Playfair_Display({
  subsets: ['latin'],
  variable: '--font-serif',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'Angel Solutions ATL | Elite Business, Tax & Financial Services',
  description: 'Transform your business with premium solutions from Angel Solutions ATL. Expert LLC formation, tax resolution, credit optimization, and business funding services. Empowering Atlanta entrepreneurs to scale faster.',
  keywords: [
    'business formation Atlanta',
    'LLC registration',
    'tax resolution services',
    'credit repair Atlanta',
    'business funding',
    'financial solutions',
    'tax debt relief',
    'business consulting',
    'Angel Solutions ATL',
  ],
  authors: [{ name: 'Angel Solutions ATL' }],
  creator: 'Angel Solutions ATL',
  publisher: 'Angel Solutions ATL Ltd Co.',
  metadataBase: new URL('https://angelsolutionsatl.com'),
  alternates: {
    canonical: '/',
  },
  openGraph: {
    title: 'Angel Solutions ATL | AI-Powered Business Systems',
    description: 'Transform your business with premium solutions. Expert business formation, tax resolution, and financial services in Atlanta.',
    url: 'https://angelsolutionsatl.com',
    siteName: 'Angel Solutions ATL',
    locale: 'en_US',
    type: 'website',
    images: [
      {
        url: '/og-image.jpg',
        width: 1200,
        height: 630,
        alt: 'Angel Solutions ATL - AI-Powered Systems',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Angel Solutions ATL | AI-Powered Business Systems',
    description: 'Transform your business with premium solutions from Atlanta\'s leading business consultants.',
    images: ['/og-image.jpg'],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  verification: {
    google: 'your-google-verification-code',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning className={`${inter.variable} ${playfair.variable}`}>
      <body className="font-sans antialiased">
        <ThemeProvider
          attribute="class"
          defaultTheme="dark"
          enableSystem
          disableTransitionOnChange={false}
        >
          <ToastProvider>
            <div className="relative flex min-h-screen flex-col">
              <Header />
              <main className="flex-1">{children}</main>
              <Footer />
            </div>
            <ClientChatWidget />
            <Toaster />
          </ToastProvider>
        </ThemeProvider>
      </body>
    </html>
  )
}
