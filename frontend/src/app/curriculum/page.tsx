import { DashboardLayout } from "@/components/layout/dashboard-layout"
import { CurriculumProgress } from "@/components/dashboard/curriculum-progress"

export default function CurriculumPage() {
  return (
    <DashboardLayout>
      <div className="p-8 max-w-5xl mx-auto space-y-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight mb-2">Curriculum</h1>
          <p className="text-muted-foreground">
            Review the course structure and view completion progress across cohorts.
          </p>
        </div>
        
        <CurriculumProgress />
      </div>
    </DashboardLayout>
  )
}
