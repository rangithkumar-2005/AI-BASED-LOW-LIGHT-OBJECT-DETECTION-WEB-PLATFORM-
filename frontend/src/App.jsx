import { useState } from 'react'
import { motion } from 'framer-motion'
import Dashboard from './pages/Dashboard'

function Landing({ setView }) {
  return (
    <div className="min-h-screen p-8 flex flex-col items-center justify-center">
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="glass-card p-12 rounded-2xl max-w-4xl w-full text-center"
      >
        <h1 className="text-5xl font-bold mb-4 neon-text">
          NightVision Guardian AI
        </h1>
        <p className="text-gray-300 text-lg mb-8">
          AI-Powered Intelligent Night Surveillance & Low-Light Object Detection
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
          <div className="bg-gray-800/50 p-6 rounded-xl border border-cyan-500/30">
            <h3 className="text-xl text-cyan-400">Low-Light Enhancement</h3>
          </div>
          <div className="bg-gray-800/50 p-6 rounded-xl border border-blue-500/30">
            <h3 className="text-xl text-blue-400">YOLOv8 Detection</h3>
          </div>
          <div className="bg-gray-800/50 p-6 rounded-xl border border-purple-500/30">
            <h3 className="text-xl text-purple-400">AI Risk Analysis</h3>
          </div>
        </div>
        <motion.button 
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setView('dashboard')}
          className="mt-12 bg-cyan-600 hover:bg-cyan-500 text-white font-bold py-3 px-8 rounded-full shadow-[0_0_15px_rgba(6,182,212,0.6)] transition-all"
        >
          Enter Dashboard
        </motion.button>
      </motion.div>
    </div>
  )
}

function Main() {
  const [view, setView] = useState('landing');

  if (view === 'dashboard') return <Dashboard setView={setView} />
  return <Landing setView={setView} />
}

function App() {
  return (
    <Main />
  )
}

export default App
