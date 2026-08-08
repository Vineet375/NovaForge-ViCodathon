"use client"
import * as React from "react"
import { Card } from "@/components/ui/card"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Search, Loader2 } from "lucide-react"
import { useCandidates } from "@/hooks/useCandidates"
import { useRouter } from "next/navigation"
import { useInterview } from "@/hooks/useInterview"
import { Candidate } from "@/lib/api"
import { CandidateModal } from "@/components/dashboard/candidate-modal"

export function CandidateSelector() {
  const { candidates, loading, error } = useCandidates()
  const { startInterview, loading: startingInterview } = useInterview()
  const [search, setSearch] = React.useState("")
  const [selectedCandidate, setSelectedCandidate] = React.useState<Candidate | null>(null)

  const filtered = candidates.filter(c => {
    const nameMatch = c.member.name.toLowerCase().includes(search.toLowerCase())
    const roleMatch = c.member.jobRole.toLowerCase().includes(search.toLowerCase())
    return nameMatch || roleMatch
  })

  const handleStart = async (id: string) => {
    if (startingInterview) return
    await startInterview(id)
  }

  return (
    <>
      <Card className="overflow-hidden">
        <div className="border-b border-border bg-muted/30 px-4 py-3 flex items-center gap-2">
          <Search className="h-4 w-4 text-muted-foreground" aria-hidden="true" />
          <input 
            type="text"
            placeholder="Search candidates..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="bg-transparent border-none outline-none text-sm w-full placeholder:text-muted-foreground"
            aria-label="Search candidates"
          />
        </div>
        <div className="flex flex-col max-h-[400px] overflow-y-auto" role="region" aria-label="Candidates list">
          {loading && (
            <div className="p-8 flex justify-center text-muted-foreground">
              <Loader2 className="h-6 w-6 animate-spin" />
            </div>
          )}
          {error && (
            <div className="p-4 text-sm text-red-500 text-center">
              {error}
            </div>
          )}
          {!loading && !error && filtered.length === 0 && (
            <div className="p-12 flex flex-col items-center justify-center text-center space-y-3">
              <div className="w-12 h-12 rounded-full bg-muted flex items-center justify-center">
                <Search className="h-6 w-6 text-muted-foreground opacity-50" />
              </div>
              <p className="text-sm font-medium text-foreground">No candidates found</p>
              <p className="text-xs text-muted-foreground">Try adjusting your search query.</p>
            </div>
          )}
          {!loading && !error && filtered.map((candidate) => {
            // Derive a small tech stack representation from completed missions
            const techStack = Array.from(new Set(
              candidate.missions
                .filter(m => m.passed)
                .map(m => {
                  if (m.title.includes("Embeddings") || m.title.includes("Vector")) return "Vector DB"
                  if (m.title.includes("Prompt")) return "Prompt Eng"
                  if (m.title.includes("API") || m.title.includes("Backend")) return "Backend API"
                  if (m.title.includes("Agent")) return "Agentic AI"
                  if (m.title.includes("Frontend")) return "React"
                  if (m.title.includes("Data")) return "Data Processing"
                  return "AI Core"
                })
            ))

            return (
              <div 
                key={candidate.member.id}
                onClick={() => setSelectedCandidate(candidate)}
                className={`flex items-center gap-4 p-4 cursor-pointer transition-colors hover:bg-muted/50 border-l-2 border-l-transparent ${startingInterview ? 'opacity-50 pointer-events-none' : ''}`}
              >
                <Avatar>
                  <AvatarFallback>{candidate.member.name.substring(0, 2).toUpperCase()}</AvatarFallback>
                </Avatar>
                <div className="flex-1 overflow-hidden">
                  <div className="flex items-center justify-between">
                    <h4 className="text-sm font-semibold truncate">{candidate.member.name}</h4>
                  </div>
                  <p className="text-xs text-muted-foreground truncate">
                    {candidate.member.jobRole} ({candidate.member.yearsExperience} yrs exp)
                  </p>
                  <div className="flex gap-1 mt-1.5 flex-wrap">
                    {techStack.slice(0, 3).map((skill) => (
                      <Badge key={skill} variant="secondary" className="px-1.5 py-0 text-[10px] h-4">
                        {skill}
                      </Badge>
                    ))}
                    {techStack.length > 3 && (
                      <Badge variant="secondary" className="px-1.5 py-0 text-[10px] h-4">
                        +{techStack.length - 3}
                      </Badge>
                    )}
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      </Card>
      
      {selectedCandidate && (
        <CandidateModal 
          candidate={selectedCandidate}
          onClose={() => setSelectedCandidate(null)}
          onStart={handleStart}
          isStarting={startingInterview}
        />
      )}
    </>
  )
}
