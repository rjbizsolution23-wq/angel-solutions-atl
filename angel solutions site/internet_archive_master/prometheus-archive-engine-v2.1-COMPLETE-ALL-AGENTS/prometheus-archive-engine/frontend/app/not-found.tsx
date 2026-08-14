import React from "react";

export default function NotFound() {
  return (
    <div className="min-h-[60vh] flex flex-col items-center justify-center text-center p-6 gap-6">
      <div className="h-16 w-16 rounded-2xl bg-red-500/10 border border-red-500/20 flex items-center justify-center text-red-500 font-mono text-xl font-black">
        404
      </div>
      <div className="flex flex-col gap-2">
        <h2 className="text-xl font-bold text-white uppercase tracking-tight">Operator Node Not Found</h2>
        <p className="text-xs text-slate-400 max-w-sm leading-relaxed">
          The coordinate address or index file you requested does not exist in the active Prometheus database.
        </p>
      </div>
      <a 
        href="/"
        className="rounded-xl bg-sky-600 hover:bg-sky-500 text-white text-xs font-bold uppercase tracking-wider px-6 py-3 transition-colors text-center inline-block"
      >
        Return to Dashboard
      </a>
    </div>
  );
}
export const dynamic = "force-dynamic";
