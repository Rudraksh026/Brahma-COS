import axios from "axios";
const baseURL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
const api = axios.create({ baseURL, headers: { "Content-Type": "application/json" }, timeout: 120000 });
export default api;
