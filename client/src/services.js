
const API_URL = 'http://localhost:5000'


const getResource = async ( endpoint, method ) => {
    try {
      const response = await fetch(`${API_URL}${endpoint}`, { method: method} )
      const responseJSON = await response.json()
      return responseJSON
    } catch ( error ) {
      return error['error']
    }
    
    
}

const sendData = async ( endpoint, method, data ) => {
  try {
    const response = await fetch(
      `${API_URL}${endpoint}`,
      { 
        headers: { 'Content-Type': 'application/json' },
        method: method,
        body: JSON.stringify(data)
      }
    )
    const responseJSON = response
    return responseJSON

  } catch (error) {
    console.log(error)
    return error['error']
  }
  
}


export default { getResource, sendData }