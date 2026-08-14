'use client'

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <html lang="en">
      <body className="bg-zinc-950 text-white flex min-h-screen flex-col items-center justify-center p-4 font-sans">
        <div className="max-w-md w-full text-center space-y-6 bg-zinc-900 border border-white/10 p-8 rounded-3xl shadow-2xl">
          <h2 className="text-2xl font-bold text-amber-400">System Handshake Interrupted</h2>
          <p className="text-sm text-white/60">
            A temporary system boundary has been encountered. Let's restart the app runtime.
          </p>
          <button
            onClick={() => reset()}
            className="w-full py-2.5 bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-500 hover:to-amber-600 text-zinc-950 font-bold rounded-lg text-sm transition-all duration-200 cursor-pointer"
          >
            Reset Runtime View
          </button>
        </div>
      </body>
    </html>
  )
}
