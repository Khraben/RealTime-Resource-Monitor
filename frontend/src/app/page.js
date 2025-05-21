"use client";

import styled from "styled-components";

export default function Home() {
  return (
    <Form>
      <h1>Asignación de Tareas</h1>
      <p>Aquí puedes asignar tareas al sistema distribuido de nodos.</p>
      <label htmlFor="task">Tarea:</label>
      <input type="text" id="task" placeholder="Ingresar tarea..." />
      <button>Asignar Tarea</button>
    </Form>
  );
}

const Form = styled.form`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;

  h1 {
    font-size: 1.8rem;
    color: #cc7832;
  }

  p {
    font-size: 1rem;
    color: #a9b7c6;
    text-align: center;
    max-width: 400px;
  }

  label {
    font-size: 1rem;
    color: #a9b7c6;
  }

  input {
    padding: 0.5rem;
    font-size: 1rem;
    border: 1px solid #555555;
    border-radius: 5px;
    background-color: #3c3f41;
    color: #a9b7c6;
    width: 100%;
    max-width: 300px;
  }

  button {
    padding: 0.7rem 1.5rem;
    font-size: 1rem;
    border: none;
    border-radius: 5px;
    background-color: #4e94ce;
    color: #ffffff;
    cursor: pointer;
    transition: background-color 0.3s;

    &:hover {
      background-color: #6ca6d8;
    }
  }
`;
