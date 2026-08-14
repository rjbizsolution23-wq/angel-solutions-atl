import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Prometheus Archive Engine v3.0 | RJ Business Solutions",
  description: "AI-powered web caching, digital preservation, book rebranding, and custom retro game packaging built by RJ Business Solutions."
};

export const dynamic = "force-dynamic";


export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-[#0f172a] text-slate-100 flex flex-col antialiased">
        {/* Premium Brand Header */}
        <header className="sticky top-0 z-50 w-full border-b border-slate-800 bg-[#0f172a]/80 backdrop-blur-md">
          <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
            <div className="flex items-center gap-3">
              {/* Brand Logo with Premium Border */}
              <div className="relative h-10 w-10 overflow-hidden rounded-lg border border-sky-500/30">
                <img 
                  src="https://storage.googleapis.com/msgsndr/qQnxRHDtyx0uydPd5sRl/media/67eb83c5e519ed689430646b.jpeg" 
                  alt="RJ Business Solutions"
                  width="40"
                  height="40"
                  className="h-full w-full object-cover"
                />
              </div>
              <div className="flex flex-col">
                <span className="text-sm font-semibold tracking-tight text-white uppercase">
                  Prometheus Engine
                </span>
                <span className="text-[10px] font-medium tracking-wide text-sky-400">
                  RJ BUSINESS SOLUTIONS
                </span>
              </div>
            </div>
            
            <nav className="hidden md:flex items-center gap-6 text-sm font-medium text-slate-300">
              <a href="#search" className="hover:text-sky-400 transition-colors">Search Portal</a>
              <a href="#rebrand" className="hover:text-sky-400 transition-colors">Book Rebranding</a>
              <a href="#arcade" className="hover:text-sky-400 transition-colors">Retro Arcade</a>
              <a href="#pricing" className="hover:text-sky-400 transition-colors">Pricing Tiers</a>
            </nav>

            <div className="flex items-center gap-4">
              <span className="hidden sm:inline-block text-xs text-slate-400">
                Operator: <strong className="text-white">Rick Jefferson</strong>
              </span>
              <a 
                href="#pricing" 
                className="rounded-full bg-sky-600 px-4 py-1.5 text-xs font-semibold text-white shadow-lg shadow-sky-600/20 hover:bg-sky-500 transition-all"
              >
                Access Pro
              </a>
            </div>
          </div>
        </header>

        <main className="flex-1 w-full mx-auto max-w-7xl px-6 py-8">
          {children}
        </main>

        {/* Premium Brand Footer */}
        <footer className="border-t border-slate-800 bg-[#0b0f19] py-8 text-center text-xs text-slate-500">
          <div className="mx-auto max-w-7xl px-6 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <span className="font-bold text-white uppercase">RJ Business Solutions</span>
              <span>© 2026. All Rights Reserved.</span>
            </div>
            <div className="flex gap-4">
              <a href="https://rjbusinesssolutions.org" target="_blank" className="hover:underline">rjbusinesssolutions.org</a>
              <span>•</span>
              <a href="mailto:support@rjbusinesssolutions.org" className="hover:underline">support@rjbusinesssolutions.org</a>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
