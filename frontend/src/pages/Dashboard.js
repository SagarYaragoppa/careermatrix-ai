import React, { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ResponsiveContainer
} from "recharts";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";

/* ------------------ LOADING SPINNER ------------------ */

const LoadingSpinner = () => (
  <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
    <div className="bg-white dark:bg-gray-800 p-8 rounded-xl shadow-xl flex flex-col items-center space-y-4">
      <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
      <p className="text-blue-600 dark:text-blue-400 font-semibold">
        Analyzing Career Match...
      </p>
    </div>
  </div>
);

/* ------------------ MAIN APP ------------------ */

function Dashboard() {
  const [skills, setSkills] = useState("");
  const [interests, setInterests] = useState("");
  const [careerMode, setCareerMode] = useState("growth");
  const [risk, setRisk] = useState("medium");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [compareMode, setCompareMode] = useState(false);

  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);

  // 🔥 NEW STATE FOR RESUME
  const [resumeFile, setResumeFile] = useState(null);

  const compareRef = useRef(null);

  useEffect(() => {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
      setDarkMode(true);
      document.documentElement.classList.add("dark");
    }
  }, []);

  useEffect(() => {
    if (compareMode && compareRef.current) {
      compareRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [compareMode]);

  const toggleTheme = () => {
    if (darkMode) {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("theme", "light");
    } else {
      document.documentElement.classList.add("dark");
      localStorage.setItem("theme", "dark");
    }
    setDarkMode(!darkMode);
  };

  const handleSubmit = async () => {
    setLoading(true);
    setCompareMode(false);

    const response = await fetch("http://127.0.0.1:8000/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        skills: skills.split(",").map(s => s.trim()),
        interests: interests.split(",").map(i => i.trim()),
        career_mode: careerMode,
        risk_preference: risk,
      }),
    });

    const data = await response.json();
    setResult(data);
    setLoading(false);
  };

  // 🔥 NEW FUNCTION FOR RESUME UPLOAD
  const handleResumeUpload = async () => {
    if (!resumeFile) return;

    setLoading(true);
    setCompareMode(false);

    const formData = new FormData();
    formData.append("file", resumeFile);

    const response = await fetch("http://127.0.0.1:8000/upload-resume", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    // Auto-fill extracted skills into input
    if (data.skills) {
      setSkills(data.skills.join(", "));
    }

    setLoading(false);
  };

  const fetchHistory = async () => {
    const response = await fetch("http://127.0.0.1:8000/history");
    const data = await response.json();
    setHistory(data.history);
  };

  const reopenRecommendation = async (item) => {
    setSkills(item.skills);
    setInterests(item.interests);
    setCareerMode(item.career_mode);
    setRisk(item.risk_preference);
    setShowHistory(false);
    await handleSubmit();
  };

  const deleteHistory = async (id) => {
    await fetch(`http://127.0.0.1:8000/history/${id}`, {
      method: "DELETE",
    });
    fetchHistory();
  };

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 p-10 transition-colors duration-300">
      {loading && <LoadingSpinner />}

      <div className="max-w-6xl mx-auto bg-white dark:bg-gray-800 shadow-xl rounded-2xl p-8">

        {/* HEADER */}
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-blue-600 dark:text-blue-400">
            CareerMatrix AI
          </h1>

          <button
            onClick={toggleTheme}
            className="px-4 py-2 rounded-lg bg-gray-200 dark:bg-gray-700 text-sm"
          >
            {darkMode ? "☀ Light" : "🌙 Dark"}
          </button>
        </div>

        {/* FORM */}
        <div className="space-y-4">
          <input
            type="text"
            placeholder="Skills (python, math)"
            value={skills}
            onChange={(e) => setSkills(e.target.value)}
            className="w-full border rounded-lg p-3 bg-white dark:bg-gray-700 dark:text-white"
          />

          <input
            type="text"
            placeholder="Interests (ai, technology)"
            value={interests}
            onChange={(e) => setInterests(e.target.value)}
            className="w-full border rounded-lg p-3 bg-white dark:bg-gray-700 dark:text-white"
          />

          <select
            value={careerMode}
            onChange={(e) => setCareerMode(e.target.value)}
            className="w-full border rounded-lg p-3 bg-white dark:bg-gray-700 dark:text-white"
          >
            <option value="growth">Growth Mode</option>
            <option value="stability">Stability Mode</option>
          </select>

          <select
            value={risk}
            onChange={(e) => setRisk(e.target.value)}
            className="w-full border rounded-lg p-3 bg-white dark:bg-gray-700 dark:text-white"
          >
            <option value="low">Low Risk</option>
            <option value="medium">Medium Risk</option>
            <option value="high">High Risk</option>
          </select>

          <button
            onClick={handleSubmit}
            className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition"
          >
            Get Recommendation
          </button>

          {/* 🔥 RESUME UPLOAD SECTION */}
          <div className="border-t pt-4 space-y-3">
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Or upload your resume (PDF):
            </p>

            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setResumeFile(e.target.files[0])}
              className="w-full border rounded-lg p-3 bg-white dark:bg-gray-700 dark:text-white"
            />

            <button
              onClick={handleResumeUpload}
              disabled={!resumeFile}
              className="w-full bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 transition disabled:opacity-50"
            >
              📎 Upload Resume
            </button>
          </div>

          {/* HISTORY BUTTON */}
          <button
            onClick={() => {
              setShowHistory(!showHistory);
              fetchHistory();
            }}
            className="w-full bg-cyan-800 text-white py-3 rounded-lg hover:bg-blue-900 transition"
          >
            {showHistory ? "Hide History ⚠️" : "View Recommendation History 📜"}
          </button>
        </div>

        {/* EXISTING RESULT SECTION UNTOUCHED */}
        {result && (
          <div className="mt-10 space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              <SimpleCard title="🥇 Primary" data={result.primary_recommendation} isBest />
              <SimpleCard title="🥈 Backup" data={result.backup_recommendation} />
            </div>

            <button
              onClick={() => setCompareMode(!compareMode)}
              className="w-full bg-purple-600 text-white py-3 rounded-lg hover:bg-purple-700 transition"
            >
              {compareMode ? "Hide Details ▲" : "Compare Recommendation ▼"}
            </button>

            <AnimatePresence>
              {compareMode && (
                <motion.div
                  ref={compareRef}
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: 0.5 }}
                  className="overflow-hidden mt-6 grid md:grid-cols-2 gap-6"
                >
                  <DetailedComparison title="🥇 Primary" data={result.primary_recommendation} isBest />
                  <DetailedComparison title="🥈 Backup" data={result.backup_recommendation} />
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        )}
      </div>
    </div>
  );
}



/* ------------------ SIMPLE CARD ------------------ */

const SimpleCard = ({ title, data, isBest }) => (
  <div className="bg-gray-50 dark:bg-gray-700 p-6 rounded-xl shadow-md relative">
    {isBest && (
      <div className="absolute top-4 right-4 bg-green-500 text-white text-xs px-3 py-1 rounded-full shadow">
        🏆 Best Match
      </div>
    )}

    <h3 className="text-xl font-bold text-blue-600 dark:text-blue-400 mb-2">
      {title}
    </h3>

    <h4 className="text-lg font-semibold dark:text-white mb-2">
      {data.career}
    </h4>

    <p className="dark:text-gray-200"><strong>Match Score:</strong> {data.match_score}</p>
    <p className="dark:text-gray-200"><strong>Salary:</strong> ₹{data.average_salary_lpa} LPA</p>
  </div>
);

/* ------------------ DETAILED COMPARISON ------------------ */

const DetailedComparison = ({ title, data, isBest }) => {

  const reportRef = useRef(null);
  const confidence = Math.min(Math.round(data.match_score), 100);

  const radarData = [
    { subject: "Skill", value: data.score_breakdown.skill_score },
    { subject: "Interest", value: data.score_breakdown.interest_score },
    { subject: "Mode", value: data.score_breakdown.growth_or_stability_score },
    { subject: "Market", value: data.score_breakdown.market_score },
    { subject: "Risk", value: data.score_breakdown.risk_alignment_score }
  ];


  const exportPDF = async () => {
    const element = reportRef.current;

    const canvas = await html2canvas(element, {
      scale: 2,
      useCORS: true,
    });

    const imgData = canvas.toDataURL("image/png");
    const pdf = new jsPDF("p", "mm", "a4");

    const imgWidth = 210;
    const pageHeight = 297;

    const imgHeight = (canvas.height * imgWidth) / canvas.width;
    let heightLeft = imgHeight;

    let position = 0;

    pdf.addImage(imgData, "PNG", 0, position, imgWidth, imgHeight);
    heightLeft -= pageHeight;

    while (heightLeft > 0) {
      position = heightLeft - imgHeight;
      pdf.addPage();
      pdf.addImage(imgData, "PNG", 0, position, imgWidth, imgHeight);
      heightLeft -= pageHeight;
    }

    pdf.save(`${data.career}_Career_Report.pdf`);
  };



  return (
    <div ref={reportRef} className="bg-gray-50 dark:bg-gray-700 p-6 rounded-xl shadow-md space-y-6 relative">

      {isBest && (
        <div className="absolute top-4 right-4 bg-green-500 text-white text-xs px-3 py-1 rounded-full shadow">
          🏆 Best Match
        </div>
      )}

      <h3 className="text-xl font-bold text-blue-600 dark:text-blue-400">
        {title}
      </h3>

      <h4 className="text-lg font-semibold dark:text-white">
        {data.career}
      </h4>

      {/* Confidence */}
      <div>
        <h5 className="font-semibold dark:text-white mb-2">
          🔥 AI Confidence Prediction
        </h5>

        <div className="w-full bg-gray-300 dark:bg-gray-600 rounded-full h-4 overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${confidence}%` }}
            transition={{ duration: 1 }}
            className="h-4 bg-green-500 rounded-full"
          />
        </div>

        <p className="mt-2 text-sm font-semibold dark:text-gray-200">
          {confidence}% Match Confidence
        </p>
      </div>

      {/* Score Grid */}
      <div className="grid grid-cols-2 gap-4 bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm">
        <div>
          <p className="text-xs text-gray-400">Match Score</p>
          <p className="font-semibold dark:text-white">{data.match_score}</p>
        </div>
        <div>
          <p className="text-xs text-gray-400">Market Demand</p>
          <p className="font-semibold dark:text-white">{data.market_demand}/10</p>
        </div>
        <div>
          <p className="text-xs text-gray-400">Risk Level</p>
          <p className="font-semibold dark:text-white">{data.risk_level}/10</p>
        </div>
        <div>
          <p className="text-xs text-gray-400">Salary</p>
          <p className="font-semibold dark:text-white">
            ₹{data.average_salary_lpa} LPA
          </p>
        </div>
      </div>

      {/* Matched Skills */}
      <div>
        <h5 className="font-semibold dark:text-white mb-2">🟢 Matched Skills</h5>
        {data.matched_skills.length > 0 ? (
          <ul className="list-disc list-inside text-green-600">
            {data.matched_skills.map((skill, i) => <li key={i}>{skill}</li>)}
          </ul>
        ) : (
          <p className="text-gray-400 italic">None</p>
        )}
      </div>

      {/* Missing Skills */}
      <div>
        <h5 className="font-semibold dark:text-white mb-2">
          🔴 Skills You Need to Improve
        </h5>
        {data.missing_skills.length > 0 ? (
          <ul className="list-disc list-inside text-red-500">
            {data.missing_skills.map((skill, i) => <li key={i}>{skill}</li>)}
          </ul>
        ) : (
          <p className="text-gray-400 italic">None</p>
        )}
      </div>

      {/* Roadmap */}
      <div>
        <h5 className="font-semibold dark:text-white mb-6">
          12-Month Career Roadmap
        </h5>

        <div className="relative pl-12">
          <div className="absolute left-5 top-0 bottom-0 w-0.5 bg-blue-500"></div>

          {Object.entries(data.career_roadmap).map(([phase, tasks], index) => (
            <div key={index} className="relative mb-10">

              <div className="absolute right-1 top-0 text-blue-500 text-[30px]">
                ↼
              </div>

              <h6 className="font-semibold text-blue-600 dark:text-blue-400 mb-3">
                {phase}
              </h6>

              <div className="space-y-2">
                {tasks.map((task, i) => (
                  <div
                    key={i}
                    className="bg-white dark:bg-gray-800 p-3 rounded-lg shadow-sm text-sm dark:text-gray-200"
                  >
                    {task}
                  </div>
                ))}
              </div>

            </div>
          ))}
        </div>
      </div>

      {/* Radar */}
      <div>
        <h5 className="font-semibold dark:text-white mb-4">
          Score Radar Breakdown
        </h5>

        <ResponsiveContainer width="100%" height={300}>
          <RadarChart data={radarData}>
            <PolarGrid />
            <PolarAngleAxis dataKey="subject" />
            <PolarRadiusAxis />
            <Radar
              dataKey="value"
              stroke="#2563eb"
              fill="#3b82f6"
              fillOpacity={0.6}
            />
          </RadarChart>
        </ResponsiveContainer>
      </div>

      {/* Export PDF */}
      <div className="pt-4 border-t border-gray-300 dark:border-gray-600">
        <button
          onClick={exportPDF}
          className="w-full bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 transition font-semibold"
        >
          📄 Export Career Report as PDF
        </button>
      </div>

    </div>
  );
};

export default Dashboard;

