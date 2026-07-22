/**
 * CalibraFit — API Client
 * Centralized API functions for communicating with the FastAPI backend.
 */

import axios from "axios";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE,
  headers: { "Content-Type": "application/json" },
});

// ─── Request Interceptor: Attach JWT Token ──────────────────
api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("calibrafit_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// ─── Response Interceptor: Handle Auth Errors ───────────────
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      if (typeof window !== "undefined") {
        localStorage.removeItem("calibrafit_token");
        // Don't redirect if already on login/onboarding
        const path = window.location.pathname;
        if (path !== "/" && !path.startsWith("/onboarding")) {
          window.location.href = "/";
        }
      }
    }
    return Promise.reject(error);
  }
);

// ─── Auth ───────────────────────────────────────────────────

export async function register(email, password, fullName) {
  const res = await api.post("/api/auth/register", {
    email,
    password,
    full_name: fullName,
  });
  return res.data;
}

export async function login(email, password) {
  const res = await api.post("/api/auth/login", { email, password });
  if (res.data.access_token) {
    localStorage.setItem("calibrafit_token", res.data.access_token);
  }
  return res.data;
}

export async function getMe() {
  const res = await api.get("/api/auth/me");
  return res.data;
}

export function logout() {
  localStorage.removeItem("calibrafit_token");
  window.location.href = "/";
}

export function isAuthenticated() {
  if (typeof window === "undefined") return false;
  return !!localStorage.getItem("calibrafit_token");
}

// ─── User Profile ───────────────────────────────────────────

export async function createProfile(profileData) {
  const res = await api.post("/api/user/profile", profileData);
  return res.data;
}

export async function getProfile() {
  const res = await api.get("/api/user/profile");
  return res.data;
}

export async function updateProfile(profileData) {
  const res = await api.put("/api/user/profile", profileData);
  return res.data;
}

// ─── Medical History ────────────────────────────────────────

export async function saveMedicalHistory(medicalData) {
  const res = await api.post("/api/user/medical-history", medicalData);
  return res.data;
}

export async function getMedicalHistory() {
  const res = await api.get("/api/user/medical-history");
  return res.data;
}

export async function updateMedicalHistory(medicalData) {
  const res = await api.put("/api/user/medical-history", medicalData);
  return res.data;
}

// ─── Full Profile ───────────────────────────────────────────

export async function getFullProfile() {
  const res = await api.get("/api/user/full-profile");
  return res.data;
}

// ─── Workout Plans ──────────────────────────────────────────

export async function generatePlan(options = {}) {
  const res = await api.post("/api/workout/generate-plan", options);
  return res.data;
}

export async function getCurrentPlan() {
  const res = await api.get("/api/workout/plan");
  return res.data;
}

export async function getPlanSummary() {
  const res = await api.get("/api/workout/plan/summary");
  return res.data;
}

// ─── Daily Workouts ─────────────────────────────────────────

export async function getDailyWorkout(dateStr) {
  const res = await api.get(`/api/workout/daily/${dateStr}`);
  return res.data;
}

// ─── Workout Completion ─────────────────────────────────────

export async function completeWorkout(completionData) {
  const res = await api.post("/api/workout/complete", completionData);
  return res.data;
}

// ─── Progress ───────────────────────────────────────────────

export async function getProgress() {
  const res = await api.get("/api/workout/progress");
  return res.data;
}

// ─── Weekly Feedback ────────────────────────────────────────

export async function submitFeedback(feedbackData) {
  const res = await api.post("/api/workout/feedback", feedbackData);
  return res.data;
}

export async function getFeedbacks() {
  const res = await api.get("/api/workout/feedback");
  return res.data;
}

export async function adaptiveRegenerate(options = {}) {
  const res = await api.post("/api/workout/adaptive-regenerate", options);
  return res.data;
}

export default api;
