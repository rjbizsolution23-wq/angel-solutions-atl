'use client'

import * as React from 'react'
import { ChatWidget } from './chat-widget'

export function ClientChatWidget() {
  const [mounted, setMounted] = React.useState(false)

  React.useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) return null

  return <ChatWidget />
}
