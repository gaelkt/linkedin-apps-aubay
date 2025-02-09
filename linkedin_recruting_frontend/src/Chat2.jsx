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
    
  
    const handleSendQuery = async () => {
      if (!query.trim()) {
        alert('Veuillez saisir une requête avant d’envoyer.');
        return;
      }
  
      if (!requette) {
        alert('Veuillez sélectionner le type de requête.');
        return;
      }
  
      const newRequestBody = {
   
        query: query,
        
      };
  
      try {
        const encodedQuery = encodeURIComponent(newRequestBody.query);
        console.log("la requette non encode est  ",newRequestBody.query)
        console.log("la requette  encode est ",encodedQuery)
        const response = await axios.get(`http://localhost:8081/sql?query=${newRequestBody.query}`);
        const point = response.data;
        setData(point);
        setDataUrl(`http://localhost:8081/sql?query=${encodedQuery}`)
  
        if (requette === 'table') {
          const currentQuery = {
            type: 'table',
            query: newRequestBody.query,
            data: data,
          };
          setQueryHistory((prevHistory) => [...prevHistory, currentQuery]);
        } else if (requette === 'chart') {
            console.log("======debut======");
            console.log("hi ",dataUrl);
            console.log("======fin======");
         /* const pathResponse = await axios.post('http://localhost:8000/getXMLFile/', data);
          const xmlFilePath = `/data/${pathResponse.data.filename}`;*/
  
          const currentQuery = {
            type: 'chart',
            query: newRequestBody.query,
            chartType: chart,
            dataUrl: dataUrl,
          };
          console.log(currentQuery.dataUrl)
          setQueryHistory((prevHistory) => [...prevHistory, currentQuery]);
        }
  
        setQuery('');
      } catch (error) {
        console.error('Erreur lors de l’envoi de la requête :', error);
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
            <button className="send-button" onClick={handleSendQuery} disabled={loading} >
              <img src="/send-icon.png" alt="Envoyer" className="icon" />
            </button>
          </div>
          
        </div>
  
    );
  };
  
  export default Dashboard;
  