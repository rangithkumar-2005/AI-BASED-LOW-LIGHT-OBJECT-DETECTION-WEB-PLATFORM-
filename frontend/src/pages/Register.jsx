import { useState } from 'react';
import { motion } from 'framer-motion';
import axios from 'axios';

export default function Register({ setView }) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      alert('Passwords do not match!');
      return;
    }
    
    try {
      await axios.post('http://127.0.0.1:8000/auth/register', {
        username: username,
        email: email,
        password: password
      });
      alert('Registration successful! Please login.');
      setView('login');
    } catch (err) {
      alert(err.response?.data?.detail || 'Registration failed.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} className="glass-card p-8 rounded-xl w-full max-w-md">
        <h2 className="text-3xl font-bold mb-6 text-center neon-text">New Operator</h2>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input 
            type="text" 
            placeholder="Operator Name" 
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="bg-gray-800/50 border border-gray-600 rounded p-3 text-white focus:outline-none focus:border-purple-500 transition-colors"
            required 
          />
          <input 
            type="email" 
            placeholder="Operator Email" 
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="bg-gray-800/50 border border-gray-600 rounded p-3 text-white focus:outline-none focus:border-purple-500 transition-colors"
            required 
          />
          <input 
            type="password" 
            placeholder="Security Key" 
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="bg-gray-800/50 border border-gray-600 rounded p-3 text-white focus:outline-none focus:border-purple-500 transition-colors"
            required 
          />
          <input 
            type="password" 
            placeholder="Confirm Security Key" 
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            className="bg-gray-800/50 border border-gray-600 rounded p-3 text-white focus:outline-none focus:border-purple-500 transition-colors"
            required 
          />
          <button type="submit" className="bg-purple-600 hover:bg-purple-500 text-white font-bold py-3 rounded mt-4 transition-all shadow-[0_0_10px_rgba(139,92,246,0.4)]">
            Register Credentials
          </button>
        </form>
        <p className="text-center mt-4 text-sm text-gray-400">
          Already an operator? <span className="text-purple-400 cursor-pointer hover:underline" onClick={() => setView('login')}>Initialize Session</span>
        </p>
      </motion.div>
    </div>
  );
}
