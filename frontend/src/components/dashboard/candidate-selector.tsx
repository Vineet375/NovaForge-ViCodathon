import * as React from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Search } from "lucide-react"

const candidates = [
  {
    id: "c1",
    name: "Alex Rivera",
    role: "Senior Frontend Engineer",
    avatar: "https://i.pravatar.cc/150?u=a042581f4e29026024d",
    progress: 84,
    skills: ["React", "System Design"],
    active: true
  },
  {
    id: "c2",
    name: "Sarah Chen",
    role: "Backend Developer",
    avatar: "https://i.pravatar.cc/150?u=a04258114e29026702d",
    progress: 45,
    skills: ["Python", "FastAPI"],
    active: false
  },
  {
    id: "c3",
    name: "David Kim",
    role: "Fullstack Engineer",
    avatar: "https://i.pravatar.cc/150?u=a04258114e29026302d",
    progress: 12,
    skills: ["Next.js", "PostgreSQL"],
    active: false
  }
]

export function CandidateSelector() {
  return (
    <Card className="overflow-hidden">
      <div className="border-b border-border bg-muted/30 px-4 py-3 flex items-center gap-2">
        <Search className="h-4 w-4 text-muted-foreground" />
        <input 
          type="text"
          placeholder="Search candidates..."
          className="bg-transparent border-none outline-none text-sm w-full placeholder:text-muted-foreground"
        />
      </div>
      <div className="flex flex-col max-h-[300px] overflow-y-auto">
        {candidates.map((candidate) => (
          <div 
            key={candidate.id}
            className={`flex items-center gap-4 p-4 cursor-pointer transition-colors hover:bg-muted/50 ${candidate.active ? 'bg-muted/20 border-l-2 border-l-primary' : 'border-l-2 border-l-transparent'}`}
          >
            <Avatar>
              <AvatarImage src={candidate.avatar} alt={candidate.name} />
              <AvatarFallback>{candidate.name.substring(0, 2).toUpperCase()}</AvatarFallback>
            </Avatar>
            <div className="flex-1 overflow-hidden">
              <div className="flex items-center justify-between">
                <h4 className="text-sm font-semibold truncate">{candidate.name}</h4>
                <span className="text-xs font-medium text-muted-foreground">{candidate.progress}%</span>
              </div>
              <p className="text-xs text-muted-foreground truncate">{candidate.role}</p>
              <div className="flex gap-1 mt-1.5 flex-wrap">
                {candidate.skills.map((skill) => (
                  <Badge key={skill} variant="secondary" className="px-1.5 py-0 text-[10px] h-4">
                    {skill}
                  </Badge>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </Card>
  )
}
