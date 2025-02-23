import { useRouter } from "next/router";
import { useState, useEffect } from "react";

export default function Results() {
  const router = useRouter();
  const [evaluationData, setEvaluationData] = useState({
    success: true,
    placeholder1: "",
    placeholder2: "",
    placeholder3: "",
    summary: "",
  });

  useEffect(() => {
    const data = localStorage.getItem("evaluationData");
    if (data) {
      setEvaluationData(JSON.parse(data));
    }
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-b from-white to-blue-500 p-6">
      {/* RAPIFY RESULTS Title */}
      <h1 className="text-7xl sm:text-8xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-800 to-teal-400 mb-8 font-['Poppins'] tracking-wide text-center">
        RAPIFY RESULTS
      </h1>

      {/* SUCCESS or FAILURE Message using evaluationData.success */}
      <p
        className={`text-5xl font-extrabold ${
          evaluationData.success ? "text-green-500" : "text-red-500"
        } drop-shadow-lg tracking-wide mb-8`}
      >
        {evaluationData.success ? "✨ SUCCESS ✨" : "💀 FAILURE 💀"}
      </p>

      {/* Analysis Placeholders */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mt-6 w-full max-w-4xl">
        <div className="w-full min-h-32 bg-white bg-opacity-90 backdrop-blur-md rounded-2xl shadow-2xl flex flex-col items-center justify-center p-4">
          <h2 className="text-lg font-bold mb-1">BPM</h2>
          <p className="text-gray-700 text-base font-semibold whitespace-pre-wrap text-center">
            {evaluationData.placeholder1 || "Placeholder 1"}
          </p>
        </div>
        <div className="w-full min-h-32 bg-white bg-opacity-90 backdrop-blur-md rounded-2xl shadow-2xl flex flex-col items-center justify-center p-4">
          <h2 className="text-lg font-bold mb-1">Word Choice</h2>
          <p className="text-gray-700 text-base font-semibold whitespace-pre-wrap text-center">
            {evaluationData.placeholder2 || "Placeholder 2"}
          </p>
        </div>
        <div className="w-full min-h-32 bg-white bg-opacity-90 backdrop-blur-md rounded-2xl shadow-2xl flex flex-col items-center justify-center p-4">
          <h2 className="text-lg font-bold mb-1">Themes</h2>
          <p className="text-gray-700 text-base font-semibold whitespace-pre-wrap text-center">
            {evaluationData.placeholder3 || "Placeholder 3"}
          </p>
        </div>
      </div>

      {/* Detailed Summary */}
      <div className="w-full max-w-4xl min-h-48 bg-white bg-opacity-90 backdrop-blur-md rounded-2xl shadow-2xl flex flex-col items-start mt-8 p-6 overflow-y-auto">
        <h2 className="text-xl font-bold mb-2">Detailed Summary</h2>
        <p className="text-gray-700 text-lg font-semibold whitespace-pre-wrap">
          {evaluationData.summary || "General Feedback Placeholder"}
        </p>
      </div>

      {/* Back Button */}
      <button
        onClick={() => router.push("/")}
        className="mt-10 px-8 py-4 bg-gradient-to-r from-blue-400 to-blue-600 text-white text-lg font-semibold rounded-lg shadow-md hover:bg-gradient-to-r hover:from-blue-600 hover:to-blue-400 hover:scale-105 transition-all"
      >
        ⬅ Back to Upload
      </button>
    </div>
  );
}