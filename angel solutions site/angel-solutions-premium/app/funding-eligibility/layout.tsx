import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Business Funding & Credibility Eligibility Scanner | Angel Solutions ATL',
  description: 'Estimate your corporate borrowing potential. Our interactive scanner calculates eligibility score and matching capital options instantly.',
  alternates: {
    canonical: '/funding-eligibility',
  },
}

export default function FundingLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return children
}
