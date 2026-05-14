import React, { useState, useEffect } from 'react';

function Teams() {
  const [teams, setTeams] = useState([]);
  const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/teams/`;

  useEffect(() => {
    console.log('Fetching teams from REST API endpoint:', apiUrl);
    fetch(apiUrl)
      .then(response => response.json())
      .then(data => {
        console.log('Teams data fetched from API:', data);
        setTeams(Array.isArray(data) ? data : (data.results || []));
      })
      .catch(error => console.error('Error fetching teams:', error));
  }, [apiUrl]);

  return (
    <div className="card octofit-card">
      <div className="card-header d-flex align-items-center gap-2">
        <span>&#127942;</span>
        <span>Teams</span>
        <span className="badge bg-secondary ms-auto">{teams.length}</span>
      </div>
      <div className="card-body">
        {teams.length === 0 ? (
          <p className="empty-state">No teams found.</p>
        ) : (
          <div className="table-responsive">
            <table className="table table-striped table-hover octofit-table mb-0">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                {teams.map(team => (
                  <tr key={team.id}>
                    <td className="fw-semibold">{team.name}</td>
                    <td className="text-muted">{team.description || <em>No description</em>}</td>
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

export default Teams;
