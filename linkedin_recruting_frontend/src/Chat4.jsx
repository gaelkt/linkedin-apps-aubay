import React, { useEffect, useState } from 'react';
import './dashboard.css';
import axios from 'axios';
import DataTable from './DataTable';
import ChartComponent from './ChartComponent2';

const Dashboard = () => {
  const [query, setQuery] = useState('');
  const [queryHistory, setQueryHistory] = useState([]);
  const [requette, setRequette] = useState('');
  const [chart, setChart] = useState('');
  const [data, setData] = useState([]);
  const [dataUrl, setDataUrl] = useState('');
  const [loading, setLoading] = useState(false); // Déclarez l'état loading

  const handleSendQuery = async () => {
    if (!query.trim()) {
      alert('Veuillez saisir une requête avant d’envoyer.');
      return;
    }
  
    if (!requette) {
      alert('Veuillez sélectionner le type de requête.');
      return;
    }
  
    const newRequestBody = { query: query };
  
    try {
      setLoading(true); // Démarre le chargement
      const encodedQuery = encodeURIComponent(newRequestBody.query);
      console.log("la requette non encode est  ", newRequestBody.query);
      console.log("la requette  encode est ", encodedQuery);
  
      const response = await axios.get(`http://localhost:8081/sql?query=${newRequestBody.query}`);
      const point = response.data;
      setData(point);
      setDataUrl(`http://localhost:8081/sql?query=${encodedQuery}`);
  
      // Après avoir reçu la réponse de l'API, ajoutez à l'historique
      if (requette === 'table') {
        const currentQuery = {
          type: 'table',
          query: newRequestBody.query,
          data: point, // Utilisation de la réponse directement
        };
        setQueryHistory((prevHistory) => [...prevHistory, currentQuery]);
      } else if (requette === 'chart') {
        const currentQuery = {
          type: 'chart',
          query: newRequestBody.query,
          chartType: chart,
          dataUrl: `http://localhost:8081/sql?query=${encodedQuery}`,
        };
        setQueryHistory((prevHistory) => [...prevHistory, currentQuery]);
      }
  
      setQuery(''); // Reset de la requête
    } catch (error) {
      console.error('Erreur lors de l’envoi de la requête :', error);
    } finally {
      setLoading(false); // Arrête le chargement une fois l'appel terminé
    }
  };
  

  return (
    <div className="main-content">
      <div className="welcome-message">
        {queryHistory.map((request, index) =>
          request.type === 'table' ? (
            <DataTable key={index} query={request.query} data={request.data} />
          ) : (
            <ChartComponent
              key={index}
              chartType={request.chartType}
              dataUrl={request.dataUrl}
              query={request.query}
            />
          )
        )}
      </div>

      <div className="query-box">
        <select
          className="query-select"
          value={requette}
          onChange={(e) => setRequette(e.target.value)}
        >
          <option value="">Type de requête</option>
          <option value="chart">Chart</option>
          <option value="table">Table</option>
        </select>
        {requette === 'chart' && (
          <select
            className="chart-select"
            value={chart}
            onChange={(e) => setChart(e.target.value)}
          >
            <option value="">Type de graphique</option>
            <option value="bar">Bar</option>
            <option value="pie">Pie</option>
            <option value="doughnut">Doughnut</option>
            <option value="radar">Radar</option>
          </select>
        )}
        <input
          type="text"
          className="query-input"
          placeholder="Tapez votre requête ici..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button className="send-button" onClick={handleSendQuery} disabled={loading}>
          <img src="/send-icon.png" alt="Envoyer" className="icon" />
        </button>
      </div>

      {/* Affichage de la barre de progression pendant le chargement */}
      {loading && (
        <div className="progress-bar">
          <div className="progress-bar-fill"></div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
