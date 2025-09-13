import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { examService } from '../services/examService';
import { ExamQuestion, ExamSubmission } from '../types/exam';
import './ExamPage.css';

const ExamPage: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [questions, setQuestions] = useState<ExamQuestion[]>([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState<number[]>([]);
  const [timeStarted, setTimeStarted] = useState<Date | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const loadQuestions = async () => {
      try {
        const examQuestions = await examService.getQuestions();
        setQuestions(examQuestions);
        setAnswers(new Array(examQuestions.length).fill(-1));
        setTimeStarted(new Date());
      } catch (err) {
        setError('Failed to load exam questions');
        console.error('Error loading questions:', err);
      }
    };

    loadQuestions();
  }, []);

  const handleAnswerSelect = (answerIndex: number) => {
    const newAnswers = [...answers];
    newAnswers[currentQuestion] = answerIndex;
    setAnswers(newAnswers);
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const handleSubmit = async () => {
    if (answers.includes(-1)) {
      if (!window.confirm('You have unanswered questions. Are you sure you want to submit?')) {
        return;
      }
    }

    setIsSubmitting(true);
    try {
      const timeTaken = timeStarted ? Math.floor((new Date().getTime() - timeStarted.getTime()) / 1000) : 0;
      const submission: ExamSubmission = {
        user_id: user?.id || '',
        answers: answers.map(ans => ans === -1 ? 0 : ans),
        time_taken: timeTaken
      };

      const result = await examService.submitExam(submission);
      alert(`Exam submitted! Your score: ${result.score}%\nClassification: ${result.classification}`);
      navigate('/');
    } catch (err) {
      setError('Failed to submit exam');
      console.error('Error submitting exam:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!user) {
    return <div>Please log in to take the exam.</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (questions.length === 0) {
    return <div className="loading">Loading exam questions...</div>;
  }

  const currentQ = questions[currentQuestion];
  const progress = ((currentQuestion + 1) / questions.length) * 100;

  return (
    <div className="exam-page">
      <div className="exam-header">
        <h1>Phishing Awareness Assessment</h1>
        <div className="exam-progress">
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <span>Question {currentQuestion + 1} of {questions.length}</span>
        </div>
      </div>

      <div className="question-card">
        <h2 className="question-text">{currentQ.question}</h2>
        
        <div className="options-list">
          {currentQ.options.map((option, index) => (
            <label key={index} className="option-label">
              <input
                type="radio"
                name="answer"
                value={index}
                checked={answers[currentQuestion] === index}
                onChange={() => handleAnswerSelect(index)}
                className="option-input"
              />
              <span className="option-text">{option}</span>
            </label>
          ))}
        </div>

        <div className="navigation-buttons">
          <button 
            onClick={handlePrevious}
            disabled={currentQuestion === 0}
            className="nav-btn previous"
          >
            Previous
          </button>
          
          {currentQuestion === questions.length - 1 ? (
            <button 
              onClick={handleSubmit}
              disabled={isSubmitting}
              className="nav-btn submit"
            >
              {isSubmitting ? 'Submitting...' : 'Submit Exam'}
            </button>
          ) : (
            <button 
              onClick={handleNext}
              className="nav-btn next"
            >
              Next
            </button>
          )}
        </div>
      </div>

      <div className="question-indicators">
        {questions.map((_, index) => (
          <button
            key={index}
            onClick={() => setCurrentQuestion(index)}
            className={`indicator ${answers[index] !== -1 ? 'answered' : ''} ${currentQuestion === index ? 'current' : ''}`}
          >
            {index + 1}
          </button>
        ))}
      </div>
    </div>
  );
};

export default ExamPage;