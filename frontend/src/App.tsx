import { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import axios from 'axios';

function LogsPage() {
  const [logText, setLogText] = useState<string>('Loading...');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    axios.get('/logs/validation-failures')
      .then(res => setLogText(res.data))
      .catch(() => {
        setLogText('');
        setError('Failed to load validation failures log.');
      });
  }, []);

  return (
    <section className="p-4">
      <h1 className="text-2xl font-semibold mb-4">Validation Failures Log</h1>
      {error && <p className="text-red-600 mb-2">{error}</p>}
      <pre className="bg-gray-100 p-4 rounded shadow max-h-[70vh] overflow-auto whitespace-pre-wrap">
        {logText || 'No entries found.'}
      </pre>
    </section>
  );
}

function MockPage() {
  const [mockData, setMockData] = useState<Record<string, any> | null>(null);
  const [result, setResult] = useState<Record<string, any> | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    axios.get('/mock/caregiver')
      .then(res => setMockData(res.data))
      .catch(() => setMockData(null));
  }, []);

  const handleCorrection = async () => {
    setLoading(true);
    try {
      const res = await axios.post('/mock/correct');
      setResult(res.data);
    } catch (err) {
      setResult({ error: 'Correction failed. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="p-4">
      <h1 className="text-2xl font-semibold mb-4">Mock Caregiver Record</h1>
      {mockData ? (
        <div className="mb-4">
          <pre className="bg-gray-100 p-4 rounded shadow whitespace-pre-wrap">
            {JSON.stringify(mockData, null, 2)}
          </pre>
          <button
            onClick={handleCorrection}
            disabled={loading}
            className="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Correcting...' : 'Run Correction'}
          </button>
        </div>
      ) : (
        <p className="text-red-600">Failed to load mock caregiver data.</p>
      )}
      {result && (
        <div className="mt-4 p-4 bg-green-100 text-green-700 rounded shadow">
          <h2 className="font-medium">Correction Result</h2>
          <pre className="whitespace-pre-wrap">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </section>
  );
}

function App() {
  return (
    <Router>
      <main className="min-h-screen flex flex-col font-sans">
        <header className="p-6 border-b">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">OpenPhone → AxisCare Admin</h1>
          <nav className="space-x-4">
            <Link to="/logs" className="text-blue-600 hover:underline">Logs</Link>
            <Link to="/mock" className="text-blue-600 hover:underline">Mock</Link>
          </nav>
        </header>

        <div className="flex-grow">
          <Routes>
            <Route path="/logs" element={<LogsPage />} />
            <Route path="/mock" element={<MockPage />} />
          </Routes>
        </div>

        <footer className="text-center text-sm text-gray-500 py-4 border-t">
          Built by Michael · {new Date().getFullYear()}
        </footer>
      </main>
    </Router>
  );
}

export default App;
