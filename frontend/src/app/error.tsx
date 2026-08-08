"use client" // Error components must be Client Components

import { useEffect } from 'react'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { PageContainer } from '@/components/layout/layout-foundation'
import { Button } from '@/components/ui/button'
import { ServerCrash } from 'lucide-react'

import { useRouter } from 'next/navigation'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  const router = useRouter()
  
  useEffect(() => {
    // Log the error to an error reporting service
    console.error(error)
  }, [error])

  return (
    <DashboardLayout>
      <PageContainer className="flex items-center justify-center min-h-[70vh]">
        <div className="flex flex-col items-center text-center space-y-6 max-w-md animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div className="w-20 h-20 bg-red-500/10 rounded-full flex items-center justify-center border-4 border-background shadow-premium">
            <ServerCrash className="w-10 h-10 text-red-500" />
          </div>
          <div className="space-y-2">
            <h1 className="text-3xl font-bold tracking-tight">System Unavailable</h1>
            <p className="text-muted-foreground leading-relaxed">
              We encountered a critical error communicating with our servers. Our engineering team has been notified.
            </p>
          </div>
          <div className="flex gap-4">
            <Button
              onClick={
                // Attempt to recover by trying to re-render the segment
                () => reset()
              }
              className="shadow-premium-sm"
              size="lg"
            >
              Try Again
            </Button>
            <Button variant="outline" size="lg" onClick={() => router.push('/')}>
              Go to Dashboard
            </Button>
          </div>
        </div>
      </PageContainer>
    </DashboardLayout>
  )
}
