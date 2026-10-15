
export type QuizType =
  | 'hanzi_to_meaning'
  | 'meaning_to_hanzi'
  | 'hanzi_to_pinyin'
  | 'pinyin_to_hanzi';

export interface QuizQuestion {
  id: string;
  quiz_type: QuizType;
  vocabulary_id: number;
  prompt: string;
  options: string[];
}

export interface QuizQuestionsResponse {
  questions: QuizQuestion[];
}

export interface QuizAnswer {
  question_id: string;
  answer: string;
}

export interface QuizBatchSubmission {
  answers: QuizAnswer[];
}

export interface QuizAnswerResult {
  question_id: string;
  correct: boolean;
  correct_answer: string;
}

export interface QuizBatchAnswerResponse {
  total_questions: number;
  correct_count: number;
  score_percentage: number;
  results: QuizAnswerResult[];
}
