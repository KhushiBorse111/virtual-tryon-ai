import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [selectedClothing, setSelectedClothing] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedImage(file);
    }
  };

  const handleClothingSelection = (clothingId) => {
    setSelectedClothing(clothingId);
  };

  const callTryOnAPI = async () => {
    if (!selectedImage) {
      alert('Please select an image first');
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('file', selectedImage);

    try {
      const response = await axios.post('/api/upload-image/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResult(response.data);
    } catch (error) {
      console.error('Error uploading image:', error);
      alert('Error uploading image');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="virtual-tryon">
      <header className="header">
        <h1>Virtual Try-On</h1>
      </header>
      
      <main>
        <section>
          <h2>Upload Your Photo</h2>
          <input 
            type="file" 
            id="photo-upload" 
            accept="image/*" 
            onChange={handleImageUpload}
          />
          <button className="button" onClick={callTryOnAPI} disabled={loading}>
            {loading ? 'Processing...' : 'Upload & Try On'}
          </button>
        </section>

        {selectedImage && (
          <section>
            <h2>Selected Image Preview</h2>
            <div className="img-container">
              <img 
                src={URL.createObjectURL(selectedImage)} 
                alt="Preview" 
              />
            </div>
          </section>
        )}

        {result && (
          <section>
            <h2>Result</h2>
            <div className="img-container">
              <p>{result.filename}</p>
            </div>
          </section>
        )}
      </main>

      <footer>
        <p>&copy; 2026 Virtual Try-On Interface</p>
      </footer>
    </div>
  );
}

export default App;
