import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux'
import { useHistory } from 'react-router-dom'

import service from '../services'
import { setProfile } from '../foodManager/profile/profileRdux'

import CssBaseline from '@material-ui/core/CssBaseline'
import Typography from '@material-ui/core/Typography'
import Container from '@material-ui/core/Container'
import { makeStyles } from '@material-ui/core/styles'
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';



const useStyles = makeStyles((theme) => ({
    container: {
        background: 'linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%)',
      height: '100vh'
    },
    paper: {
        padding: theme.spacing(4),
        textAlign: 'center',
        color: theme.palette.text.secondary,
        height: 350,
        marginTop: "10%",
        marginLeft: "30%",
        marginRight: "30%",
      },
      button: {
          marginRight: theme.spacing(2),
      },
      buttons: {
        textAlign: 'left',
        marginRight: theme.spacing(2),
        marginTop: theme.spacing(2),
    },
    warning: {
        color: "#ff0000"
    }
  }));


const Login = () => {
    const classes = useStyles();
    const dispatch = useDispatch()
    const history = useHistory()
    const controls = useSelector( state => state.landingReducer)
    const [username, setUsername] = useState('')
    const [email, setEmail] = useState('')
    const [message, setMessage] = useState('')
    
    //Login needs only a username
    const handleLogin = async ( event ) => {
        event.preventDefault()
        try {
            //use controls to get necessary information for the next request
            const href = controls['get'].href
            const method = controls['get'].method
            const endpoint = `${href}/${username}`
            const data = await service.getResource( endpoint, method )

            //dispatch the response to the store and push the next location to the history instance
            if (!data['@error']) {
                dispatch( setProfile( data ) )
                history.push(`/api/users/${data.username}/profile`)
            }
            else {
                setMessage('user not found')
            }
 
        } catch (error) {
            window.alert(error)
            setEmail('')
        }
      }

    //Username and email are required for creating a new account
    const handleRegister = async ( event ) => {
        event.preventDefault()
        try {

            //use controls to get necessary information for creating a new user 
            const endpoint = controls['foodman:add-user'].href
            const method = controls['foodman:add-user'].method
            const properties = Object.keys(controls['foodman:add-user'].schema.properties)
            
            //new user object
            const newUser = {
                [properties[0]]: username,
                [properties[1]]: email
            }
            
            const data = await service.sendData( endpoint, method, newUser )

            //Save the response to the 'store' if response is not an error message
            if (!data['@error']) {
                dispatch( setProfile( data ) )
                setMessage(`${username} created`)
                setEmail('')
            }

        } catch (error) {
        setEmail('')
        window.alert(error)
        }
    }

    return (
        <React.Fragment>
            <CssBaseline />
            <Container fixed className={classes.container}>
                <Grid container spacing={10}>
                    <Grid item lg={12}>
                        <Paper className={classes.paper}>
                            <Typography variant="h5">Sign in or create an account</Typography>
                            <Typography className={classes.warning} variant="overline">{message}</Typography>

                            <form className={classes.form} noValidate>
                                <div>
                                    <TextField
                                        variant="filled"
                                        margin="normal"
                                        fullWidth
                                        label={"username"}
                                        name={username}
                                        autoFocus
                                        value={username}
                                        onChange={({ target }) =>  setUsername(target.value)} //set the state of a username
                                    />
                                    <TextField
                                        variant="filled"
                                        margin="normal"
                                        fullWidth
                                        label={"email"}
                                        name={email}
                                        value={email}
                                        onChange={({ target }) => setEmail(target.value)}
                                    />
                                </div>
                                <div className={classes.buttons}>
                                    <Button onClick={handleLogin} className={classes.button} type="submit" variant="contained">Sign In</Button>
                                    <Button onClick={handleRegister} className={classes.button} type="submit" variant="contained">Register</Button>
                                </div>
                            </form>
                        </Paper>
                    </Grid>
                </Grid>
            </Container>
        </React.Fragment>
    )
}

export default Login
