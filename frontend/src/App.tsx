import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { UserProvider } from './context/UserContext';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Home from './pages/Home';
import ExamPage from './pages/ExamPage';
import TrainingPage from './pages/TrainingPage';
import ChatbotPage from './pages/ChatbotPage';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <UserProvider>
        <Router>
          <div className="App">
            <Navbar />
            <main className="main-content">
              <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/" element={<Home />} />
                <Route path="/exam" element={<ExamPage />} />
                <Route path="/training" element={<TrainingPage />} />
                <Route path="/chatbot" element={<ChatbotPage />} />
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </main>
          </div>
        </Router>
      </UserProvider>
    </AuthProvider>
  );
}

export default App;