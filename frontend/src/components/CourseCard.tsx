import React from 'react';
import { Course } from '../types/content';
import './CourseCard.css';

interface CourseCardProps {
  course: Course;
  onStartCourse: (courseId: string) => void;
  isCompleted?: boolean;
}

const CourseCard: React.FC<CourseCardProps> = ({ course, onStartCourse, isCompleted = false }) => {
  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return '#10b981';
      case 'intermediate': return '#f59e0b';
      case 'advanced': return '#ef4444';
      default: return '#6b7280';
    }
  };

  const getContentTypeIcon = (type: string) => {
    switch (type) {
      case 'video': return '🎬';
      case 'interactive': return '🔄';
      case 'scenario': return '🎯';
      case 'quiz': return '📝';
      default: return '📚';
    }
  };

  return (
    <div className={`course-card ${isCompleted ? 'completed' : ''}`}>
      <div className="course-header">
        <span 
          className="difficulty-badge"
          style={{ backgroundColor: getDifficultyColor(course.difficulty) }}
        >
          {course.difficulty}
        </span>
        <span className="content-type">
          {getContentTypeIcon(course.content_type)} {course.content_type}
        </span>
      </div>
      
      <h3 className="course-title">{course.title}</h3>
      <p className="course-description">{course.description}</p>
      
      <div className="course-details">
        <span className="duration">⏱️ {course.duration} min</span>
        <span className="modules">📦 {course.modules.length} modules</span>
      </div>
      
      {course.prerequisites.length > 0 && (
        <div className="prerequisites">
          <strong>Prerequisites:</strong> {course.prerequisites.join(', ')}
        </div>
      )}
      
      <button 
        onClick={() => onStartCourse(course.id)}
        className={`start-btn ${isCompleted ? 'completed' : ''}`}
        disabled={isCompleted}
      >
        {isCompleted ? 'Completed ✓' : 'Start Course'}
      </button>
    </div>
  );
};

export default CourseCard;