"use client";

import { useState } from "react";
import styled from "styled-components";

export default function Home() {
  const [selectedFilters, setSelectedFilters] = useState([]);
  const [grayscaleValue, setGrayscaleValue] = useState(0.5);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const formData = new FormData();
    formData.append("image", document.getElementById("image").files[0]);
    formData.append("filters", JSON.stringify(selectedFilters));
    if (selectedFilters.includes("grises")) {
      formData.append("grayscaleIntensity", grayscaleValue);
    }

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/apply-filters`,
        {
          method: "POST",
          body: formData,
        }
      );
      if (response.ok) {
        const result = await response.json();
        result.tasks.forEach((task) => {
          const newTab = window.open(
            `${process.env.NEXT_PUBLIC_API_URL}/${
              task.output_path
            }?t=${Date.now()}`,
            "_blank"
          );
          if (newTab) {
            newTab.focus();
          }
        });
      } else {
        console.error("Error al enviar las tareas:", response.statusText);
      }
    } catch (error) {
      console.error("Error en la solicitud:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (filter) => {
    setSelectedFilters((prevFilters) => {
      if (prevFilters.includes(filter)) {
        return prevFilters.filter((f) => f !== filter);
      } else {
        return [...prevFilters, filter];
      }
    });
  };

  return (
    <Container>
      <h1>Aplicación de Filtros</h1>
      <Form onSubmit={handleSubmit} encType="multipart/form-data">
        {/* Subir Imagen */}
        <FormGroup>
          <Label htmlFor="image">Subir Imagen:</Label>
          <input
            type="file"
            name="image"
            id="image"
            accept="image/*"
            required
          />
        </FormGroup>

        {/* Selección de Filtros */}
        <FormGroup>
          <Label>Filtros:</Label>
          <Radio>
            <input
              type="checkbox"
              name="filters"
              value="bn"
              id="filter-bn"
              checked={selectedFilters.includes("bn")}
              onChange={() => handleFilterChange("bn")}
            />
            <label htmlFor="filter-bn">Blanco y Negro</label>
          </Radio>
          <Radio>
            <input
              type="checkbox"
              name="filters"
              value="negativo"
              id="filter-negativo"
              checked={selectedFilters.includes("negativo")}
              onChange={() => handleFilterChange("negativo")}
            />
            <label htmlFor="filter-negativo">Negativo</label>
          </Radio>
          <Radio>
            <input
              type="checkbox"
              name="filters"
              value="grises"
              id="filter-grises"
              checked={selectedFilters.includes("grises")}
              onChange={() => handleFilterChange("grises")}
            />
            <label htmlFor="filter-grises">Grises Ajustable</label>
            {selectedFilters.includes("grises") && (
              <SliderContainer>
                <input
                  type="range"
                  name="intensity"
                  id="intensity"
                  min="0.1"
                  max="0.9"
                  step="0.1"
                  value={grayscaleValue}
                  onChange={(e) => setGrayscaleValue(e.target.value)}
                />
                <span>{grayscaleValue}</span>
              </SliderContainer>
            )}
          </Radio>
        </FormGroup>

        {/* Botón de Enviar */}
        <Button type="submit">Aplicar Filtros</Button>
      </Form>

      {/* Loader */}
      {loading && <Loader>Procesando...</Loader>}
    </Container>
  );
}

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 2rem;
  padding: 1rem;
  background-color: #2b2b2b;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);

  h1 {
    font-size: 1.8rem;
    color: #cc7832;
    margin-bottom: 1rem;
  }
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  width: 100%;
  max-width: 400px;
`;

const FormGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;

  input[type="file"] {
    width: 100%;
  }
`;

const Label = styled.label`
  font-size: 1rem;
  color: #ff5647;
`;

const Radio = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid #3c3f41;

  input[type="radio"] {
    accent-color: #4e94ce;
  }

  label {
    font-size: 1rem;
    color: #a9b7c6;
  }
`;

const SliderContainer = styled.div`
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 1rem;
  margin-top: 0.5rem;

  input[type="range"] {
    flex: 1;
    accent-color: #4e94ce;
  }

  span {
    font-size: 1rem;
    color: #ffc66d;
  }
`;

const Button = styled.button`
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
`;

const Loader = styled.div`
  margin-top: 2rem;
  font-size: 1.5rem;
  color: #ffffff;
`;
