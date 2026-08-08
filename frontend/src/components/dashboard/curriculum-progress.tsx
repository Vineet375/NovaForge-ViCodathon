"use client"
import * as React from "react"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { BookOpen, CheckCircle2, Loader2 } from "lucide-react"
import { useCurriculum } from "@/hooks/useCurriculum"

export function CurriculumProgress() {
  const { curriculum, loading, error } = useCurriculum()
  
  if (loading) {
    return (
      <Card className="shadow-premium h-full min-h-[300px] flex items-center justify-center">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
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

  // Calculate mock progress since the backend doesn't store per-user progress yet
  const modules = curriculum.days.map((day, index) => ({
    id: `m${day.day_number}`,
    title: day.title,
    progress: index === 0 ? 100 : index === 1 ? 65 : 0,
    status: index === 0 ? "completed" : index === 1 ? "in-progress" : "not-started"
  }))

  const completed = modules.filter(m => m.progress === 100).length
  const total = modules.length
  const overallProgress = Math.round((modules.reduce((acc, m) => acc + m.progress, 0)) / total)

  return (
    <Card className="shadow-premium">
      <CardHeader className="pb-4 border-b border-border">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg font-semibold flex items-center gap-2">
            <BookOpen className="h-5 w-5 text-primary" />
            Curriculum Progress
          </CardTitle>
          <span className="text-sm font-medium bg-primary/10 text-primary px-2.5 py-0.5 rounded-full">
            {completed}/{total} Completed
          </span>
        </div>
        <div className="mt-4">
          <div className="flex justify-between text-sm mb-2">
            <span className="text-muted-foreground font-medium">Overall Completion</span>
            <span className="font-bold">{overallProgress}%</span>
          </div>
          <Progress value={overallProgress} className="h-2.5" />
        </div>
      </CardHeader>
      <CardContent className="pt-4 p-0">
        <div className="flex flex-col">
          {modules.map((mod, index) => (
            <div 
              key={mod.id} 
              className={`flex items-center gap-4 p-4 transition-colors hover:bg-muted/30 ${index !== modules.length - 1 ? 'border-b border-border/50' : ''}`}
            >
              <div className="flex-shrink-0 mt-0.5">
                {mod.progress === 100 ? (
                  <CheckCircle2 className="h-5 w-5 text-green-500" />
                ) : (
                  <div className="h-5 w-5 rounded-full border-2 border-muted-foreground/30 flex items-center justify-center">
                    {mod.progress > 0 && <div className="h-2 w-2 rounded-full bg-primary" />}
                  </div>
                )}
              </div>
              <div className="flex-1 min-w-0">
                <h4 className={`text-sm font-medium truncate ${mod.progress === 100 ? 'text-muted-foreground line-through' : 'text-foreground'}`}>
                  Day {index + 1}: {mod.title}
                </h4>
                {mod.progress > 0 && mod.progress < 100 && (
                  <div className="flex items-center gap-3 mt-2">
                    <Progress value={mod.progress} className="h-1.5 flex-1" />
                    <span className="text-xs text-muted-foreground font-medium w-8">{mod.progress}%</span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}

