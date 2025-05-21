"use client";

import { useEffect, useState } from "react";
import styled from "styled-components";

export default function Dashboard() {
  const [workers, setWorkers] = useState([]);

  useEffect(() => {
    async function fetchWorkers() {
      try {
        const response = await fetch("http://localhost:5001/workers");
        const data = await response.json();
        setWorkers(data);
      } catch (error) {
        console.error("Error fetching workers:", error);
      }
    }

    const interval = setInterval(() => {
      fetchWorkers();
    }, 500);

    return () => clearInterval(interval);
  }, []);

  return (
    <StatsContainer>
      <h1>Dashboard de Recursos</h1>
      {workers.map((worker) => (
        <StatCard key={worker.worker_id}>
          <h2>{worker.worker_id}</h2>
          <StatBar usage={worker.cpu_usage}>
            <span>CPU Usage: {worker.cpu_usage}%</span>
          </StatBar>
          <StatBar usage={worker.memory_usage}>
            <span>Memory Usage: {worker.memory_usage}%</span>
          </StatBar>
          <StatBar usage={worker.disk_usage}>
            <span>Disk Usage: {worker.disk_usage}%</span>
          </StatBar>
          <StatBar usage={worker.network_usage}>
            <span>Network Usage: {worker.network_usage}%</span>
          </StatBar>
          <p>Tasks Processed: {worker.tasks_processed}</p>
        </StatCard>
      ))}
    </StatsContainer>
  );
}

const StatsContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  justify-content: center;
  align-items: center;
  margin-top: 2rem;
  padding: 1rem;

  h1 {
    font-size: 1.8rem;
    color: #cc7832;
    text-align: center;
    width: 100%;
    grid-column: span 4;
  }
`;

const StatCard = styled.div`
  background-color: #3c3f41;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  text-align: center;
  border: 2px solid #555555;

  h2 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: #ffc66d;
  }

  p {
    font-size: 1rem;
    margin: 0.5rem 0;
    color: #a9b7c6;
  }
`;

const StatBar = styled.div`
  background-color: ${({ usage }) =>
    usage < 10
      ? "#4e94ce"
      : usage < 40
      ? "#4caf50"
      : usage < 70
      ? "#ffeb3b"
      : usage < 80
      ? "#ff9800"
      : "#f44336"};
  color: ${({ usage }) => (usage >= 70 ? "#ffffff" : "#000000")};
  padding: 0.5rem;
  border-radius: 5px;
  margin: 0.5rem 0;
  font-size: 0.9rem;
  font-weight: bold;
  text-align: center;
`;
