import { api } from './api';
import { Course, TrainingContent } from '../types/content';

export const trainingService = {
  getCourses: async (level: string): Promise<Course[]> => {
    const response = await api.get(`/training/courses/${level}`);
    return response.data;
  },

  getCourseContent: async (courseId: string): Promise<TrainingContent[]> => {
    const response = await api.get(`/training/content/${courseId}`);
    return response.data;
  },

  markCourseComplete: async (courseId: string): Promise<void> => {
    await api.post(`/training/complete/${courseId}`);
  },

  getUserProgress: async (): Promise<any> => {
    const response = await api.get('/training/progress');
    return response.data;
  },
};