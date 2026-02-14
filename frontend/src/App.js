import React, { useState } from "react";

function App() {
  const [skills, setSkills] = useState("");
  const [interests, setInterests] = useState("");
  const [careerMode, setCareerMode] = useState("growth");
  const [risk, setRisk] = useState("medium");
  const [result, setResult] = useState(null);

  const handleSubmit = async () => {
    const response = await fetch("http://127.0.0.1:8000/recommend", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        skills: skills.split(",").map(s => s.trim()),
        interests: interests.split(",").map(i => i.trim()),
        career_mode: careerMode,
        risk_preference: risk,
      }),
    });

    const data = await response.json();
    setResult(data);
  };

  const renderCareer = (careerData, title) => (
    <div style={{ border: "1px solid #ccc", padding: "20px", marginTop: "20px", borderRadius: "8px" }}>
      <h2>{title}</h2>
      <h3>{careerData.career}</h3>
      <p><b>Match Score:</b> {careerData.match_score}</p>
      <p><b>Average Salary (LPA):</b> {careerData.average_salary_lpa}</p>
      <p><b>Risk Level:</b> {careerData.risk_level}</p>
      <p><b>Market Demand:</b> {careerData.market_demand}</p>

      <h4>Matched Skills:</h4>
      <ul>
        {careerData.matched_skills.map((skill, index) => (
          <li key={index}>{skill}</li>
        ))}
      </ul>

      <h4>Skill Gap Learning Plan:</h4>
      <ul>
        {careerData.learning_plan.map((item, index) => (
          <li key={index}>
            <b>{item.skill_to_learn}</b> — {item.difficulty_level} — {item.estimated_timeline}
          </li>
        ))}
      </ul>

      <h4>12-Month Roadmap:</h4>
      {Object.entries(careerData.career_roadmap).map(([phase, tasks], index) => (
        <div key={index}>
          <b>{phase}</b>
          <ul>
            {tasks.map((task, i) => (
              <li key={i}>{task}</li>
            ))}
          </ul>
        </div>
      ))}

      <h4>Score Breakdown:</h4>
      <ul>
        {Object.entries(careerData.score_breakdown).map(([key, value], index) => (
          <li key={index}>
            {key}: {value}
          </li>
        ))}
      </ul>
    </div>
  );

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>CareerMatrix AI</h1>

      <div>
        <label>Skills (comma separated)</label><br />
        <input
          type="text"
          value={skills}
          onChange={(e) => setSkills(e.target.value)}
          placeholder="python, math"
          style={{ width: "300px" }}
        />
      </div>

      <div style={{ marginTop: "10px" }}>
        <label>Interests (comma separated)</label><br />
        <input
          type="text"
          value={interests}
          onChange={(e) => setInterests(e.target.value)}
          placeholder="ai, technology"
          style={{ width: "300px" }}
        />
      </div>

      <div style={{ marginTop: "10px" }}>
        <label>Career Mode</label><br />
        <select value={careerMode} onChange={(e) => setCareerMode(e.target.value)}>
          <option value="growth">Growth</option>
          <option value="stability">Stability</option>
        </select>
      </div>

      <div style={{ marginTop: "10px" }}>
        <label>Risk Preference</label><br />
        <select value={risk} onChange={(e) => setRisk(e.target.value)}>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </div>

      <button style={{ marginTop: "20px" }} onClick={handleSubmit}>
        Get Recommendation
      </button>

      {result && (
        <div style={{ marginTop: "40px" }}>
          {renderCareer(result.primary_recommendation, "🎯 Primary Career")}
          {renderCareer(result.backup_recommendation, "🔁 Backup Career")}
        </div>
      )}
    </div>
  );
}

export default App;
