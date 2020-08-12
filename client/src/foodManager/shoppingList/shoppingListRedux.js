
const SEND_SHOPPING_LIST = "SEND_SHOPPING_LIST"
const GET_SHOPPING_LIST = "GET_SHOPPING_LIST"
const CHECK_SHOPPING_LIST = "CHECK_SHOPPING_LIST"

const initialState = {}

const shoppingListReducer = (state = initialState, action) => {
    
    switch (action.type) {
        case SEND_SHOPPING_LIST:
            return action.payload

        case GET_SHOPPING_LIST:
            return action.payload['@controls']

        case CHECK_SHOPPING_LIST:
            return action.payload
        default:
            return state
      }
}

export const checkShoppingList = () => {
    
    return dispatch => {
        const shoppingListJSON = window.localStorage.getItem('shoppingList')
        if ( shoppingListJSON ) {
            const shoppingList = JSON.parse(shoppingListJSON)
            dispatch({
                type: CHECK_SHOPPING_LIST,
                payload: shoppingList
            })
        }
    }
}

export const setShoppingList = ( data ) => {
    return async dispatch => {
        window.localStorage.setItem('shoppingList', JSON.stringify(data))
        dispatch({
            type: SEND_SHOPPING_LIST,
            payload: data
        })
    }
}


export default { shoppingListReducer }