"use client";

import { useState } from "react";
import styled from "styled-components";

export default function Home() {
  const [showGrayscale, setShowGrayscale] = useState(false);
  const [grayscaleValue, setGrayscaleValue] = useState(0.5);

  const [showPixelate, setShowPixelate] = useState(false);
  const [pixelateValue, setPixelateValue] = useState(10);

  const [loading, setLoading] = useState(false);
  const [processedImages, setProcessedImages] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true); // Mostrar loader

    const formData = new FormData();
    const selectedFilters = Array.from(
      document.querySelectorAll('input[name="filters"]:checked')
    ).map((input) => input.value);

    formData.append("image", document.getElementById("image").files[0]);
    formData.append("filters", JSON.stringify(selectedFilters));

    if (showGrayscale) {
      formData.append("grayscaleIntensity", grayscaleValue);
    }
    if (showPixelate) {
      formData.append("pixelSize", pixelateValue);
    }

    try {
      const response = await fetch("http://localhost:5000/apply-filters", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        setProcessedImages(result.tasks.map((task) => task.output_path)); // Guardar rutas de imágenes procesadas
      } else {
        console.error("Error al enviar las tareas:", response.statusText);
      }
    } catch (error) {
      console.error("Error en la solicitud:", error);
    } finally {
      setLoading(false); // Ocultar loader
    }
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
          <Checkbox>
            <input type="checkbox" name="filters" value="bn" id="filter-bn" />
            <label htmlFor="filter-bn">Blanco y Negro</label>
          </Checkbox>
          <Checkbox>
            <input
              type="checkbox"
              name="filters"
              value="sepia"
              id="filter-sepia"
            />
            <label htmlFor="filter-sepia">Sepia</label>
          </Checkbox>
          <Checkbox>
            <input
              type="checkbox"
              name="filters"
              value="negativo"
              id="filter-negativo"
            />
            <label htmlFor="filter-negativo">Negativo</label>
          </Checkbox>
          <Checkbox>
            <input
              type="checkbox"
              name="filters"
              value="desenfoque"
              id="filter-desenfoque"
            />
            <label htmlFor="filter-desenfoque">Desenfoque</label>
          </Checkbox>
          <Checkbox>
            <input
              type="checkbox"
              name="filters"
              value="bordes"
              id="filter-bordes"
            />
            <label htmlFor="filter-bordes">Bordes</label>
          </Checkbox>
          <Checkbox>
            <input
              type="checkbox"
              name="filters"
              value="grises"
              id="filter-grises"
              onChange={(e) => setShowGrayscale(e.target.checked)}
            />
            <label htmlFor="filter-grises">Grises Ajustable</label>
            {showGrayscale && (
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
          </Checkbox>
          <Checkbox>
            <input
              type="checkbox"
              name="filters"
              value="pixelado"
              id="filter-pixelado"
              onChange={(e) => setShowPixelate(e.target.checked)}
            />
            <label htmlFor="filter-pixelado">Pixelado</label>
            {showPixelate && (
              <SliderContainer>
                <input
                  type="range"
                  name="pixel_size"
                  id="pixel_size"
                  min="1"
                  max="25"
                  step="1"
                  value={pixelateValue}
                  onChange={(e) => setPixelateValue(e.target.value)}
                />
                <span>{pixelateValue}</span>
              </SliderContainer>
            )}
          </Checkbox>
        </FormGroup>

        {/* Botón de Enviar */}
        <Button type="submit">Aplicar Filtros</Button>
      </Form>

      {/* Loader */}
      {loading && <Loader>Procesando...</Loader>}

      {/* Modal de Imágenes Procesadas */}
      {processedImages.length > 0 && (
        <Modal>
          <h2>Imágenes Procesadas</h2>
          <ImageGrid>
            {processedImages.map((image, index) => (
              <div key={index}>
                <img
                  src={`http://localhost:5000/${image}`}
                  alt={`Filtro ${index}`}
                />
                <a href={`http://localhost:5000/${image}`} download>
                  Descargar
                </a>
              </div>
            ))}
          </ImageGrid>
          <Button onClick={() => setProcessedImages([])}>Cerrar</Button>
        </Modal>
      )}
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

const Checkbox = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid #3c3f41;

  input[type="checkbox"] {
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

const Modal = styled.div`
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #2b2b2b;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  z-index: 1000;

  h2 {
    color: #cc7832;
    margin-bottom: 1rem;
  }
`;

const ImageGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;

  img {
    width: 100%;
    border-radius: 8px;
  }

  a {
    display: block;
    margin-top: 0.5rem;
    text-align: center;
    color: #4e94ce;
    text-decoration: none;

    &:hover {
      text-decoration: underline;
    }
  }
`;
