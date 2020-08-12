
const SEND_FOOD_STORAGE = "SEND_FOOD_STORAGE"
const CHECK_FOOD_STORAGE = "CHECK_FOOD_STORAGE"

const initialState = {}

const foodStorageReducer = (state = initialState, action) => {
    
    switch (action.type) {
        case SEND_FOOD_STORAGE:
            return action.payload

        case CHECK_FOOD_STORAGE:
            return action.payload
        default:
            return state
      }
}

export const checkfoodStorage = () => {
    
    return dispatch => {
        const foodStorageJSON = window.localStorage.getItem('foodStorage')
        if ( foodStorageJSON ) {
            const foodStorage = JSON.parse(foodStorageJSON)
            dispatch({
                type: CHECK_FOOD_STORAGE,
                payload: foodStorage
            })
        }
    }
}

export const sendfoodStorage = ( data ) => {
    return async dispatch => {
        window.localStorage.setItem('foodStorage', JSON.stringify(data))
        dispatch({
            type: SEND_FOOD_STORAGE,
            payload: data
        })
    }
}

export default { foodStorageReducer }