import service from "../services"

const INIT_CONTROLS = "INIT_CONTROLS"
const CHECK_CONTROLS = "CHECK_CONTROLS"
const initialState = {}


const controlsReducer = (state = initialState, action) => {
    
    switch (action.type) {
        case INIT_CONTROLS:
            return action.payload['@controls']
        
        case CHECK_CONTROLS:
            return action.payload

        default:
            return state
      }
}


export const start = () => {
    return async dispatch => {
        try {
            window.localStorage.removeItem('controls')
            const controls = await service.getResource('/api', 'GET')
            window.localStorage.setItem('controls', JSON.stringify(controls['@controls']))
            dispatch({
                type: INIT_CONTROLS,
                payload: controls
            })
        } catch (error) {
            window.alert(error)
        }
    }
}

export const checkControls = () => {
    return dispatch => {
        const controlsJSON = window.localStorage.getItem('controls')
        if ( controlsJSON ) {
            const controls = JSON.parse(controlsJSON)
            dispatch({
                type: CHECK_CONTROLS,
                payload: controls
            })
        }
        else {
            start()
        }
    }
}


export default { controlsReducer }