
const SET_PANTRY = "SET_PANTRY"
const CHECK_PANTRY = "CHECK_PANTRY"

const initialState = {}

const pantryReducer = (state = initialState, action) => {
    
    switch (action.type) {
        case SET_PANTRY:
            return action.payload

        case CHECK_PANTRY:
            return action.payload
        default:
            return state
      }
}

export const checkPantry = () => {
    
    return dispatch => {
        const pantryJSON = window.localStorage.getItem('pantry')
        if ( pantryJSON ) {
            const pantry = JSON.parse(pantryJSON)
            dispatch({
                type: CHECK_PANTRY,
                payload: pantry
            })
        }
        else {
            dispatch({
                type: CHECK_PANTRY,
                payload: null
            })
        }
    }
}

export const setPantry = ( data ) => {
    return async dispatch => {
        window.localStorage.setItem('pantry', JSON.stringify(data))
        dispatch({
            type: SET_PANTRY,
            payload: data
        })
    }
}

export default { pantryReducer }