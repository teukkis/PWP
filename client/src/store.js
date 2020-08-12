import { createStore, combineReducers, applyMiddleware } from 'redux'
import thunk from 'redux-thunk'
import { composeWithDevTools } from 'redux-devtools-extension'

import landing from './landing/landingRedux'
import login from './login/loginRedux'
import profile from './foodManager/profile/profileRdux'
import shoppingLists from './foodManager/shoppingList/shoppingListsRedux'
import shoppingList from './foodManager/shoppingList/shoppingListRedux'
import foodStorage from './foodManager/shoppingList/foodStorageRedux'
import pantry from './foodManager/pantry/pantryRedux'


const rootReducer = combineReducers({
    landingReducer: landing.controlsReducer,
    loginReducer: login.loginReducer,
    profileReducer: profile.profileReducer,
    shoppingListsReducer: shoppingLists.shoppingListsReducer,
    shoppingListReducer: shoppingList.shoppingListReducer,
    foodStorageReducer: foodStorage.foodStorageReducer,
    pantryReducer: pantry.pantryReducer
})

const store = createStore(rootReducer, composeWithDevTools(applyMiddleware(thunk)))

export default store
