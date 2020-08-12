import React, { useState, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { useHistory } from 'react-router-dom'

import services from '../../services'
import { setProfile } from './profileRdux'

import CssBaseline from '@material-ui/core/CssBaseline'
import Typography from '@material-ui/core/Typography'
import { makeStyles } from '@material-ui/core/styles'
import Paper from '@material-ui/core/Paper'
import Grid from '@material-ui/core/Grid'
import Button from '@material-ui/core/Button'
import TextField from '@material-ui/core/TextField'


const useStyles = makeStyles((theme) => ({
    container: {
        backgroundColor: '#ffffff',
        height: '80vh'
      },
      paper: {
          padding: theme.spacing(4),
          textAlign: 'left',
          color: theme.palette.text.secondary,
          height: 300,
          marginTop: '2%',
          marginLeft: "5%",
          marginRight: "50%",
        },
        button: {
            marginRight: theme.spacing(2),
            marginTop: theme.spacing(2),
        },
        buttons: {
          textAlign: 'left',
          marginRight: theme.spacing(2),
          marginTop: theme.spacing(2),
        },
        currentInfo: {
            marginLeft: '5%'
        }
}));


const Profile = () => {
    const classes = useStyles();
    const dispatch = useDispatch()
    const history = useHistory()
    const profile = useSelector( state => state.profileReducer)
    const [username, setUsername] = useState('')
    const [email, setEmail] = useState('')
    const [currentusername, setcurrentUsername] = useState('')
    const [currentEmail, setcurrentEmail] = useState('')


    useEffect( () =>{
        if (profile['@controls'] !== undefined){
            const endpoint = profile['@controls'].self.href
            console.log(endpoint)
            services
            .getResource( endpoint )
            .then(response => {
                if ( response['@error'] ) {
                    window.localStorage.removeItem('profile')
                    history.push(`/api`)
                }
                else {
                    console.log(response)
                    setcurrentEmail(response.email)
                    setcurrentUsername(response.username)
                }
            })
        }
    }, [profile])

    const handleDelete = async ( event ) => {
        event.preventDefault()
        try {
            const endpoint = profile['@controls']['delete'].href
            const method = profile['@controls']['delete'].method
            
            await services.getResource( endpoint, method )
            
            history.push(`/api`)
            window.localStorage.removeItem('profile')
    
        } catch (error) {
            window.alert(error)
            setEmail('')
        }
    }

    const handleEdit =  async ( event ) => {
        event.preventDefault()
        try {
            const endpoint = profile['@controls']['edit'].href
            const method = profile['@controls']['edit'].method
            const properties = Object.keys(profile['@controls']['edit'].schema.properties)
            const u = properties[0]
            const e = properties[1]
            const newUser = {
                [u]: username,
                [e]: email
            }
            
            await services.sendData( endpoint, method, newUser )

            const href = profile['@controls']['collection'].href
            const getMethod = profile['@controls']['collection'].method
            const getEndpoint = `${href}/${username}`

            const data = await services.getResource( getEndpoint, getMethod )

            if (!data['@error']) {
                dispatch( setProfile( data ) )
                history.push(`/api/users/${username}/profile`)
            }

            setUsername('')
            setEmail('')
    
        } catch (error) {
            setEmail('')
            window.alert(error)
        }
    } 

  return (
    <React.Fragment>
        <CssBaseline />
        <Grid container spacing={2}>
            <Grid item lg={12}>
                <div className={classes.currentInfo}>
                    <Typography variant="h6">Username: {currentusername}</Typography>
                    <Typography variant="h6">Email: {currentEmail}</Typography>
                    <Button onClick={handleDelete} className={classes.button} type="submit" variant="contained">Delete</Button>
                </div>
            </Grid>
            <Grid item lg={12}>
                <Paper className={classes.paper}>
                    <Typography variant="h5">Edit your profile</Typography>
                    <form className={classes.form} noValidate>
                        <div>
                            <TextField
                                margin="normal"
                                fullWidth
                                label={"username"}
                                name={username}
                                autoFocus
                                value={username}
                                onChange={({ target }) =>  setUsername(target.value)}
                            />
                            <TextField
                                margin="normal"
                                fullWidth
                                label={"email"}
                                name={email}
                                value={email}
                                onChange={({ target }) => setEmail(target.value)}
                            />
                        </div>
                        <div className={classes.buttons}>
                            <Button onClick={handleEdit} className={classes.button} type="submit" variant="contained">Edit</Button>
                        </div>
                    </form>
                </Paper>
            </Grid>
        </Grid>
    </React.Fragment>
  )
}

export default Profile