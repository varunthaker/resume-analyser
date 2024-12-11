import DisplayDiv from "./DisplayDiv"
import { APPSTATE } from "./enums"


export interface responseDataType {
    contactDetails:string[]
    education:string[]
    experience:string[]
    projects:string[]
    skills:string[]
    languages:string[]
    certificates:string[]
}

interface ResponsePageProps {
    setAppState:(value:string)=>void
    responseData:responseDataType
}


const ResponsePage = (props:ResponsePageProps) => {

    const {setAppState, responseData} = props

    const {contactDetails, certificates,education, experience, languages, projects, skills } = responseData
    
    return (<div>
    <button  type='button'className= "backBtn" onClick={() => { setAppState(APPSTATE.FORM); }}>{" ⬅ To Form"}</button>
    <div className="card-container">
        <DisplayDiv sectionData = {contactDetails} icon = {"📧"} title= {"Contact Details"}/>  
        <DisplayDiv sectionData = {education} icon = {"📚"} title= {"Education"}/>  
        <DisplayDiv sectionData = {experience} icon = {"💼"} title={"Experience"}/> 
        <DisplayDiv sectionData = {projects} icon = {"📝"} title={"Projects"}/> 
        <DisplayDiv sectionData = {skills} icon = {"🔧"} title={"Skills"}/> 
        <DisplayDiv sectionData = {languages} icon = {"🌐"} title={"Languages"}/> 
        <DisplayDiv sectionData = {certificates} icon = {"📜"} title={"Certificates"}/> 
    </div>
    </div>
    )
}

export default ResponsePage