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

    const testResponseData = {
        contactDetails: [
          "contact1@example.com is the primary contact email for customer service inquiries, customer support, and all account-related communication needs.",
          "contact2@example.com serves as the secondary email for communication, particularly for technical issues, billing questions, and internal operations support."
        ],
        education: [
          "Bachelor of Science in Computer Science from XYZ University, which included courses in algorithms, data structures, software engineering, and systems design.",
          "Master of Business Administration from ABC University, focusing on leadership, strategic management, organizational behavior, and advanced financial analysis skills."
        ],
        experience: [
          "Software Engineer at XYZ Corp, responsible for developing and maintaining scalable web applications, collaborating with cross-functional teams to deliver high-quality software solutions.",
          "Team Lead at ABC Inc, overseeing a team of software developers, managing project timelines, ensuring quality assurance processes are followed, and driving innovation in product development."
        ],
        projects: [
          "E-commerce Platform Development, a large-scale project aimed at creating a user-friendly, secure, and responsive online store for a wide variety of retail products and services.",
          "Mobile App for Social Networking, designed to allow users to connect, share updates, and create groups, with features such as real-time messaging, video calls, and multimedia sharing."
        ],
        skills: [
          "JavaScript, a versatile programming language widely used for building interactive web applications, and React, a popular JavaScript library for building user interfaces efficiently with reusable components.",
          "React, which enhances the development of complex web applications through its component-based architecture, and JavaScript, which powers both the front-end and server-side functionality of web applications."
        ],
        languages: [
          "English, a widely spoken language, used in professional and academic contexts for communication, documentation, and international collaboration across various industries.",
          "Spanish, spoken by millions worldwide, enabling communication with Spanish-speaking individuals and communities, offering a competitive edge in business and cultural engagement."
        ],
        certificates: [
          "AWS Certified Solutions Architect, which demonstrates expertise in designing and deploying scalable, highly available, and fault-tolerant systems on Amazon Web Services cloud infrastructure.",
          "Certified Scrum Master, which signifies proficiency in agile project management and leading scrum teams to successfully deliver complex projects on time and within scope."
        ]
      };
      

    // console.log("responseData == ", responseData);
    

    return (

        
     <>
  <div className="card-container">
    <div className="card">
      <div className="card-header">
        <span className="card-icon">🎓</span>
        <h3>Contact Details</h3>
      </div>
      <ul className="card-content">
        {testResponseData?.contactDetails?.map((data, key) => (
          <li key={key}>{data}</li>
        ))}
      </ul>
    </div>

    <div className="card">
      <div className="card-header">
        <span className="card-icon">🎓</span>
        <h3>Education</h3>
      </div>
      <ul className="card-content">
        {testResponseData?.education?.map((data, key) => (
          <li key={key}>{data}</li>
        ))}
      </ul>
    </div>

    <div className="card">
      <div className="card-header">
        <span className="card-icon">💼</span>
        <h3>Experience</h3>
      </div>
      <ul className="card-content">
        {testResponseData?.experience?.map((data, key) => (
          <li key={key}>{data}</li>
        ))}
      </ul>
    </div>

    <div className="card">
      <div className="card-header">
        <span className="card-icon">🛠️</span>
        <h3>Projects</h3>
      </div>
      <ul className="card-content">
        {testResponseData?.projects?.map((data, key) => (
          <li key={key}>{data}</li>
        ))}
      </ul>
    </div>

    <div className="card">
      <div className="card-header">
        <span className="card-icon">💻</span>
        <h3>Skills</h3>
      </div>
      <ul className="card-content">
        {testResponseData?.skills?.map((data, key) => (
          <li key={key}>{data}</li>
        ))}
      </ul>
    </div>

    <div className="card">
      <div className="card-header">
        <span className="card-icon">🗣️</span>
        <h3>Languages</h3>
      </div>
      <ul className="card-content">
        {testResponseData?.languages?.map((data, key) => (
          <li key={key}>{data}</li>
        ))}
      </ul>
    </div>

    <div className="card">
      <div className="card-header">
        <span className="card-icon">📜</span>
        <h3>Certificates</h3>
      </div>
      <ul className="card-content">
        {testResponseData?.certificates?.map((data, key) => (
          <li key={key}>{data}</li>
        ))}
      </ul>
    </div>
  </div>

  <button onClick={() => { setAppState(APPSTATE.FORM); }}>Back</button>
</>

  

        

    )
}

export default ResponsePage