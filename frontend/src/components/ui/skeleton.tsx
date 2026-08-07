import { cn } from "@/lib/utils"

function Skeleton({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn("animate-pulse rounded-md bg-muted", className)}
      {...props}
    />
  )
}

function CardSkeleton() {
  return (
    <div className="rounded-xl border border-border bg-card p-6 shadow-premium">
      <div className="space-y-3">
        <Skeleton className="h-6 w-2/5" />
        <Skeleton className="h-4 w-4/5" />
      </div>
      <div className="mt-6 space-y-4">
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-3/4" />
      </div>
    </div>
  )
}

function PageHeaderSkeleton() {
  return (
    <div className="flex flex-col space-y-2 pb-8">
      <Skeleton className="h-8 w-1/3" />
      <Skeleton className="h-4 w-1/2" />
    </div>
  )
}

export { Skeleton, CardSkeleton, PageHeaderSkeleton }
