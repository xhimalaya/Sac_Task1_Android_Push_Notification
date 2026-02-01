const API_BASE = 'https://whale-stunning-brightly.ngrok-free.app';
const ENDPOINT = `${API_BASE}/api/survey/`;

export const checkApiReachable = async () => {
  try {
    const res = await fetch(ENDPOINT, { method: 'HEAD', signal: AbortSignal.timeout(5000) });
    return res.ok || res.status === 405;
  } catch (e) {
    return false;
  }
};

export const submitSingle = async (data, imageFile) => {
  const formData = new FormData();
  formData.append('client_id', data.client_id || crypto.randomUUID());
  formData.append('name', data.name);
  formData.append('age', data.age);
  formData.append('location', JSON.stringify(data.location));

  if (imageFile) formData.append('image', imageFile);

  const res = await fetch(ENDPOINT, {
    method: 'POST',
    body: formData
  });

  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
};

export const submitBulk = async (pendingSurveys) => {
  const formData = new FormData();

  for (const survey of pendingSurveys) {
    const file = base64ToFile(survey.imageBase64, `survey_${survey.id}.jpg`);

    formData.append('client_id', survey.client_id || survey.id);
    formData.append('name', survey.name);
    formData.append('age', survey.age);
    formData.append('location', JSON.stringify(survey.location));
    formData.append('image', file);
  }

  const res = await fetch(ENDPOINT, {
    method: 'POST',
    body: formData
  });

  if (!res.ok) throw new Error(`Bulk failed: ${res.status}`);
  return res.json();
};

function base64ToFile(base64, filename) {
  const arr = base64.split(',');
  const mime = arr[0].match(/:(.*?);/)[1];
  const bstr = atob(arr[1]);
  let n = bstr.length;
  const u8arr = new Uint8Array(n);
  while (n--) u8arr[n] = bstr.charCodeAt(n);
  return new File([u8arr], filename, { type: mime });
}