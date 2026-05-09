import { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import axios from 'axios';

export default function Dashboard({ setView }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  // Chatbot State
  const [chatInput, setChatInput] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [chatLoading, setChatLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory]);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post('http://127.0.0.1:8000/detect/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResult(res.data);
    } catch (err) {
      alert('Upload failed');
    }
    setLoading(false);
  };

  const handleChat = async (e) => {
    e.preventDefault();
    if (!chatInput.trim()) return;
    
    const userMessage = chatInput;
    setChatInput('');
    setChatHistory(prev => [...prev, { role: 'user', content: userMessage }]);
    setChatLoading(true);

    try {
      const res = await axios.post('http://127.0.0.1:8000/chat/', { message: userMessage });
      setChatHistory(prev => [...prev, { role: 'ai', content: res.data.response }]);
    } catch (err) {
      setChatHistory(prev => [...prev, { role: 'ai', content: 'Error communicating with AI.' }]);
    }
    setChatLoading(false);
  };

  return (
    <div className="min-h-screen p-8">
      <div className="flex justify-between items-center mb-8 glass-card p-4 rounded-xl">
        <h1 className="text-2xl font-bold neon-text">NightVision AI Dashboard</h1>
        <div className="flex items-center gap-4">
          <button onClick={() => setView('landing')} className="bg-red-500/20 hover:bg-red-500/40 text-red-400 px-4 py-2 rounded transition-colors">Go Back</button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Upload & Images */}
        <div className="lg:col-span-2 space-y-8">
          <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-6 rounded-xl">
            <h2 className="text-xl font-bold mb-4 text-cyan-400">Feed Upload</h2>
            <div className="border-2 border-dashed border-gray-600 rounded-xl p-8 text-center hover:border-cyan-500 transition-colors">
              <input type="file" onChange={(e) => setFile(e.target.files[0])} className="mb-4 text-gray-300" />
              <button 
                onClick={handleUpload} 
                disabled={loading}
                className="w-full bg-cyan-600 hover:bg-cyan-500 disabled:bg-gray-600 text-white font-bold py-3 rounded shadow-[0_0_10px_rgba(6,182,212,0.4)] transition-all"
              >
                {loading ? 'Processing Feed...' : 'Analyze Night Feed'}
              </button>
            </div>
          </motion.div>

          {result && (
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-6 rounded-xl space-y-6">
              <div className="flex justify-between items-center">
                <h2 className="text-xl font-bold text-purple-400">AI Risk Assessment</h2>
                <a 
                  href={`http://127.0.0.1:8000/detect/report/${result.upload_id}`} 
                  target="_blank" 
                  rel="noreferrer"
                  className="bg-purple-600 hover:bg-purple-500 text-white px-4 py-2 rounded font-bold shadow-[0_0_10px_rgba(139,92,246,0.4)] transition-all"
                >
                  Download PDF Report
                </a>
              </div>
              
              <div className="flex items-center gap-4">
                <span className={`px-4 py-2 rounded text-lg font-bold ${result.risk_level === 'HIGH' ? 'bg-red-500/20 text-red-400 border border-red-500' : 'bg-green-500/20 text-green-400 border border-green-500'}`}>
                  {result.risk_level} RISK
                </span>
              </div>
              <p className="text-gray-300 text-lg">{result.explanation}</p>
              
              <div className="bg-gray-800/50 p-4 rounded-lg">
                <h3 className="text-sm text-gray-400 mb-2">Detected Objects:</h3>
                <ul className="list-disc list-inside">
                  {result.detected_objects.map((obj, i) => (
                    <li key={i} className="text-cyan-300 font-mono">{obj.class} - {obj.confidence}%</li>
                  ))}
                </ul>
              </div>

              {/* Image Display */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
                <div className="border border-gray-600 rounded p-2">
                  <h3 className="text-center text-gray-400 mb-2">Enhanced Night Vision</h3>
                  <img src={result.enhanced_image_url} alt="Enhanced" className="w-full h-auto rounded" />
                </div>
                <div className="border border-cyan-500/50 rounded p-2 shadow-[0_0_15px_rgba(6,182,212,0.2)]">
                  <h3 className="text-center text-cyan-400 mb-2">YOLOv8 Detection</h3>
                  <img src={result.result_image_url} alt="Result" className="w-full h-auto rounded" />
                </div>
              </div>
            </motion.div>
          )}
        </div>

        {/* Right Column: AI Chatbot */}
        <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} className="glass-card flex flex-col rounded-xl overflow-hidden h-[800px]">
          <div className="bg-gray-800/80 p-4 border-b border-gray-700">
            <h2 className="text-xl font-bold text-blue-400">Guardian AI Assistant</h2>
          </div>
          
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {chatHistory.length === 0 && (
              <p className="text-gray-500 text-center mt-4">Ask me anything about the surveillance feed or risk protocols.</p>
            )}
            {chatHistory.map((msg, i) => (
              <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[80%] p-3 rounded-xl ${msg.role === 'user' ? 'bg-blue-600 text-white rounded-tr-none' : 'bg-gray-700 text-gray-200 rounded-tl-none'}`}>
                  {msg.content}
                </div>
              </div>
            ))}
            {chatLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-700 text-gray-400 p-3 rounded-xl rounded-tl-none animate-pulse">
                  AI is analyzing...
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form onSubmit={handleChat} className="p-4 bg-gray-800/80 border-t border-gray-700 flex gap-2">
            <input 
              type="text" 
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              placeholder="Ask Guardian AI..." 
              className="flex-1 bg-gray-900 border border-gray-600 rounded p-2 text-white focus:outline-none focus:border-blue-500"
            />
            <button 
              type="submit" 
              disabled={chatLoading}
              className="bg-blue-600 hover:bg-blue-500 disabled:bg-gray-600 text-white px-4 py-2 rounded font-bold transition-colors"
            >
              Send
            </button>
          </form>
        </motion.div>
      </div>
    </div>
  );
}
