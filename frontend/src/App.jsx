import { BrowserRouter } from 'react-router-dom'
import ErrorBoundary from './ErrorBoundary'
import { HistoryAIModule } from './modules/history-ai'

function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <HistoryAIModule />
      </BrowserRouter>
    </ErrorBoundary>
  )
}

export default App
