import React from 'react'
import { useDispatch } from 'react-redux'
import { useHistory } from 'react-router-dom'

import { start } from './landingRedux'

import CssBaseline from '@material-ui/core/CssBaseline'
import Typography from '@material-ui/core/Typography'
import Container from '@material-ui/core/Container'
import { makeStyles } from '@material-ui/core/styles'
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';



const useStyles = makeStyles((theme) => ({
    container: {
      background: 'linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%)',
      height: '100vh'
    },
    paper: {
        padding: theme.spacing(4),
        textAlign: 'center',
        color: theme.palette.text.secondary,
        height: 300,
        marginTop: 200,
        marginLeft: 300,
        marginRight: 300,
    },
    button: {
        margin: theme.spacing(10)
    },
  }));


const Landing = () => {

    const classes = useStyles()
    const dispatch = useDispatch()
    const history = useHistory()

    const handleButton = () => {
        dispatch( start() )
        history.push('/api/login')
    }

    return (
        <React.Fragment>
            <CssBaseline />
            <Container fixed className={classes.container}>
                <Grid container spacing={10}>
                    <Grid item lg={12}>
                        <Paper className={classes.paper}>
                            <Typography variant="h3">Welcome to FoodManager</Typography>
                                <Button onClick={handleButton} className={classes.button} variant="contained" color="primary">
                                    Start
                                </Button>
                        </Paper>
                    </Grid>
                </Grid>
            </Container>
        </React.Fragment>
    )
}


export default Landing
