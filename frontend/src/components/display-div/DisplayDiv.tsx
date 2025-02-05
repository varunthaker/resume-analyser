const DisplayDiv = ({ sectionData, icon, title }: { sectionData: string[], icon: string, title:string }) => {


    return (
        <div className="card">
        <div className="card-header">
          <span className="card-icon">{icon}</span>
          <h3>{title}</h3>
        </div>
        <div className="card-content">
    
        {sectionData.length? <ul>
          {sectionData?.map((data, key) => (
            <li key={key}>{data}</li>
          ))}
        </ul> : <p>No improvement points</p>}
        
        </div>
      </div>
        
    )

}

export default DisplayDiv