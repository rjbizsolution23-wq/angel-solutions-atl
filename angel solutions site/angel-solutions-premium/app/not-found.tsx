import Link from 'next/link'
import { ArrowRight, HelpCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'

export default function NotFound() {
  return (
    <div className="pt-20 min-h-screen bg-zinc-950 text-white flex flex-col justify-center relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-brand-gold-500/10 rounded-full blur-3xl pointer-events-none" />
      
      <div className="container mx-auto px-4 py-16 relative z-10 text-center max-w-xl space-y-8">
        <div className="w-20 h-20 bg-brand-gold-500/10 border border-brand-gold-500/30 rounded-3xl flex items-center justify-center mx-auto">
          <HelpCircle className="h-10 w-10 text-brand-gold-400" />
        </div>
        
        <div className="space-y-4">
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight">
            Asset <span className="text-gold-gradient">Not Found</span>
          </h1>
          <p className="text-sm md:text-base text-white/60">
            The requested page does not exist or has been archived. Let's get you back on track to business restoral and funding options.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button asChild size="lg" className="shadow-2xl">
            <Link href="/">
              Return Home
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </Button>
          <Button asChild size="lg" variant="outline" className="border-white/10 text-white hover:bg-white/10">
            <Link href="/contact">Contact Support</Link>
          </Button>
        </div>
      </div>
    </div>
  )
}
