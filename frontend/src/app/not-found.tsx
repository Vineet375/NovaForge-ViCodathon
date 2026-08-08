import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { PageContainer } from '@/components/layout/layout-foundation'
import { SearchX } from 'lucide-react'

export default function NotFound() {
  return (
    <DashboardLayout>
      <PageContainer className="flex items-center justify-center min-h-[70vh]">
        <div className="flex flex-col items-center text-center space-y-6 max-w-md animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div className="w-20 h-20 bg-muted/50 rounded-full flex items-center justify-center border-4 border-background shadow-premium">
            <SearchX className="w-10 h-10 text-muted-foreground" />
          </div>
          <div className="space-y-2">
            <h1 className="text-4xl font-bold tracking-tight">404</h1>
            <h2 className="text-xl font-semibold">Page not found</h2>
            <p className="text-muted-foreground max-w-md">
              We couldn&apos;t find the page you&apos;re looking for. It might have been moved or deleted.
            </p>
          </div>
          <Link href="/">
            <Button className="shadow-premium-sm" size="lg">
              Return to Dashboard
            </Button>
          </Link>
        </div>
      </PageContainer>
    </DashboardLayout>
  )
}
