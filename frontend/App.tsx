import { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import axios from 'axios';

function LogsPage() {
  const [logText, setLogText] = useState('Loading...');

  useEffect(() => {
    axios.get('/logs/validation-failures')
      .then(res => setLogText(res.data))
      .catch(err => setLogText('Error loading log'));
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Validation Failures</h1>
      <pre className="bg-gray-100 p-4 rounded max-h-[70vh] overflow-auto whitespace-pre-wrap">{logText}</pre>
    </div>
  );
}

function MockPage() {
  const [mockData, setMockData] = useState(null);
  const [result, setResult] = useState(null);

  useEffect(() => {
    axios.get('/mock/caregiver')
      .then(res => setMockData(res.data));
  }, []);

  const correct = () => {
    axios.post('/mock/correct')
      .then(res => setResult(res.data));
  };

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Mock Caregiver</h1>
      {mockData && (
        <div className="mb-4">
          <pre className="bg-gray-100 p-4 rounded whitespace-pre-wrap">{JSON.stringify(mockData, null, 2)}</pre>
          <button onClick={correct} className="mt-2 px-4 py-2 bg-blue-600 text-white rounded">Correct</button>
        </div>
      )}
      {result && (
        <div className="mt-4 text-green-700">
          Correction Complete: {JSON.stringify(result)}
        </div>
      )}
    </div>
  );
}

function App() {
  return (
    <Router>
      <div className="p-4">
        <nav className="mb-4 space-x-4">
          <Link to="/logs" className="text-blue-500 hover:underline">Logs</Link>
          <Link to="/mock" className="text-blue-500 hover:underline">Mock</Link>
        </nav>
        <Routes>
          <Route path="/logs" element={<LogsPage />} />
          <Route path="/mock" element={<MockPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
