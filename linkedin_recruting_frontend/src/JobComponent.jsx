import React, { useState, useEffect } from 'react';

const JobComponent=({refresh}) =>  {

    const host = import.meta.env.VITE_HOST;
    const [jobs, setJobs] = useState([]);
    const [rolesList, setRolesList] = useState([]);
    const [role, setRole] = useState('');

  useEffect(() => {
    const fetchRoles = async () => {
      try {
        const response = await fetch(`http://${host}:8081/view_jobs/`);
        if (response.ok) {
          const data = await response.json();
          const roles = Object.values(data).map((item) => item.role);
          setRolesList(roles);
          setRoles(roles)
        } else {
          console.error('Failed to fetch roles');
        }
      } catch (error) {
        console.error('Error fetching roles:', error);
      }
    };

    const fetchJobs = async () => {
      try {
        console.log("L'URL de l'API est :", host);
        const response = await fetch(`http://${host}:8081/view_jobs/`);
        if (response.ok) {
          const data = await response.json();
          const jobsList = Object.values(data).map((item) => ({
            role: item.role,
            date: item.date,
            experience: item.experience, // Assuming certifications reflect experience
            diplome: item.diplome,
            path: item.path,
          }));
          setJobs(jobsList);
        } else {
          console.error('Failed to fetch jobs');
        }
      } catch (error) {
        console.error('Error fetching jobs:', error);
      }
    };

    fetchRoles();
    fetchJobs();
  }, [refresh]);
  
  return (

    <table className="table table-striped">
    <thead style={{ backgroundColor: 'red', color: 'white' }}>
      <tr>
        <th>Role</th>
        <th>Date</th>
        <th>Experience</th>
        <th>Degree</th>
        <th>Job Description</th>
      </tr>
    </thead>
    <tbody>
      {jobs.map((job, index) => {
        // Transformer "media/pdf_job/Consultant Data Management.pdf" en URL correcte
        const downloadUrl = `http://${host}:8081/download/pdf_job/${encodeURIComponent(job.path.split("/").pop())}`;
  
        return (
          <tr key={index}>
            <td>{job.role}</td>
            <td>{job.date}</td>
            <td>{job.experience}</td>
            <td>{job.diplome}</td>
            <td>
              <a 
                href={downloadUrl} 
                download={`${job.role}_description.pdf`} 
                target="_blank" 
                rel="noopener noreferrer"
              >
                Download Description
              </a>
            </td>
          </tr>
        );
      })}
    </tbody>
  </table>
   
  );
}



export default JobComponent;
