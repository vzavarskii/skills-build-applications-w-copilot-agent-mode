import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;

  useEffect(() => {
    console.log('Fetching workouts from REST API endpoint:', apiUrl);
    fetch(apiUrl)
      .then(response => response.json())
      .then(data => {
        console.log('Workouts data fetched from API:', data);
        setWorkouts(Array.isArray(data) ? data : (data.results || []));
      })
      .catch(error => console.error('Error fetching workouts:', error));
  }, [apiUrl]);

  return (
    <div className="card octofit-card">
      <div className="card-header d-flex align-items-center gap-2">
        <span>&#128170;</span>
        <span>Workouts</span>
        <span className="badge bg-secondary ms-auto">{workouts.length}</span>
      </div>
      <div className="card-body">
        {workouts.length === 0 ? (
          <p className="empty-state">No workouts found.</p>
        ) : (
          <div className="table-responsive">
            <table className="table table-striped table-hover octofit-table mb-0">
              <thead>
                <tr>
                  <th>User</th>
                  <th>Name</th>
                  <th>Description</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {workouts.map(workout => (
                  <tr key={workout.id}>
                    <td className="fw-semibold">{workout.user}</td>
                    <td>{workout.name}</td>
                    <td className="text-muted">{workout.description || <em>None</em>}</td>
                    <td>{workout.date}</td>
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

export default Workouts;
