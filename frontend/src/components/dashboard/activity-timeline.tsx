import * as React from "react"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Activity, Code, MessageSquare, CheckCircle } from "lucide-react"

const activities = [
  {
    id: "a1",
    title: "Completed System Design Mock",
    description: "Scored 85% on distributed systems questions.",
    time: "2 hours ago",
    icon: CheckCircle,
    color: "text-green-500",
    bg: "bg-green-500/10"
  },
  {
    id: "a2",
    title: "Generated New Feedback",
    description: "AI identified 3 areas for improvement in React state management.",
    time: "5 hours ago",
    icon: MessageSquare,
    color: "text-blue-500",
    bg: "bg-blue-500/10"
  },
  {
    id: "a3",
    title: "Started Algorithm Practice",
    description: "Focused on dynamic programming patterns.",
    time: "Yesterday",
    icon: Code,
    color: "text-amber-500",
    bg: "bg-amber-500/10"
  }
]

export function ActivityTimeline() {
  return (
    <Card className="shadow-premium">
      <CardHeader className="pb-4">
        <CardTitle className="text-lg font-semibold flex items-center gap-2">
          <Activity className="h-5 w-5 text-primary" />
          Recent Activity
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="relative space-y-6 before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-border before:to-transparent">
          {activities.map((activity, index) => {
            const Icon = activity.icon
            return (
              <div key={activity.id} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group">
                <div className="flex items-center justify-center w-10 h-10 rounded-full border-4 border-background bg-background shadow-sm shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center ${activity.bg}`}>
                    <Icon className={`h-4 w-4 ${activity.color}`} />
                  </div>
                </div>
                
                <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded-xl border border-border bg-card/50 shadow-sm transition-all hover:shadow-premium-sm hover:bg-muted/30">
                  <div className="flex items-center justify-between mb-1">
                    <h4 className="text-sm font-semibold text-foreground">{activity.title}</h4>
                    <span className="text-xs font-medium text-muted-foreground">{activity.time}</span>
                  </div>
                  <p className="text-xs text-muted-foreground">{activity.description}</p>
                </div>
              </div>
            )
          })}
        </div>
      </CardContent>
    </Card>
  )
}
