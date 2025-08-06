import React, { useState } from 'react';
import UploadForm from './components/UploadForm';

function App() {
  const [reportData, setReportData] = useState([]);

  return (
    <div style={{ padding: 20 }}>
      <h1>Report Generator</h1>
      <UploadForm setReportData={setReportData} />

      {reportData.map((student, idx) => (
        <div key={idx} style={{ marginTop: 20 }}>
          <h3>{student.name}</h3>
          <ul>
            {Object.entries(student.subjects).map(([subject, data]) => (
              <li key={subject}>
                <b>{subject}</b> - {data.score} <br />
                <i>{data.comment}</i>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}

export default App;
