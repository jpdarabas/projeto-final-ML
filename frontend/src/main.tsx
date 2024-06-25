import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'
import { ContextProvider } from './context/context.tsx'
import { ModalProvider } from 'styled-react-modal'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ModalProvider>
      <ContextProvider>
        <App />
      </ContextProvider>
    </ModalProvider>
  </React.StrictMode>,
)
