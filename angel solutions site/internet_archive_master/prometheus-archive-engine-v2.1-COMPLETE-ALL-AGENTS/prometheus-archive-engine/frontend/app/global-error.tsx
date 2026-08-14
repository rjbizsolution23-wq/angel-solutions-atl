'use client';

import React from 'react';

export const dynamic = "force-dynamic";

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <html>
      <body className="bg-slate-950 text-slate-100 min-h-screen flex items-center justify-center font-sans antialiased p-6">
        <div className="max-w-md w-full border border-red-500/20 bg-red-500/5 p-8 rounded-3xl text-center flex flex-col gap-6 items-center">
          <div className="h-16 w-16 rounded-2xl bg-red-500/10 border border-red-500/20 flex items-center justify-center text-red-500 font-mono text-xl font-black">
            FAULT
          </div>
          
          <div className="flex flex-col gap-2">
            <h2 className="text-lg font-black text-white uppercase tracking-tight">System Core Fault</h2>
            <p className="text-xs text-slate-400 leading-relaxed">
              A critical execution exception occurred within the active Prometheus Engine instance.
            </p>
          </div>

          <button
            onClick={() => reset()}
            className="w-full rounded-xl bg-red-600 hover:bg-red-500 text-white text-xs font-bold uppercase tracking-wider py-3.5 transition-colors shadow-lg shadow-red-600/10"
          >
            Re-Initialize System
          </button>
        </div>
      </body>
    </html>
  );
}
