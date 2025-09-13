export interface Course {
  id: string;
  title: string;
  description: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  content_type: 'video' | 'interactive' | 'scenario' | 'quiz';
  duration: number;
  modules: string[];
  prerequisites: string[];
}

export interface TrainingContent {
  id: string;
  course_id: string;
  title: string;
  content: string;
  content_type: 'video' | 'interactive' | 'scenario' | 'quiz';
  order: number;
  duration: number;
}