import React, { useState } from 'react';
import axios from 'axios';

function UploadForm() {
  const [file, setFile] = useState(null);
  const [reportLinks, setReportLinks] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    setLoading(true);

    try {
      const response = await axios.post('http://localhost:5000/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      if (response.data.reports) {
        setReportLinks(response.data.reports);
      } else {
        alert('No reports returned!');
      }
    } catch (err) {
      alert('Upload failed. Check console.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-container">
      <h2>Upload Student Marks Excel</h2>
      <input type="file" accept=".xlsx,.xls" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Uploading..." : "Generate Reports"}
      </button>

      <div className="report-links">
        {reportLinks.length > 0 && <h3>Generated Reports</h3>}
        <ul>
          {reportLinks.map((report, idx) => (
            <li key={idx}>
              <a href={`http://localhost:5000/download/${report.name}`} target="_blank" rel="noreferrer">
                {report.name}'s Report
              </a>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default UploadForm;
