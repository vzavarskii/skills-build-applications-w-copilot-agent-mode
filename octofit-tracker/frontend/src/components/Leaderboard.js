import React, { useState, useEffect } from 'react';

function Leaderboard() {
  const [entries, setEntries] = useState([]);
  const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/leaderboard/`;

  useEffect(() => {
    console.log('Fetching leaderboard from REST API endpoint:', apiUrl);
    fetch(apiUrl)
      .then(response => response.json())
      .then(data => {
        console.log('Leaderboard data fetched from API:', data);
        setEntries(Array.isArray(data) ? data : (data.results || []));
      })
      .catch(error => console.error('Error fetching leaderboard:', error));
  }, [apiUrl]);

  const sorted = [...entries].sort((a, b) => b.points - a.points);
  const medals = ['\uD83E\uDD47', '\uD83E\uDD48', '\uD83E\uDD49'];

  return (
    <div className="card octofit-card">
      <div className="card-header d-flex align-items-center gap-2">
        <span>&#127942;</span>
        <span>Leaderboard</span>
        <span className="badge bg-secondary ms-auto">{entries.length} teams</span>
      </div>
      <div className="card-body">
        {sorted.length === 0 ? (
          <p className="empty-state">No leaderboard data found.</p>
        ) : (
          <div className="table-responsive">
            <table className="table table-striped table-hover octofit-table mb-0">
              <thead>
                <tr>
                  <th style={{width:'3rem'}}>#</th>
                  <th>Team</th>
                  <th>Points</th>
                </tr>
              </thead>
              <tbody>
                {sorted.map((entry, index) => (
                  <tr key={entry.id}>
                    <td className="text-center fw-bold">
                      {medals[index] || index + 1}
                    </td>
                    <td className="fw-semibold">{entry.team}</td>
                    <td>
                      <span className="badge" style={{backgroundColor:'#e94560', fontSize:'0.95rem'}}>
                        {entry.points} pts
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default Leaderboard;
