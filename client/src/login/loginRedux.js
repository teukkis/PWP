const SET_USER = "SET_USER"

const initialState = {
    user: {}
}

const loginReducer = (state = initialState, action) => {
    
    switch (action.type) {
        case SET_USER:
            return { controls: action.payload['@controls'] }

        default:
            return state
      }
}




export default { loginReducer }