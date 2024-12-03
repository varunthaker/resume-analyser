import { APPSTATE } from "./enums"

interface ResponsePageProps {

    setAppState:(value:string)=>void
    responseData:any
}



const ResponsePage = (props:ResponsePageProps) => {

    const {setAppState, responseData} = props

    console.log("responseData == ", responseData);
    

    return (

        <><h1>Here are the reults</h1>
        <p>{responseData.data}</p>
        
        <button onClick= {()=> {setAppState(APPSTATE.FORM)}}>Back</button>
        
        </>

        

    )
}

export default ResponsePage