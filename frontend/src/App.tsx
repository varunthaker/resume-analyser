
import { useState } from 'react'
import './App.css'

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

  const handleSubmit = (event:React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()

    console.log("Form Data", formData);
    



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
