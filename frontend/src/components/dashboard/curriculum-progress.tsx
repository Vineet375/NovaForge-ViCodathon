"use client"
import * as React from "react"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { BookOpen, Loader2 } from "lucide-react"
import { useCurriculum } from "@/hooks/useCurriculum"
import { Skeleton } from "@/components/ui/skeleton"

export function CurriculumProgress() {
  const { curriculum, loading, error } = useCurriculum()
  
  if (loading) {
    return (
      <Card className="shadow-premium">
        <CardHeader className="pb-4 border-b border-border">
          <Skeleton className="h-6 w-[200px]" />
        </CardHeader>
        <CardContent className="pt-4 p-0">
          <div className="flex flex-col p-4 space-y-6">
            {[1, 2, 3].map((i) => (
              <div key={i} className="flex items-start gap-4">
                <Skeleton className="h-6 w-6 rounded-full" />
                <div className="space-y-2 flex-1">
                  <Skeleton className="h-4 w-[200px]" />
                  <Skeleton className="h-3 w-[150px]" />
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    )
  }

  if (error || !curriculum) {
    return (
      <Card className="shadow-premium h-full min-h-[300px] flex items-center justify-center">
        <p className="text-sm text-red-500">{error || "Failed to load curriculum"}</p>
      </Card>
    )
  }

  const total = curriculum.days.length

  return (
    <Card className="shadow-premium">
      <CardHeader className="pb-4 border-b border-border">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg font-semibold flex items-center gap-2">
            <BookOpen className="h-5 w-5 text-primary" />
            Curriculum Overview
          </CardTitle>
          <span className="text-sm font-medium bg-primary/10 text-primary px-2.5 py-0.5 rounded-full">
            {total} Days
          </span>
        </div>
      </CardHeader>
      <CardContent className="pt-4 p-0">
        <div className="flex flex-col">
          {curriculum.days.map((day, index) => (
            <div 
              key={day.day} 
              className={`flex items-start gap-4 p-4 transition-colors hover:bg-muted/30 ${index !== curriculum.days.length - 1 ? 'border-b border-border/50' : ''}`}
            >
              <div className="flex-shrink-0 mt-0.5">
                <div className="h-6 w-6 rounded-full border-2 border-primary flex items-center justify-center text-xs font-bold text-primary">
                  {day.day}
                </div>
              </div>
              <div className="flex-1 min-w-0">
                <h4 className="text-sm font-semibold text-foreground">
                  {day.title}
                </h4>
                <div className="flex flex-wrap gap-2 mt-2">
                  {day.tools.slice(0, 3).map((tool) => (
                    <span key={tool} className="text-xs bg-muted px-2 py-0.5 rounded-md text-muted-foreground">
                      {tool}
                    </span>
                  ))}
                  {day.tools.length > 3 && (
                    <span className="text-xs bg-muted px-2 py-0.5 rounded-md text-muted-foreground">
                      +{day.tools.length - 3} more
                    </span>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
