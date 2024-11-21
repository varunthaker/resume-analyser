
import { useState } from 'react'
import './App.css'
import axios from 'axios';

function App() {

  const [formData, setFormData] = useState({
    resumeFile:null as File | null,
    language:'',
    aiModel:''
  })

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFormData({ ...formData, resumeFile: event.target.files[0] });
    }
  };

  const handleInputChange = (e:React.ChangeEvent<HTMLSelectElement>) => {

    const {name, value} = e.target


    setFormData({...formData, [name]: value})

  }

  const resetFormData = () => {
    (document.getElementById('resumeFile') as HTMLInputElement).value = '';
    (document.getElementById('language') as HTMLSelectElement).value = '';
    (document.getElementById('aiModel') as HTMLSelectElement).value = '';

  }
  const handleSubmit = async (event:React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()

    console.log("Form Data", formData);

    if (!formData.resumeFile || !formData.language || !formData.aiModel) {
      alert("Please fill out all fields and upload a file.");
      return;
    }
    
    const formPayload = new FormData()
    formPayload.append('resumeFile', formData.resumeFile);
    formPayload.append('language', formData.language);
    formPayload.append('aiModel', formData.aiModel);
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/upload/', formPayload, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log("Server Response:", response.data);
      alert("Resume submitted successfully!");
      resetFormData()
    } catch (error) {

      if (axios.isAxiosError(error) && error.response) {
        console.error("Error Response:", error.response);
        alert(`Error: ${error.response.data.error || 'Failed to submit resume.'}`);
        
      } else {
        console.error("Network Error:", error);
        alert("Network error. Please check your connection.");
        
      }
      resetFormData()
    }

  }

  return (
    <>
      <h1>Resume Analyser</h1>
      <div>
        <form onSubmit={handleSubmit}>
          
          <div>
            <label htmlFor="resumeFile">Upload your resume (PDF):</label>
            <input type="file" name="resumeFile" id="resumeFile" accept='.pdf' onChange={handleFileChange}/>
          </div>

          <div>
          <label htmlFor="language">Select Language:</label>
          <select name="language" id="language" onChange={handleInputChange}>
          <option value="">-- Select Language --</option>
          <option value="en">English</option>
          <option value="de">German</option>
          </select>
          </div>

          <div>
            <label htmlFor="aiModel">Select AI Model:</label>
            <select name="aiModel" id="aiModel" onChange={handleInputChange}>
            <option value="">-- Select AI Model --</option>
          <option value="gpt-3">GPT-3</option>
          <option value="claude">Claude</option>
          <option value="gemini">GEMINI</option>
            </select>
            <button type="submit">Submit</button>
          </div>

        </form>
      </div>

    </>
  )
}

export default App
