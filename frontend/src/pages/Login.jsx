import { useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { motion } from 'framer-motion';
import axios from 'axios';

export default function Login({ setView }) {
  const { login } = useContext(AuthContext);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);
      
      const res = await axios.post('http://127.0.0.1:8000/auth/login', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });
      login(res.data.access_token, res.data.username);
      setView('dashboard');
    } catch (err) {
      alert('Login failed. Check credentials.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} className="glass-card p-8 rounded-xl w-full max-w-md">
        <h2 className="text-3xl font-bold mb-6 text-center neon-text">Access System</h2>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input 
            type="email" 
            placeholder="Operator Email" 
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="bg-gray-800/50 border border-gray-600 rounded p-3 text-white focus:outline-none focus:border-cyan-500 transition-colors"
            required 
          />
          <input 
            type="password" 
            placeholder="Security Key" 
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="bg-gray-800/50 border border-gray-600 rounded p-3 text-white focus:outline-none focus:border-cyan-500 transition-colors"
            required 
          />
          <button type="submit" className="bg-cyan-600 hover:bg-cyan-500 text-white font-bold py-3 rounded mt-4 transition-all shadow-[0_0_10px_rgba(6,182,212,0.4)]">
            Initialize Session
          </button>
        </form>
        <p className="text-center mt-4 text-sm text-gray-400">
          New operator? <span className="text-cyan-400 cursor-pointer hover:underline" onClick={() => setView('register')}>Register Credentials</span>
        </p>
      </motion.div>
    </div>
  );
}
