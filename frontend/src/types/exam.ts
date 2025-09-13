export interface ExamQuestion {
  id: string;
  question: string;
  options: string[];
  correct_answer: number;
  explanation: string;
}

export interface ExamSubmission {
  user_id: string;
  answers: number[];
  time_taken: number;
}

export interface ExamResult {
  user_id: string;
  score: number;
  total_questions: number;
  correct_answers: number;
  classification: 'beginner' | 'intermediate' | 'advanced';
  submitted_at: string;
}