import { useRouter } from "next/router";

export default function Results() {
  const router = useRouter();
  const { status } = router.query;

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-b from-white to-blue-500 p-6">
      {/* RAPIFY RESULTS Title - Matches Home Page */}
      <h1 className="text-7xl sm:text-8xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-800 to-teal-400 mb-8 font-['Poppins'] tracking-wide text-center">
        RAPIFY RESULTS
      </h1>

      {/* SUCCESS or FAILURE Message - Bigger and Bubbly Font */}
      <p
        className={`text-5xl font-extrabold ${
          status === "success" ? "text-green-500" : "text-red-500"
        } drop-shadow-lg tracking-wide mb-8`}
      >
        {status === "success" ? "✨ SUCCESS ✨" : "💀 FAILURE 💀"}
      </p>

      {/* Placeholder for Analysis Results - 3 Smaller Boxes */}
      <div className="grid grid-cols-3 gap-6 mt-6">
        <div className="w-64 h-32 bg-white bg-opacity-90 backdrop-blur-md rounded-2xl shadow-2xl flex items-center justify-center">
          <p className="text-gray-700 text-lg font-semibold">🔍 Placeholder 1</p>
        </div>
        <div className="w-64 h-32 bg-white bg-opacity-90 backdrop-blur-md rounded-2xl shadow-2xl flex items-center justify-center">
          <p className="text-gray-700 text-lg font-semibold">🎵 Placeholder 2</p>
        </div>
        <div className="w-64 h-32 bg-white bg-opacity-90 backdrop-blur-md rounded-2xl shadow-2xl flex items-center justify-center">
          <p className="text-gray-700 text-lg font-semibold">📊 Placeholder 3</p>
        </div>
      </div>

      {/* General Text Feedback Box - Larger Placeholder */}
      <div className="w-full max-w-3xl h-48 bg-white bg-opacity-90 backdrop-blur-md rounded-2xl shadow-2xl flex items-center justify-center mt-8 p-6">
        <p className="text-gray-700 text-lg font-semibold">📝 General Feedback Placeholder</p>
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
