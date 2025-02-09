import React, { useEffect, useRef } from 'react';
import {
  Chart,
  BarController,
  PieController,
  DoughnutController,
  RadarController,
  ArcElement,
  LineElement,
  BarElement,
  PointElement,
  RadialLinearScale,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';

// Register all necessary components
Chart.register(
  BarController,
  PieController,
  DoughnutController,
  RadarController,
  ArcElement,
  LineElement,
  BarElement,
  PointElement,
  RadialLinearScale,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
  Filler
);

const GenericChart = ({ type, data, options }) => {
  const chartRef = useRef(null);
  const chartInstanceRef = useRef(null);

  useEffect(() => {
    if (chartInstanceRef.current) {
      chartInstanceRef.current.destroy();
    }

    const ctx = chartRef.current.getContext('2d');
    chartInstanceRef.current = new Chart(ctx, {
      type,
      data,
      options,
    });

    return () => {
      if (chartInstanceRef.current) {
        chartInstanceRef.current.destroy();
      }
    };
  }, [type, data, options]);

  return <canvas ref={chartRef}></canvas>;
};

export default GenericChart;
