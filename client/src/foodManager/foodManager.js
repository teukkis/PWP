import React from 'react';
import { Route, useHistory } from 'react-router-dom'
import { useSelector } from 'react-redux'

import Profile from './profile/profile'
import Pantry from './pantry/pantry'
import ShoppinglistsContainer from './shoppingList/shoppinglistContainer'

import { makeStyles } from '@material-ui/core/styles';
import Drawer from '@material-ui/core/Drawer';
import CssBaseline from '@material-ui/core/CssBaseline';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import List from '@material-ui/core/List';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';


const drawerWidth = 240;

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
  },
  appBar: {
    width: `calc(100% - ${drawerWidth}px)`,
    marginLeft: drawerWidth,
    background: 'linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%)',
  },
  drawer: {
    width: drawerWidth,
    flexShrink: 0,
  },
  drawerPaper: {
    width: drawerWidth,
  },
  // necessary for content to be below app bar
  toolbar: theme.mixins.toolbar,
  content: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    padding: theme.spacing(3),
  },
}));


const FoodManager = () => {
    const classes = useStyles()
    const history = useHistory()
    const profile = useSelector( state => state.profileReducer) //take the profile of the currently logged in user
    
    return (
        <div className={classes.root}>
            <CssBaseline />
            <AppBar position="fixed" className={classes.appBar}>
                <Toolbar>
                    <Typography variant="h3" noWrap>
                        Food Manager
                    </Typography>
                </Toolbar>
            </AppBar>
            <Drawer
                className={classes.drawer}
                variant="permanent"
                classes={{ paper: classes.drawerPaper }}
                anchor="left"
            >
        <div className={classes.toolbar} />
            <Divider />
                <List>
                  {['Profile', 'Shoppinglists', 'Pantry'].map((text, index) => (
                    <ListItem button key={text} onClick={ () => history.push(`${profile['@controls'].self.href}/${text}`)}>
                      <ListItemText primary={text} />
                    </ListItem>
                  ))}
                </List>
            </Drawer>
          <main className={classes.content}>
              <div className={classes.toolbar} />
            
              <Route exact path='/api/users/:user/profile'>
                  <Profile />
              </Route>
              <Route exact path='/api/users/:user/pantry'>
                  <Pantry />
              </Route>
              <Route path='/api/users/:user/shoppinglists'>
                  <ShoppinglistsContainer />
              </Route>
          </main>
      </div>
  );
}

export default FoodManager

