import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/router"; // ⬅ Add for navigation

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");
  const [currentWord, setCurrentWord] = useState("playing");
  const fileInputRef = useRef<HTMLInputElement>(null);
  const router = useRouter(); // ⬅ Hook for navigation

  // Cycling words for the blank space
  useEffect(() => {
    const words = ["playing", "life", "music"];
    let index = 0;

    const interval = setInterval(() => {
      index = (index + 1) % words.length;
      setCurrentWord(words[index]);
    }, 1000);

    return () => clearInterval(interval); // Cleanup on component unmount
  }, []);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files?.[0]) {
      setFile(event.target.files[0]);
      setMessage(`🎵 Selected: ${event.target.files[0].name}`);
    }
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    const droppedFile = event.dataTransfer.files?.[0];
    if (droppedFile) {
      setFile(droppedFile);
      setMessage(`🎶 Selected: ${droppedFile.name}`);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("⚠️ Please select or drop a file.");
      return;
    }

    setUploading(true);
    setMessage("🎼 Uploading...");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        router.push(`/results?status=success`); // ⬅ Redirect to results page
      } else {
        router.push(`/results?status=failure`); // ⬅ Redirect with failure
      }
    } catch (error) {
      router.push(`/results?status=failure`); // ⬅ Redirect if error
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-b from-white to-blue-500 p-6 flex-col">
      {/* Title with cycling text */}
      <h1 className="text-3xl sm:text-4xl font-normal text-black mb-4 font-['Poppins'] tracking-wide text-center pt-12">
        Make your <span className="text-blue-600">{currentWord}</span> sound better with
      </h1>

      {/* Rapify title */}
      <h2 className="text-7xl sm:text-8xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-800 to-teal-400 mb-16 font-['Poppins'] tracking-wide text-center">
        Rapify
      </h2>

      <div className="w-full max-w-2xl bg-white bg-opacity-90 backdrop-blur-md rounded-2xl shadow-2xl p-10 text-center border border-white/30 transition-all duration-300 transform hover:scale-105 hover:shadow-3xl hover:ring-4 hover:ring-blue-500">
        
        {/* Drag & Drop Box */}
        <div
          className="border-2 border-dashed border-gray-700 rounded-lg p-8 mb-6 text-gray-900 cursor-pointer bg-white bg-opacity-70 hover:bg-opacity-90 transition-all duration-300 transform hover:scale-105 hover:border-blue-500"
          onClick={() => fileInputRef.current?.click()}
          onDragOver={(e) => e.preventDefault()}
          onDrop={handleDrop}
        >
          {file ? (
            <p className="text-xl font-medium">{file.name}</p>
          ) : (
            <p className="text-xl opacity-80">🎤 Drag & drop or click to upload</p>
          )}
        </div>

        {/* Hidden File Input */}
        <input
          type="file"
          accept="audio/*"
          className="hidden"
          ref={fileInputRef}
          onChange={handleFileChange}
        />

        {/* Upload Button */}
        <button
          onClick={handleUpload}
          className="mt-6 px-8 py-4 bg-gradient-to-r from-blue-400 to-blue-600 text-white font-bold rounded-lg shadow-md hover:bg-gradient-to-r hover:from-blue-600 hover:to-blue-400 hover:scale-105 transition-all duration-200"
          disabled={uploading}
        >
          {uploading ? "🎼 Uploading..." : "🚀 Upload"}
        </button>

        {/* Message Display */}
        {message && (
          <p className="mt-6 text-gray-900 text-lg font-medium">{message}</p>
        )}
      </div>
    </div>
  );
}
