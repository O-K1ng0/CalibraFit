"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import MedicalHistoryStep from "@/components/OnboardingSteps/MedicalHistoryStep";
import {
  getFullProfile, updateProfile, updateMedicalHistory,
  generatePlan, isAuthenticated,
} from "@/lib/api";

const TABS = [
  { id: "demographics", label: "Demographics", icon: "📋" },
  { id: "medical", label: "Medical", icon: "🩺" },
  { id: "equipment", label: "Equipment", icon: "🏠" },
  { id: "schedule", label: "Schedule", icon: "📅" },
];

const EQUIPMENT_LIST = [
  "dumbbells", "barbell", "bench", "pull_up_bar", "resistance_bands",
  "kettlebell", "squat_rack", "cable_machine", "leg_press_machine",
  "leg_curl_machine", "ab_wheel", "jump_rope", "yoga_mat", "foam_roller",
];

const DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"];

export default function ProfilePage() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState("demographics");
  const [profileData, setProfileData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [editing, setEditing] = useState(false);
  const [planDuration, setPlanDuration] = useState(30);

  // Editable copies
  const [editProfile, setEditProfile] = useState({});
  const [editMedical, setEditMedical] = useState({});

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push("/");
      return;
    }
    loadProfile();
  }, [router]);

  const loadProfile = async () => {
    try {
      const data = await getFullProfile();
      setProfileData(data);
      if (data.profile) setEditProfile({ ...data.profile });
      if (data.medical_history) setEditMedical({ ...data.medical_history });
    } catch (err) {
      console.error("Failed to load profile:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    setSaved(false);
    try {
      await updateProfile(editProfile);
      if (editMedical && Object.keys(editMedical).length > 0) {
        await updateMedicalHistory(editMedical);
      }
      setEditing(false);
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
      await loadProfile();
    } catch (err) {
      console.error("Save error:", err);
    } finally {
      setSaving(false);
    }
  };

  const handleRegenerate = async () => {
    setSaving(true);
    try {
      await generatePlan({ duration_days: planDuration });
      router.push("/dashboard");
    } catch (err) {
      console.error("Plan generation error:", err);
    } finally {
      setSaving(false);
    }
  };

  const getBmiCategory = (bmi) => {
    if (!bmi) return null;
    const v = parseFloat(bmi);
    if (v < 18.5) return { label: "Underweight", color: "text-blue-400" };
    if (v < 25) return { label: "Normal", color: "text-success-400" };
    if (v < 30) return { label: "Overweight", color: "text-energy-400" };
    return { label: "Obese", color: "text-danger-400" };
  };

  if (loading) {
    return (
      <main className="flex-1 flex items-center justify-center">
        <div className="animate-spin w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full" />
      </main>
    );
  }

  const profile = profileData?.profile || {};
  const medical = profileData?.medical_history || {};
  const user = profileData?.user || {};
  const bmiCat = getBmiCategory(profile.bmi);

  return (
    <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-3xl mx-auto w-full">
      {/* Header */}
      <div className="mb-6 animate-fade-in-up">
        <Link href="/dashboard" className="text-sm text-slate-500 hover:text-slate-300 transition-colors mb-2 inline-block">
          ← Back to Dashboard
        </Link>
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white">Your Profile</h1>
            <p className="text-sm text-slate-400 mt-1">{user.email}</p>
          </div>
          <div className="flex items-center gap-2">
            {!editing ? (
              <button onClick={() => setEditing(true)} className="btn-secondary text-sm py-2 px-4">
                Edit
              </button>
            ) : (
              <>
                <button onClick={() => setEditing(false)} className="btn-secondary text-sm py-2 px-4">
                  Cancel
                </button>
                <button onClick={handleSave} disabled={saving} className="btn-primary text-sm py-2 px-4">
                  {saving ? "Saving..." : "Save"}
                </button>
              </>
            )}
          </div>
        </div>
        {saved && (
          <div className="mt-3 p-3 rounded-lg bg-success-500/10 border border-success-500/20 text-success-400 text-sm animate-fade-in">
            ✓ Profile saved successfully
          </div>
        )}
      </div>

      {/* Tabs */}
      <div className="flex gap-1 p-1 mb-6 rounded-xl bg-white/5 animate-fade-in-up delay-100">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex-1 py-2.5 text-xs sm:text-sm font-medium rounded-lg transition-all duration-200 ${activeTab === tab.id
              ? "bg-primary-600 text-white shadow-lg"
              : "text-slate-400 hover:text-white"
              }`}
          >
            <span className="mr-1">{tab.icon}</span> {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="glass-card p-6 animate-fade-in-up delay-200">
        {/* Demographics */}
        {activeTab === "demographics" && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-white mb-4">Personal Information</h2>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="input-label">Name</label>
                <p className="text-white font-medium">{user.full_name || "—"}</p>
              </div>
              <div>
                <label className="input-label" htmlFor="profileAge">Age</label>
                {editing ? (
                  <input id="profileAge" type="number" className="input-field" value={editProfile.age || ""}
                    onChange={(e) => setEditProfile({ ...editProfile, age: parseInt(e.target.value) || "" })} />
                ) : (
                  <p className="text-white font-medium">{profile.age || "—"}</p>
                )}
              </div>
              <div>
                <label className="input-label" htmlFor="profileHeight">Height</label>
                {editing ? (
                  <input id="profileHeight" type="number" className="input-field" value={editProfile.height_cm || ""}
                    onChange={(e) => setEditProfile({ ...editProfile, height_cm: parseFloat(e.target.value) || "" })} />
                ) : (
                  <p className="text-white font-medium">{profile.height_cm ? `${profile.height_cm} cm` : "—"}</p>
                )}
              </div>
              <div>
                <label className="input-label" htmlFor="profileWeight">Weight</label>
                {editing ? (
                  <input id="profileWeight" type="number" className="input-field" value={editProfile.weight_kg || ""}
                    onChange={(e) => setEditProfile({ ...editProfile, weight_kg: parseFloat(e.target.value) || "" })} />
                ) : (
                  <p className="text-white font-medium">{profile.weight_kg ? `${profile.weight_kg} kg` : "—"}</p>
                )}
              </div>
            </div>
            {profile.bmi && (
              <div className="glass-card p-4 mt-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-slate-400">BMI</span>
                  <div className="flex items-center gap-2">
                    <span className="text-xl font-bold text-white">{parseFloat(profile.bmi).toFixed(1)}</span>
                    {bmiCat && <span className={`text-xs ${bmiCat.color}`}>{bmiCat.label}</span>}
                  </div>
                </div>
              </div>
            )}
            <div>
              <label className="input-label">Fitness Experience</label>
              {editing ? (
                <select className="input-field" value={editProfile.fitness_experience || "beginner"}
                  onChange={(e) => setEditProfile({ ...editProfile, fitness_experience: e.target.value })}>
                  <option value="beginner">Beginner</option>
                  <option value="moderate">Moderate</option>
                  <option value="expert">Expert</option>
                </select>
              ) : (
                <p className="text-white font-medium capitalize">{profile.fitness_experience || "—"}</p>
              )}
            </div>
          </div>
        )}

        {/* Medical */}
        {activeTab === "medical" && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-white mb-4">Medical History</h2>
            {editing ? (
              <MedicalHistoryStep 
                data={editMedical} 
                onUpdate={(newData) => setEditMedical({ ...editMedical, ...newData })} 
                hideHeader={true}
              />
            ) : (
              <>
                <div className="glass-card p-3 flex items-center gap-3 text-xs text-slate-400 mb-4">
                  <span>🔒</span>
                  <p>Your medical data is stored securely and encrypted.</p>
                </div>
                <div>
                  <label className="input-label">Pain Areas</label>
                  <div className="flex flex-wrap gap-1.5">
                    {(medical.pain_areas || []).length > 0 ? medical.pain_areas.map((area) => (
                      <span key={area} className="chip selected">{area.replace(/_/g, " ")}</span>
                    )) : <p className="text-sm text-slate-500">None reported</p>}
                  </div>
                </div>
                <div>
                  <label className="input-label">Past Surgeries</label>
                  <div className="flex flex-wrap gap-1.5">
                    {(medical.past_surgeries || []).length > 0 ? medical.past_surgeries.map((s) => (
                      <span key={s} className="chip">{s}</span>
                    )) : <p className="text-sm text-slate-500">None reported</p>}
                  </div>
                </div>
                <div>
                  <label className="input-label">Chronic Conditions</label>
                  <div className="flex flex-wrap gap-1.5">
                    {(medical.chronic_diseases || []).length > 0 ? medical.chronic_diseases.map((d) => (
                      <span key={d} className="chip">{d}</span>
                    )) : <p className="text-sm text-slate-500">None reported</p>}
                  </div>
                </div>
                <div>
                  <label className="input-label">Active Safety Filters</label>
                  <div className="flex flex-wrap gap-1.5">
                    {(medical.contraindication_flags || []).length > 0 ? medical.contraindication_flags.map((f) => (
                      <span key={f} className="px-2 py-1 rounded-full bg-danger-500/15 text-danger-400 text-xs font-medium">
                        {f.replace(/_/g, " ")}
                      </span>
                    )) : <p className="text-sm text-slate-500">No active filters</p>}
                  </div>
                </div>
                {medical.notes && (
                  <div>
                    <label className="input-label">Additional Notes</label>
                    <div className="glass-card p-3">
                      <p className="text-sm text-slate-300">{medical.notes}</p>
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        )}

        {/* Equipment */}
        {activeTab === "equipment" && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-white mb-4">Equipment & Environment</h2>
            <div>
              <label className="input-label">Training Environment</label>
              {editing ? (
                <div className="grid grid-cols-2 gap-3">
                  {["home", "gym"].map((env) => (
                    <button key={env} type="button"
                      onClick={() => setEditProfile({ ...editProfile, training_environment: env })}
                      className={`p-4 rounded-xl border text-center transition-all ${editProfile.training_environment === env
                        ? "bg-primary-600/20 border-primary-500/40" : "bg-white/5 border-white/10"
                        }`}>
                      <span className="text-2xl block mb-1">{env === "home" ? "🏠" : "🏢"}</span>
                      <span className="capitalize text-sm text-white">{env}</span>
                    </button>
                  ))}
                </div>
              ) : (
                <p className="text-white font-medium capitalize">{profile.training_environment || "—"}</p>
              )}
            </div>
            <div>
              <label className="input-label">Available Equipment</label>
              <div className="grid grid-cols-2 gap-2">
                {EQUIPMENT_LIST.map((eq) => {
                  const has = (editing ? editProfile : profile).available_equipment?.includes(eq);
                  return (
                    <button key={eq} type="button" disabled={!editing}
                      onClick={() => {
                        if (!editing) return;
                        const current = editProfile.available_equipment || [];
                        setEditProfile({
                          ...editProfile,
                          available_equipment: has ? current.filter(e => e !== eq) : [...current, eq]
                        });
                      }}
                      className={`flex items-center gap-2 p-3 rounded-xl border text-sm transition-all ${has ? "bg-primary-600/15 border-primary-500/30 text-white" : "bg-white/5 border-white/10 text-slate-500"
                        } ${editing ? "cursor-pointer hover:bg-white/8" : "cursor-default"}`}>
                      {has && <span className="text-primary-400">✓</span>}
                      <span className="capitalize">{eq.replace(/_/g, " ")}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          </div>
        )}

        {/* Schedule */}
        {activeTab === "schedule" && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-white mb-4">Workout Schedule</h2>
            <div>
              <label className="input-label" htmlFor="profileWeeklyFreq">Weekly Frequency</label>
              {editing ? (
                <div className="flex items-center gap-4">
                  <input id="profileWeeklyFreq" type="range" min={1} max={7}
                    value={editProfile.weekly_frequency || 3}
                    onChange={(e) => setEditProfile({ ...editProfile, weekly_frequency: parseInt(e.target.value) })}
                    className="flex-1" />
                  <span className="text-2xl font-bold text-primary-400">{editProfile.weekly_frequency || 3}</span>
                </div>
              ) : (
                <p className="text-white font-medium">{profile.weekly_frequency || 3}x per week</p>
              )}
            </div>
            <div>
              <label className="input-label">Preferred Days</label>
              <div className="grid grid-cols-7 gap-2">
                {DAYS.map((day) => {
                  const selected = (editing ? editProfile : profile).preferred_workout_days?.includes(day);
                  return (
                    <button key={day} type="button" disabled={!editing}
                      onClick={() => {
                        if (!editing) return;
                        const current = editProfile.preferred_workout_days || [];
                        setEditProfile({
                          ...editProfile,
                          preferred_workout_days: selected ? current.filter(d => d !== day) : [...current, day]
                        });
                      }}
                      className={`py-3 rounded-xl text-center text-xs font-medium transition-all ${selected ? "bg-primary-600 text-white" : "bg-white/5 text-slate-500 border border-white/10"
                        } ${editing ? "cursor-pointer" : "cursor-default"}`}>
                      {day.slice(0, 3)}
                    </button>
                  );
                })}
              </div>
            </div>
            <div>
              <label className="input-label">Preferred Time</label>
              <p className="text-white font-medium capitalize">{profile.preferred_time || "morning"}</p>
            </div>
          </div>
        )}
      </div>

      {/* Regenerate Plan */}
      {!editing && (
        <div className="mt-6 glass-card p-4 animate-fade-in">
          <p className="text-sm text-slate-400 mb-3">
            Want to refresh your routine or apply recent profile changes?
          </p>
          <div className="flex gap-3 items-center">
            <select
              className="input-field flex-shrink-0"
              style={{ width: "auto", minWidth: "140px" }}
              value={planDuration}
              onChange={(e) => setPlanDuration(parseInt(e.target.value))}
            >
              <option value={30}>30-Day Plan</option>
              <option value={60}>60-Day Plan</option>
              <option value={90}>90-Day Plan</option>
            </select>
            <button onClick={handleRegenerate} disabled={saving} className="btn-primary flex-1">
              {saving ? "Generating..." : "Regenerate Plan 🔄"}
            </button>
          </div>
        </div>
      )}
    </main>
  );
}
