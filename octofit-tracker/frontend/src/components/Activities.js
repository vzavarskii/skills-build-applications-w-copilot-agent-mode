import React, { useState, useEffect } from 'react';

function Activities() {
  const [activities, setActivities] = useState([]);
  const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/activities/`;

  useEffect(() => {
    console.log('Fetching activities from REST API endpoint:', apiUrl);
    fetch(apiUrl)
      .then(response => response.json())
      .then(data => {
        console.log('Activities data fetched from API:', data);
        setActivities(Array.isArray(data) ? data : (data.results || []));
      })
      .catch(error => console.error('Error fetching activities:', error));
  }, [apiUrl]);

  return (
    <div className="card octofit-card">
      <div className="card-header d-flex align-items-center gap-2">
        <span>&#127939;</span>
        <span>Activities</span>
        <span className="badge bg-secondary ms-auto">{activities.length}</span>
      </div>
      <div className="card-body">
        {activities.length === 0 ? (
          <p className="empty-state">No activities found.</p>
        ) : (
          <div className="table-responsive">
            <table className="table table-striped table-hover octofit-table mb-0">
              <thead>
                <tr>
                  <th>User</th>
                  <th>Activity Type</th>
                  <th>Duration (min)</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {activities.map(activity => (
                  <tr key={activity.id}>
                    <td className="fw-semibold">{activity.user}</td>
                    <td>
                      <span className="badge" style={{backgroundColor:'#0f3460'}}>
                        {activity.activity_type}
                      </span>
                    </td>
                    <td>{activity.duration} min</td>
                    <td>{activity.date}</td>
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

export default Activities;
