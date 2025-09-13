import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { trainingService } from '../services/trainingService';
import { Course } from '../types/content';
import CourseCard from '../components/CourseCard';
import './TrainingPage.css';

const TrainingPage: React.FC = () => {
  const { user } = useAuth();
  const [courses, setCourses] = useState<Course[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedLevel, setSelectedLevel] = useState('all');

  useEffect(() => {
    const fetchCourses = async () => {
      if (!user) return;

      try {
        setIsLoading(true);
        let courseData: Course[] = [];
        
        if (selectedLevel === 'all') {
          // Fetch courses for all levels
          const [beginner, intermediate, advanced] = await Promise.all([
            trainingService.getCourses('beginner'),
            trainingService.getCourses('intermediate'),
            trainingService.getCourses('advanced')
          ]);
          courseData = [...beginner, ...intermediate, ...advanced];
        } else {
          courseData = await trainingService.getCourses(selectedLevel);
        }
        
        setCourses(courseData);
      } catch (err) {
        setError('Failed to load courses');
        console.error('Error fetching courses:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchCourses();
  }, [user, selectedLevel]);

  const handleStartCourse = (courseId: string) => {
    // Navigate to course content page or open course modal
    alert(`Starting course: ${courseId}`);
    // In a real implementation, you would navigate to the course content page
  };

  if (!user) {
    return <div>Please log in to view training materials.</div>;
  }

  const filteredCourses = selectedLevel === 'all' 
    ? courses 
    : courses.filter(course => course.difficulty === selectedLevel);

  return (
    <div className="training-page">
      <div className="training-header">
        <h1>Phishing Awareness Training</h1>
        <p>Your current level: <span className={`level-badge ${user.classification}`}>{user.classification}</span></p>
      </div>

      <div className="filters">
        <label htmlFor="level-filter">Filter by level:</label>
        <select 
          id="level-filter"
          value={selectedLevel}
          onChange={(e) => setSelectedLevel(e.target.value)}
          className="filter-select"
        >
          <option value="all">All Levels</option>
          <option value="beginner">Beginner</option>
          <option value="intermediate">Intermediate</option>
          <option value="advanced">Advanced</option>
        </select>
      </div>

      {isLoading ? (
        <div className="loading">Loading courses...</div>
      ) : error ? (
        <div className="error">{error}</div>
      ) : (
        <>
          <div className="courses-section">
            <h2>Available Courses</h2>
            <div className="courses-grid">
              {filteredCourses.map(course => (
                <CourseCard
                  key={course.id}
                  course={course}
                  onStartCourse={handleStartCourse}
                  isCompleted={user.completed_courses.includes(course.id)}
                />
              ))}
            </div>
          </div>

          {filteredCourses.length === 0 && (
            <div className="no-courses">
              <h3>No courses available</h3>
              <p>There are no courses matching your selected filter.</p>
            </div>
          )}
        </>
      )}

      <div className="progress-section">
        <h2>Your Progress</h2>
        <div className="progress-stats">
          <div className="stat">
            <span className="stat-number">
              {user.completed_courses.length}
            </span>
            <span className="stat-label">Courses Completed</span>
          </div>
          <div className="stat">
            <span className="stat-number">
              {courses.filter(c => user.completed_courses.includes(c.id)).length}
            </span>
            <span className="stat-label">In Progress</span>
          </div>
          <div className="stat">
            <span className="stat-number">{courses.length}</span>
            <span className="stat-label">Total Courses</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TrainingPage;