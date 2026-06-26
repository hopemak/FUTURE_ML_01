import { useState } from 'react';
import { UploadCloud, FileSpreadsheet, CheckCircle } from 'lucide-react';
import { uploadFile } from '../utils/api';

export default function Upload() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResult(null);
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    try {
      const response = await uploadFile(file);
      setResult(response.data);
    } catch (error) {
      alert('Upload failed: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Upload Sales Data</h1>
      
      <div className="card">
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center">
          <UploadCloud className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <p className="text-lg text-gray-600 mb-4">Drag and drop your CSV file here</p>
          <input
            type="file"
            accept=".csv"
            onChange={handleFileChange}
            className="hidden"
            id="file-input"
          />
          <label htmlFor="file-input" className="btn-primary cursor-pointer inline-block">
            Select File
          </label>
          {file && (
            <div className="mt-4 flex items-center justify-center gap-2 text-green-600">
              <FileSpreadsheet className="w-5 h-5" />
              <span>{file.name}</span>
            </div>
          )}
        </div>

        {file && (
          <button
            onClick={handleUpload}
            disabled={loading}
            className="btn-success w-full mt-6"
          >
            {loading ? 'Processing...' : 'Upload & Predict'}
          </button>
        )}

        {result && (
          <div className="mt-6 p-4 bg-green-50 rounded-lg">
            <div className="flex items-center gap-2 text-green-700 mb-2">
              <CheckCircle className="w-5 h-5" />
              <span className="font-semibold">Upload Successful!</span>
            </div>
            <p className="text-gray-600">Total rows processed: {result.total_rows}</p>
            <p className="text-gray-600">Predictions generated: {result.predictions?.length}</p>
          </div>
        )}
      </div>
    </div>
  );
}
