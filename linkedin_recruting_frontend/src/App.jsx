import { useState,useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import Dashboard from './Chat';
const host = "localhost";

function App() {
  
  const [activeTab, setActiveTab] = useState('settings');
  const [role, setRole] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [filteredData, setFilteredData] = useState([]);
  const [rolesList, setRolesList] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [email, setEmail] = useState('');
  const [emailApp, setEmailApp] = useState('');
  const [emailJob, setEmailJob] = useState('');
  const [selectedRoles, setSelectedRoles] = useState([]);
  const [roles, setRoles] = useState([]);
  const [pdfs, setPdfs] = useState([]);
  const [selectedJobs, setSelectedJobs] = useState([]);
  const [selectedApplication, setSelectedApplication] = useState([]);
  const [loadingJobs, setLoadingJobs] = useState(false); // Déclarez l'état loading
  const [loadingApps, setLoadingApps] = useState(false); // Déclarez l'état loading



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
  }, []);

  const handleInitializeDB = async () => {
    try {
      const response = await fetch(`http://${host}:8081/initialization/`);

      if (response.ok) {
        alert('Base de données initialisée avec succès!');
      } else {
        alert('Erreur lors de l\'initialisation de la base de données.');
      }
    } catch (error) {
      console.error('Erreur:', error);
      alert(error);
    }
  };
  const handleJobUpload = (event) => {

    const files = Array.from(event.target.files); // Convertit FileList en tableau
    setSelectedJobs(files);
    
    
  };
  const handleApplicationUpload = (event) => {

    const files = Array.from(event.target.files); // Convertit FileList en tableau
    setSelectedApplication(files);
    
    
  };

  const processApplication = async () => {

    if (selectedApplication.length === 0) {
      alert("Veuillez sélectionner au moins un fichier.");
      return;
    }
  
    const formData = new FormData();
    selectedApplication.forEach((file) => {
      formData.append("files", file); // L'API attend "files"
    });
  
    try {

      setLoadingApps(true);
      const response = await fetch(`http://${host}:8081/applications/?recipient_email=${emailApp}`, {
        method: "POST",
        headers: {
          accept: "application/json", // L'API attend ce header
          // ⚠️ Ne pas ajouter 'Content-Type': 'multipart/form-data'
          // Fetch l'ajoute automatiquement avec le bon boundary
        },
        body: formData,
      });
  
      const result = await response.json(); // Convertir la réponse en JSON
  
      if (response.ok) {
        alert(`Applications succcessfully added !`);
        
        if (result["number of failed"] > 0) {
          console.warn("Apps échoués :");
          console.warn("Erreurs :");
        }
      } else {
        alert("❌ Une erreur est survenue lors du traitement des Applications.");
        console.error("Réponse API :", result);
      }
    } catch (error) {
      console.error("Erreur lors de la requête :", error);
      alert("❌ Une erreur réseau est survenue.");
    }finally {
      setLoadingApps(false);
    }

    
  };


  const processJobs = async () => {
    if (selectedJobs.length === 0) {
      alert("Veuillez sélectionner au moins un fichier.");
      return;
    }
  
    const formData = new FormData();
    selectedJobs.forEach((file) => {
      formData.append("files", file); // L'API attend "files"
    });
  
    try {
      setLoadingJobs(true);
      const response = await fetch(`http://${host}:8081/jobs/?recipient_email=${emailJob}`, {
        method: "POST",
        headers: {
          accept: "application/json", // L'API attend ce header
         
        },
        body: formData,
      });
  
      const result = await response.json(); // Convertir la réponse en JSON
  
      if (response.ok) {
        alert(`Jobs succcessfully added !`);
        
        if (result["number of failed"] > 0) {
          console.warn("Jobs échoués :");
          console.warn("Erreurs :");
        }
      } else {
        alert("❌ Une erreur est survenue lors du traitement des jobs.");
        console.error("Réponse API :", result);
      }
    } catch (error) {
      console.error("Erreur lors de la requête :", error);
      alert("❌ Une erreur réseau est survenue.");
    }finally{
      setLoadingJobs(false);
    }
  };
  


  const handleFilter = async () => {
    try {
      const url = `http://${host}:8081/view_applications/?begin_date=${startDate}&end_date=${endDate}&roles=${encodeURIComponent(role)}`;
      const response = await fetch(url);

      if (response.ok) {
        const data = await response.json();
        const results = data[role] || [];
        setFilteredData(results);
      } else {
        alert('Erreur lors de la récupération des données.');
      }
    } catch (error) {
      console.error('Erreur:', error);
      alert('Une erreur est survenue lors de la récupération des données.');
    }
  };

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handleEmailJobChange = (e) => {
    setEmailJob(e.target.value);
  };

  const handleEmailAppChange = (e) => {
    setEmailApp(e.target.value);
  };

  const handleRoleSelection = (role) => {
    setSelectedRoles((prevRoles) =>
      prevRoles.includes(role)
        ? prevRoles.filter((r) => r !== role)
        : [...prevRoles, role]
    );
  };

  const handleSendReport = async () => {
    if (!email || selectedRoles.length === 0 || !startDate || !endDate) {
      alert('Veuillez remplir tous les champs.');
      return;
    }

    const url = `http://${host}:8081/report?begin_date=${startDate}&end_date=${endDate}&recipient_email=${email}${selectedRoles.map(role => `&roles=${encodeURIComponent(role)}`).join('')}`;

    try {
      const response = await fetch(url);

      if (response.ok) {
        alert('Email envoyé avec succès!');
      } else {
        alert('Erreur lors de l\'envoi de l\'email.');
      }
    } catch (error) {
      console.error('Erreur:', error);
      alert('Une erreur est survenue.');
    }
  };


  return (


    <div className="container mt-3">
      <ul className="nav nav-tabs mb-4 fixed-header" style={{ borderBottom: '2px solid red', marginTop: '5px' }}>
         
        <li className="nav-item">
          <button 
            className={`nav-link ${activeTab === 'settings' ? 'active' : ''}`} 
            style={{ color: activeTab === 'settings' ? 'white' : 'red', backgroundColor: activeTab === 'settings' ? 'red' : 'white' }}
            onClick={() => setActiveTab('settings')}
          >
            Settings
          </button>
        </li>
        <li className="nav-item">
          <button 
            className={`nav-link ${activeTab === 'view-job' ? 'active' : ''}`} 
            style={{ color: activeTab === 'view-job' ? 'white' : 'red', backgroundColor: activeTab === 'view-job' ? 'red' : 'white' }}
            onClick={() => setActiveTab('view-job')}
          >
            Open Positions
          </button>
        </li>
        
        <li className="nav-item">
          <button 
            className={`nav-link ${activeTab === 'view-application' ? 'active' : ''}`} 
            style={{ color: activeTab === 'view-application' ? 'white' : 'red', backgroundColor: activeTab === 'view-application' ? 'red' : 'white' }}
            onClick={() => setActiveTab('view-application')}
          >
            View Applications
          </button>
        </li>
        <li className="nav-item">
          <button 
            className={`nav-link ${activeTab === 'process-job' ? 'active' : ''}`} 
            style={{ color: activeTab === 'process-job' ? 'white' : 'red', backgroundColor: activeTab === 'process-job' ? 'red' : 'white' }}
            onClick={() => setActiveTab('process-job')}
          >
            Process Jobs
          </button>
        </li>
        <li className="nav-item">
          <button 
            className={`nav-link ${activeTab === 'process-apps' ? 'active' : ''}`} 
            style={{ color: activeTab === 'process-apps' ? 'white' : 'red', backgroundColor: activeTab === 'process-apps' ? 'red' : 'white' }}
            onClick={() => setActiveTab('process-apps')}
          >
            Process Applications
          </button>
        </li>
        
        <li className="nav-item">
          <button 
            className={`nav-link ${activeTab === 'chat' ? 'active' : ''}`} 
            style={{ color: activeTab === 'chat' ? 'white' : 'red', backgroundColor: activeTab === 'chat' ? 'red' : 'white' }}
            onClick={() => setActiveTab('chat')}
          >
            Chat
          </button>
        </li>
        <li className="nav-item">
          <button 
            className={`nav-link ${activeTab === 'send-email' ? 'active' : ''}`} 
            style={{ color: activeTab === 'send-email' ? 'white' : 'red', backgroundColor: activeTab === 'send-email' ? 'red' : 'white' }}
            onClick={() => setActiveTab('send-email')}
          >
            Send Email
          </button>
        </li>

        <li className="nav-item ml-auto">
        <img src="/logo.png" alt="Logo" style={{ height: '40px' }} />
    </li>

       
      </ul>


      <div className="tab-content content">
        {activeTab === 'settings' && (
          <div>
            <h3></h3>
            <button onClick={handleInitializeDB} className="btn btn-primary mb-3" style={{ backgroundColor: 'red', borderColor: 'red' }}>
              Initialise DB
            </button>
           
          </div>
        )}

        {activeTab === 'process-job' && <div>
          <h3></h3>

          <div className="mb-3">
             <label htmlFor="job" className="form-label">Recipient Email</label>
             <input type="email" id="job" className="form-control" value={emailJob} onChange={handleEmailJobChange}/>
         </div>
          <ul>
        {selectedJobs.map((file, index) => (
          <li key={index}>{file.name}</li>
        ))}
      </ul>

      {/* Input pour le téléversement multiple */}
      
      <input
        type="file"
        multiple
        className="form-control mb-3"
        onChange={handleJobUpload}
      />
   
          <button onClick={processJobs} className="btn btn-primary mb-3" style={{ backgroundColor: 'red', borderColor: 'red' }} disabled={loadingJobs}>
              Process Jobs
            </button>

            {loadingJobs && (
        <div className="progress-bar">
          <div className="progress-bar-fill"></div>
        </div>
      )}

          </div>}

        {activeTab === 'view-application' && (
          <div>
            <h3></h3>
            <div className="mb-3">
              <label htmlFor="role" className="form-label">Select Role</label>
              <select 
                id="role" 
                className="form-select" 
                value={role} 
                onChange={(e) => setRole(e.target.value)}
              >
                <option value="">Select a role</option>
                {rolesList.map((r, index) => (
                  <option key={index} value={r}>{r}</option>
                ))}
              </select>
            </div>

            <div className="mb-3">
              <label htmlFor="start-date" className="form-label">Start Date</label>
              <input 
                type="date" 
                id="start-date" 
                className="form-control" 
                value={startDate} 
                onChange={(e) => setStartDate(e.target.value)}
              />
            </div>

            <div className="mb-3">
              <label htmlFor="end-date" className="form-label">End Date</label>
              <input 
                type="date" 
                id="end-date" 
                className="form-control" 
                value={endDate} 
                onChange={(e) => setEndDate(e.target.value)}
              />
            </div>

            <button onClick={handleFilter} className="btn btn-primary mb-4" style={{ backgroundColor: 'red', borderColor: 'red' }}>
              Filter
            </button>

            <table className="table table-striped">
              <thead style={{ backgroundColor: 'red', color: 'white' }}>
                <tr>
                  <th>Name</th>
                  <th>Date</th>
                  <th>Score</th>
                  <th>Experience</th>
                  <th>Degree</th>
                  <th>Hard Skills</th>
                  <th>Resume</th>
                  
                </tr>
              </thead>
              <tbody>

              {filteredData.map((item, index) => {
      // Transformer "media/pdf_job/Consultant Data Management.pdf" en URL correcte
      const downloadUrl = `http://${host}:8081/download/resume/${encodeURIComponent(item.path.split("/").pop())}`;

      return (
        <tr key={index}>
          <td>{item.name}</td>
          <td>{item.date}</td>
          <td>{item.score}</td>
          <td>{item.experience}</td>
          <td>{item.diplome}</td>
          <td style={{ fontSize: "13px" }}>{item.hard_skills}</td>
          <td>
            <a 
              href={downloadUrl} 
              download={`${item.name}_resume.pdf`} 
              target="_blank" 
              rel="noopener noreferrer"
            >
              Download Resume
            </a>
          </td>
        </tr>
      );
    })}
                
              </tbody>
            </table>
          </div>
        )}

        {activeTab === 'view-job' && <div>
            <h3></h3>
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
          </div>}

        {activeTab === 'process-apps' && <div>
          <h3></h3>
          <div className="mb-3">
               <label htmlFor="apps" className="form-label">Recipient Email</label>
               <input type="email" id="apps" className="form-control" value={emailApp} onChange={handleEmailAppChange} />
          </div>
          <ul>
        {selectedApplication.map((file, index) => (
          <li key={index}>{file.name}</li>
        ))}
      </ul>

      {/* Input pour le téléversement multiple */}
      <input
        type="file"
        multiple
        className="form-control mb-3"
        onChange={handleApplicationUpload}
      />
          <button onClick={processApplication} className="btn btn-primary mb-3" style={{ backgroundColor: 'red', borderColor: 'red' }} disabled={loadingApps}>
              Process Application
            </button>
            {loadingApps && (
        <div className="progress-bar">
          <div className="progress-bar-fill"></div>
        </div>
      )}
          </div>}

          {activeTab === 'send-email' && (
  <div>
    <h3></h3>

    <div className="mb-3">
      <label className="form-label">Select Roles</label>
      <select
        className="form-select"
        multiple
        value={selectedRoles}
        onChange={(e) => {
          const selectedOptions = Array.from(e.target.selectedOptions, (option) => option.value);
          setSelectedRoles([...selectedRoles, ...selectedOptions.filter(option => !selectedRoles.includes(option))]);
        }}
      >
        {roles.map((role, index) => (
          <option key={index} value={role}>{role}</option>
        ))}
      </select>
    </div>

    <div className="mb-3 d-flex gap-3">
      <div className="w-50">
        <label htmlFor="start-date" className="form-label">Start Date</label>
        <input
          type="date"
          id="start-date"
          className="form-control"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
        />
      </div>
      <div className="w-50">
        <label htmlFor="end-date" className="form-label">End Date</label>
        <input
          type="date"
          id="end-date"
          className="form-control"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
        />
      </div>
    </div>

    <div className="mb-3">
      <label htmlFor="email" className="form-label">Recipient Email</label>
      <input
        type="email"
        id="email"
        className="form-control"
        value={email}
        onChange={handleEmailChange}
      />
    </div>

    <button onClick={handleSendReport} className="btn btn-primary mb-4" style={{ backgroundColor: 'red', borderColor: 'red' }}>
      Send Report
    </button>
  </div>
)}



        {activeTab === 'chat' && <Dashboard/>}

      </div>

    
    </div>

  );
}

export default App
