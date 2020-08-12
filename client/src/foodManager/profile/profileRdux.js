const SET_PROFILE = "SET_PROFILE"
const CHECK_PROFILE = "CHECK_PROFILE"
const initialState = {}


const profileReducer = (state = initialState, action) => {
    
    switch (action.type) {
        case SET_PROFILE:
            return action.payload

        case CHECK_PROFILE:
            return action.payload
        default:
            return state
      }
}

export const checkProfile = () => {
    return dispatch => {
        const profileJSON = window.localStorage.getItem('profile')
        if ( profileJSON ) {
            const profile = JSON.parse(profileJSON)
            dispatch({
                type: CHECK_PROFILE,
                payload: profile
            })
        }
        else {
            dispatch({
                type: CHECK_PROFILE,
                payload: null
            })
        }
    }
}

export const setProfile = ( data ) => {
    return async dispatch => {
        window.localStorage.setItem('profile', JSON.stringify(data))
        dispatch({
            type: SET_PROFILE,
            payload: data
        })
    }
}

export default { profileReducer }