import * as React from "react"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { BookOpen, CheckCircle2 } from "lucide-react"

const modules = [
  {
    id: "m1",
    title: "System Design Fundamentals",
    progress: 100,
    status: "completed"
  },
  {
    id: "m2",
    title: "Advanced React Patterns",
    progress: 65,
    status: "in-progress"
  },
  {
    id: "m3",
    title: "Data Structures & Algorithms",
    progress: 0,
    status: "not-started"
  },
  {
    id: "m4",
    title: "Behavioral Interviews",
    progress: 0,
    status: "not-started"
  }
]

export function CurriculumProgress() {
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
                  {mod.title}
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
