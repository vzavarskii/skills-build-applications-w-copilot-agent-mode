import React, { useState, useEffect } from 'react';

function Users() {
  const [users, setUsers] = useState([]);
  const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/users/`;

  useEffect(() => {
    console.log('Fetching users from REST API endpoint:', apiUrl);
    fetch(apiUrl)
      .then(response => response.json())
      .then(data => {
        console.log('Users data fetched from API:', data);
        setUsers(Array.isArray(data) ? data : (data.results || []));
      })
      .catch(error => console.error('Error fetching users:', error));
  }, [apiUrl]);

  return (
    <div className="card octofit-card">
      <div className="card-header d-flex align-items-center gap-2">
        <span>&#128100;</span>
        <span>Users</span>
        <span className="badge bg-secondary ms-auto">{users.length}</span>
      </div>
      <div className="card-body">
        {users.length === 0 ? (
          <p className="empty-state">No users found.</p>
        ) : (
          <div className="table-responsive">
            <table className="table table-striped table-hover octofit-table mb-0">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Team</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {users.map(user => (
                  <tr key={user.id}>
                    <td className="fw-semibold">{user.name}</td>
                    <td><a href={`mailto:${user.email}`} className="text-decoration-none">{user.email}</a></td>
                    <td>{user.team}</td>
                    <td>
                      <span className={`badge ${user.is_active ? 'badge-active' : 'badge-inactive'}`}>
                        {user.is_active ? 'Active' : 'Inactive'}
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

export default Users;
