export interface StudyWord {
  id: number;
  simplified: string;
  pinyin: string;
  meaning: string;
}

export interface StudyWordsResponse {
  count: number;
  page: number;
  page_size: number;
  total_pages: number;
  next_page: number | null;
  previous_page: number | null;
  results: StudyWord[];
}