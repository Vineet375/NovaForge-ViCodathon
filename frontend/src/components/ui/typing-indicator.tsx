import * as React from "react"

export function TypingIndicator() {
  return (
    <div className="flex items-center gap-1.5 p-4 rounded-xl bg-muted/50 w-fit">
      <div className="w-2 h-2 bg-primary rounded-full animate-bounce [animation-delay:-0.3s]" />
      <div className="w-2 h-2 bg-primary rounded-full animate-bounce [animation-delay:-0.15s]" />
      <div className="w-2 h-2 bg-primary rounded-full animate-bounce" />
    </div>
  )
}
