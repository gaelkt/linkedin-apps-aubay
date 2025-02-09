import React, { useEffect, useState } from "react";
import axios from "axios";
import './DataTable.css';

const DataTable = ({ query, data }) => {

    

    if (!data || data.length === 0) {
        return <p>Aucune donnée trouvée pour la requête : {query}</p>;
      }


  return (
    <div className="data-table-container">

      <div className="query">
        
          <div className="query2">
            {query}
          </div>
       
      </div>

      <div className="data">
        
        <div className="data2">
        <table>
        <thead>
          <tr>
            {data.length > 0 &&
              Object.keys(data[0]).map((key) => <th key={key}>{key}</th>)}
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <tr key={index}>
              {Object.values(row).map((value, idx) => (
                <td key={idx}>{value}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
          
        </div>
     
    </div>

     
    </div>
  );
};

export default DataTable;
