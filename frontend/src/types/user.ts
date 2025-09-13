export interface User {
  id: string;
  name: string;
  email: string;
  classification: 'beginner' | 'intermediate' | 'advanced';
  exam_score?: number;
  completed_courses: string[];
  current_course?: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface UserCreate {
  name: string;
  email: string;
  password: string;
}

export interface Token {
  access_token: string;
  token_type: string;
  user: User;
}