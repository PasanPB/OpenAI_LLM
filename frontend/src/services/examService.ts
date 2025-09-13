import { api } from './api';
import { ExamQuestion, ExamSubmission, ExamResult } from '../types/exam';

export const examService = {
  getQuestions: async (): Promise<ExamQuestion[]> => {
    const response = await api.get('/exam/questions');
    return response.data;
  },

  submitExam: async (submission: ExamSubmission): Promise<ExamResult> => {
    const response = await api.post('/exam/submit', submission);
    return response.data;
  },

  getExamResults: async (): Promise<ExamResult[]> => {
    const response = await api.get('/exam/results');
    return response.data;
  },
};