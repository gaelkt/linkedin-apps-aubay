import React, { useEffect, useState, useRef } from 'react';
import './dashboard2.css';
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
  const [loading, setLoading] = useState(false);
  const chatContainerRef = useRef(null);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTo({ top: chatContainerRef.current.scrollHeight, behavior: 'smooth' });
    }
  }, [queryHistory]);

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
      setLoading(true);
      const encodedQuery = encodeURIComponent(newRequestBody.query);
      const response = await axios.get(`http://localhost:8081/sql?query=${encodedQuery}`);
      const point = response.data;
      setData(point);
      setDataUrl(`http://localhost:8081/sql?query=${encodedQuery}`);

      const currentQuery = {
        type: requette,
        query: newRequestBody.query,
        data: requette === 'table' ? point : null,
        chartType: requette === 'chart' ? chart : null,
        dataUrl: requette === 'chart' ? `http://localhost:8081/sql?query=${encodedQuery}` : null,
      };

      setQueryHistory((prevHistory) => [...prevHistory, currentQuery]);
      setQuery('');
    } catch (error) {
      console.error('Erreur lors de l’envoi de la requête :', error);
    } finally {
      setLoading(false);
      setTimeout(() => {
        if (chatContainerRef.current) {
          chatContainerRef.current.scrollTo({ top: chatContainerRef.current.scrollHeight, behavior: 'smooth' });
        }
      }, 100);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-messages" ref={chatContainerRef}>
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
        <select className="query-select" value={requette} onChange={(e) => setRequette(e.target.value)}>
          <option value="">Type de requête</option>
          <option value="chart">Chart</option>
          <option value="table">Table</option>
        </select>
        {requette === 'chart' && (
          <select className="chart-select" value={chart} onChange={(e) => setChart(e.target.value)}>
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
    </div>
  );
};

export default Dashboard;
