import { FormEventHandler } from "react";
import { AIMODEL, LANGUAGE } from "../enums";

export interface FormData {
    resumeFile: File | null;
    language: string;
    aiModel: string;
}

interface FormProps {
    handleSubmit:FormEventHandler | undefined;
    formData:FormData;
    setFormData:(value:FormData)=>void

}

const Form = (props:FormProps) => {
    const {handleSubmit, formData, setFormData} = props


    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files) {
          setFormData({ ...formData, resumeFile: event.target.files[0] });
        }
      };
    
    const handleInputChange = (e:React.ChangeEvent<HTMLSelectElement>) => {
        const {name, value} = e.target
        setFormData({...formData, [name]: value})
    
      }
    
    return (<>
     
        <form onSubmit={handleSubmit}>
          
          <div>
            <label htmlFor="resumeFile">Upload your resume (PDF):</label>
            <input type="file" name="resumeFile" id="resumeFile" accept='.pdf' onChange={handleFileChange}/>
          </div>

          <div>
          <label htmlFor="language">Select Language:</label>
          <select name="language" id="language" onChange={handleInputChange}>
          <option value="">-- Select Language --</option>
          <option value={LANGUAGE.EN}>English</option>
          <option value={LANGUAGE.DE}>German</option>
          </select>
          </div>

          <div>
            <label htmlFor="aiModel">Select AI Model:</label>
            <select name="aiModel" id="aiModel" onChange={handleInputChange}>
            <option value="">-- Select AI Model --</option>
          <option value={AIMODEL.OPENAI_GPT}>Chat GPT</option>
          <option value={AIMODEL.GOOGLE_GEMINI}>GEMINI</option>          
            </select>
            <button type="submit">Submit</button>
          </div>

        </form>
      

    </>)
}

export default Form