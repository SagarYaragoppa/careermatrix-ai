import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function ResumeParser() {

  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [jobSkills, setJobSkills] = useState("");

  const navigate = useNavigate();

  const handleUpload = async () => {

    if (!file) {
      alert("Please upload a resume first");
      return;
    }

    setLoading(true);

    const formData = new FormData();

    formData.append("file", file);
    formData.append("job_skills", jobSkills);

    try {

      const response = await fetch("http://127.0.0.1:8000/upload-resume", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      setResult(data);

    } catch (error) {
      console.error("Upload error:", error);
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-10">

      <div className="max-w-3xl mx-auto bg-white shadow-xl rounded-xl p-8 space-y-6">

        {/* TITLE */}
        <h1 className="text-2xl font-bold text-center">
          Resume Intelligence
        </h1>

        {/* BACK BUTTON */}
        <div className="mb-6 flex justify-center">

          <button
            onClick={() => navigate("/")}
            className="relative text-black text-lg font-medium group"
          >
            ⬅ Back to CareerMatrix

            <span
              className="absolute left-0 -bottom-1 h-[4px] w-full 
              bg-gradient-to-r from-purple-600 to-pink-300 
              rounded-full shadow-[0_0_20px_rgba(168,85,247,1)]
              transition-all duration-300 
              group-hover:scale-x-110"
            ></span>

          </button>

        </div>


        {/* JOB SKILLS INPUT */}
        <input
          type="text"
          placeholder="Enter job description skills (python, ml, sql)"
          value={jobSkills}
          onChange={(e) => setJobSkills(e.target.value)}
          className="w-full border rounded p-3"
        />


        {/* FILE INPUT */}
        <input
          type="file"
          accept=".pdf,.docx"
          onChange={(e) => setFile(e.target.files[0])}
          className="w-full border p-3 rounded"
        />


        {/* UPLOAD BUTTON */}
        <button
          onClick={handleUpload}
          className="w-full bg-blue-600 text-white py-3 rounded hover:bg-blue-700 transition"
        >
          Upload Resume
        </button>


        {/* LOADING */}
        {loading && (
          <p className="text-center">Parsing Resume...</p>
        )}


        {/* RESULTS */}
        {result && (

          <div className="bg-gray-100 p-4 rounded space-y-4 mt-6">

            <h2 className="text-lg font-semibold">
              Resume Analysis
            </h2>


            {/* RESUME SCORE */}
            <div className="bg-green-100 p-4 rounded">
              <h3 className="text-lg font-semibold">
                Resume Score: {result.resume_score} / 100
              </h3>
            </div>


            {/* SCORE BREAKDOWN */}
            <div className="bg-gray-50 p-4 rounded">

              <h3 className="font-semibold mb-2">
                Score Breakdown
              </h3>

              <p>Skills: {result.score_breakdown?.skills}</p>
              <p>Projects: {result.score_breakdown?.projects}</p>
              <p>Experience: {result.score_breakdown?.experience}</p>
              <p>Education: {result.score_breakdown?.education}</p>

            </div>


            {/* BASIC INFO */}
            <p><b>Name:</b> {result.name || "Not detected"}</p>
            <p><b>Email:</b> {result.email || "Not detected"}</p>
            <p><b>Phone:</b> {result.phone || "Not detected"}</p>


            {/* SKILLS */}
            <p>
              <b>Skills:</b> {result.skills?.join(", ") || "None detected"}
            </p>


            {/* EDUCATION */}
            <p>
              <b>Education:</b> {result.education?.join(", ") || "Not detected"}
            </p>


            {/* EXPERIENCE */}
            <p>
              <b>Experience:</b> {result.experience?.join(", ") || "Not detected"}
            </p>


            {/* PROJECTS */}
            <div>
              <b>Projects:</b>

              <ul className="list-disc ml-6">
                {result.projects?.length > 0 ? (
                  result.projects.map((p, i) => (
                    <li key={i}>{p}</li>
                  ))
                ) : (
                  <li>No projects detected</li>
                )}
              </ul>
            </div>


            {/* JOB MATCH ANALYSIS */}
            {result?.job_match && (

              <div className="bg-purple-50 p-4 rounded-lg">

                <h3 className="font-semibold text-lg mb-2">
                  Job Match Analysis
                </h3>

                <p>
                  Match Score: {result.job_match.match_score}%
                </p>

                <p>
                  Matched Skills: {result.job_match?.matched_skills?.join(", ") || "None"}
                </p>

                <p>
                  Missing Skills: {result.job_match?.missing_skills?.join(", ") || "None"}
                </p>

              </div>

            )}


            {/* CANDIDATE SUMMARY */}
            <div className="bg-blue-50 p-4 rounded-lg">

              <h3 className="font-semibold text-lg mb-2">
                Candidate Summary
              </h3>

              <p>
                {result?.candidate_summary}
              </p>

            </div>


            {/* RESUME FEEDBACK */}
            <div className="bg-blue-50 p-4 rounded-lg">

              <h3 className="font-semibold mb-2">
                Resume Feedback
              </h3>

              {result.skills?.length > 5 ? (
                <p>✅ Good technical skill coverage.</p>
              ) : (
                <p>⚠ Consider adding more technical skills.</p>
              )}

              {result.experience?.length > 0 ? (
                <p>✅ Experience section detected.</p>
              ) : (
                <p>⚠ Add internship or project experience.</p>
              )}

            </div>


            {/* CAREER ALIGNMENT */}
            <div className="bg-purple-50 p-4 rounded-lg">

              <h3 className="font-semibold mb-2">
                Career Alignment
              </h3>

              <p>AI / ML Engineer → {result.skills?.includes("python") ? "80%" : "40%"}</p>
              <p>Data Analyst → {result.skills?.includes("sql") ? "75%" : "50%"}</p>
              <p>Backend Developer → {result.skills?.includes("java") ? "70%" : "45%"}</p>

            </div>

          </div>

        )}

      </div>

    </div>
  );
}

export default ResumeParser;