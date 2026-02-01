const STORAGE_KEY = 'pending_surveys';

export const loadPendingSurveys = () => {
  const data = localStorage.getItem(STORAGE_KEY);
  return data ? JSON.parse(data) : [];
};

export const savePendingSurveys = (surveys) => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(surveys));
};

export const addPendingSurvey = (survey) => {
  const surveys = loadPendingSurveys();
  surveys.push({
    id: crypto.randomUUID(),
    ...survey,
    timestamp: Date.now()
  });
  savePendingSurveys(surveys);
};

export const clearPendingSurveys = () => {
  localStorage.removeItem(STORAGE_KEY);
};

export const removePendingSurvey = (id) => {
  const surveys = loadPendingSurveys().filter(s => s.id !== id);
  savePendingSurveys(surveys);
};