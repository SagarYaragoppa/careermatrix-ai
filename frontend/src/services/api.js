const API_URL = "http://127.0.0.1:8000";

export const apiRequest = async (endpoint, method = "GET", body = null) => {

  const token = localStorage.getItem("token");

  const response = await fetch(`${API_URL}${endpoint}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` })
    },
    body: body ? JSON.stringify(body) : null
  });

  if (!response.ok) {
    throw new Error("API Error");
  }

  return response.json();
};
