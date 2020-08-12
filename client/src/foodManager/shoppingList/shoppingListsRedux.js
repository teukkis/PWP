const SET_SHOPPING_LISTS = "SET_SHOPPING_LISTS"
const CHECK_SHOPPING_LISTS = "CHECK_SHOPPING_LISTS"

const initialState = {}

const shoppingListsReducer = (state = initialState, action) => {
    
    switch (action.type) {
        case SET_SHOPPING_LISTS:
            return action.payload

        case CHECK_SHOPPING_LISTS:
            return action.payload['@controls']
        default:
            return state
      }
}

export const checkShoppingLists = () => {
    
    return dispatch => {
        const shoppingListsJSON = window.localStorage.getItem('shoppingLists')
        if ( shoppingListsJSON ) {
            const shoppingLists = JSON.parse(shoppingListsJSON)
            dispatch({
                type: CHECK_SHOPPING_LISTS,
                payload: shoppingLists
            })
        }
    }
}


export const setShoppingLists = ( data ) => {
    
    return async dispatch => {
        window.localStorage.setItem('shoppingLists', JSON.stringify(data))
        dispatch({
            type: SET_SHOPPING_LISTS,
            payload: data
        })
    }
}

export default { shoppingListsReducer }