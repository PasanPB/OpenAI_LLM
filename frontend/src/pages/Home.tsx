import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { trainingService } from '../services/trainingService';
import './Home.css';

const Home: React.FC = () => {
  const { user } = useAuth();
  const [progress, setProgress] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchProgress = async () => {
      if (user) {
        try {
          const progressData = await trainingService.getUserProgress();
          setProgress(progressData);
        } catch (error) {
          console.error('Failed to fetch progress:', error);
        } finally {
          setIsLoading(false);
        }
      }
    };

    fetchProgress();
  }, [user]);

  if (!user) {
    return <div>Please log in to view your dashboard.</div>;
  }

  return (
    <div className="home-page">
      <div className="welcome-section">
        <h1>Welcome back, {user.name}!</h1>
        <p>Your current awareness level: <span className={`level-badge ${user.classification}`}>{user.classification}</span></p>
      </div>

      {isLoading ? (
        <div className="loading">Loading your progress...</div>
      ) : progress && (
        <div className="progress-section">
          <h2>Your Learning Progress</h2>
          <div className="progress-cards">
            <div className="progress-card">
              <h3>Courses Completed</h3>
              <div className="progress-number">{progress.completed_courses}</div>
              <p>out of {progress.total_courses} total courses</p>
            </div>
            <div className="progress-card">
              <h3>Overall Progress</h3>
              <div className="progress-number">{Math.round(progress.progress_percentage)}%</div>
              <div className="progress-bar">
                <div 
                  className="progress-fill" 
                  style={{ width: `${progress.progress_percentage}%` }}
                ></div>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="quick-actions">
        <h2>Quick Actions</h2>
        <div className="action-cards">
          <Link to="/exam" className="action-card">
            <div className="action-icon">📝</div>
            <h3>Take Assessment</h3>
            <p>Test your phishing awareness knowledge</p>
          </Link>
          <Link to="/training" className="action-card">
            <div className="action-icon">📚</div>
            <h3>View Courses</h3>
            <p>Browse available training materials</p>
          </Link>
          <Link to="/chatbot" className="action-card">
            <div className="action-icon">🤖</div>
            <h3>AI Assistant</h3>
            <p>Get help with phishing questions</p>
          </Link>
        </div>
      </div>

      <div className="recent-activity">
        <h2>Recommended Next Steps</h2>
        <div className="activity-list">
          <div className="activity-item">
            <span className="activity-icon">🎯</span>
            <div className="activity-content">
              <h4>Complete your current course</h4>
              <p>Continue your learning journey</p>
            </div>
          </div>
          <div className="activity-item">
            <span className="activity-icon">🔄</span>
            <div className="activity-content">
              <h4>Review phishing examples</h4>
              <p>Stay updated with latest threats</p>
            </div>
          </div>
          <div className="activity-item">
            <span className="activity-icon">📊</span>
            <div className="activity-content">
              <h4>Check your progress</h4>
              <p>Track your learning achievements</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;