import React from 'react'
import { Route } from "react-router-dom";

import Shoppinglist from './shoppinglistContent/shoppinglist'
import Shoppinglists from './shoppinglistContent/shoppinglists'
import FoodStorage from './shoppinglistContent/foodStorage'

import Paper from '@material-ui/core/Paper/Paper'
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';

const useStyles = makeStyles((theme) => ({
    paper: {
    minHeight: 300,
    maxWidth: 600
    },
    
  }));

const ShoppinglistContainer = () => {

    const classes = useStyles()

    return (
        <div>
            <Grid container spacing={3}>
                <Grid item lg={3}>
                
                    <Shoppinglists />
                
                </Grid>
                <Route exact path="/api/users/:user/Shoppinglists/:listname">
                    <Grid item lg={5}>
                            <Shoppinglist />                        
                    </Grid>
                
                    <Grid item lg={4}>
                        <Paper className={classes.paper}>
                            <FoodStorage/>
                        </Paper>
                    </Grid>
                </Route>
            </Grid>
            
        </div>
    )
}

export default ShoppinglistContainer
