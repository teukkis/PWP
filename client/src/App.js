import React, { useEffect } from 'react'
import { Switch, Route, Redirect } from 'react-router-dom'
import { useDispatch } from 'react-redux'

import Landing from './landing/landing'
import Login from './login/login'
import { checkControls } from './landing/landingRedux'
import { checkProfile } from './foodManager/profile/profileRdux'
import FoodManager from './foodManager/foodManager'

const App = () => {

    const dispatch = useDispatch()

    //check localstorage for existing (user related) controls on every dispatch
    useEffect( () => {
        dispatch( checkControls() )
        dispatch( checkProfile() )
    }, [ dispatch, ])

    return (
        <div>
            <Switch>
                <Route exact path='/api/login'>
                    <Login />
                </Route>
                <Route path='/api/:user'>
                    <FoodManager />
                </Route>
                <Route exact path='/api'>
                    <Landing />
                </Route>
                <Route path='/'>
                    <Redirect to='/api' />
                </Route>
            </Switch>
        </div>
    )
}

export default App
