
import { useState } from 'react';
import './App.css'
import LoadingPage from './LoadingPage';
import ResponsePage from './ResponsePage';
import Form from './assets/Form';
import { APPSTATE } from './enums';
import axios from 'axios';

function App() {

  const[appState, setAppState] = useState<string>(APPSTATE.FORM)
  const [formData, setFormData] = useState({
    resumeFile:null as File | null,
    language:'',
    aiModel:''
  })
  const[responseData, setResponseData] =useState<any>()

  const handleSubmit = async (event:React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!formData.resumeFile || !formData.language || !formData.aiModel) {
      alert("Please fill out all fields and upload a file.");
      return;
    }
    setAppState(APPSTATE.LOADING)
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
       
      if(response.data) {
        console.log("Server Response:", response.data);
        setResponseData(response.data)
        setAppState(APPSTATE.RESPONSE)
        resetFormData()
      }

    } catch (error) {

      if (axios.isAxiosError(error) && error.response) {
        console.error("Error Response:", error.response);
        alert(`Error: ${error.response.data.error || 'Failed to submit resume.'}`);
        
      } else {
        console.error("Network Error:", error);
        alert("Network error. Please check your connection.");
        
      }
      resetFormData()
      setAppState(APPSTATE.FORM)
    }

  }
  const resetFormData = () => {
  setFormData({resumeFile: null,
  language: '',
  aiModel: '',})

  }

  return (
    <>
      <h1>Resume Analyser</h1>
      {appState == APPSTATE.FORM && <Form handleSubmit = {handleSubmit} formData= {formData} setFormData= {setFormData}/>}
      {appState == APPSTATE.LOADING && <LoadingPage/> }
      {appState == APPSTATE.RESPONSE && <ResponsePage setAppState = {setAppState} responseData={responseData}/> }
            
      
    </>
  )
}

export default App
