import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux'
import { useHistory, useParams } from 'react-router-dom'

import services from '../../../services'
import { setShoppingLists } from '../shoppingListsRedux'
import { setShoppingList } from '../shoppingListRedux'


import { makeStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction';
import ListItemText from '@material-ui/core/ListItemText';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import IconButton from '@material-ui/core/IconButton';
import ArrowIcon from '@material-ui/icons/ArrowForwardIos';
import DeleteIcon from '@material-ui/icons/DeleteForever'
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Paper from '@material-ui/core/Paper/Paper'
import Typography from '@material-ui/core/Typography'
import SaveIcon from '@material-ui/icons/Save';



const useStyles = makeStyles((theme) => ({
    root: {
      width: '100%',
      maxWidth: 360,
      backgroundColor: theme.palette.background.paper,
    },
    paper: {
        height: "60vh",
        maxWidth: 600,
        marginBottom: theme.spacing(1)
    },
    textField: {
        '& > *': {
          margin: theme.spacing(1),
          width: 150,
          height: 35
        },
    },
    add: {
        height: 35,
        display: 'inline',
    },
    button: {
        marginTop: 30,
        background:"linear-gradient(45deg, #555555 30%, #888888 90%)",
        color:"#ffffff"
    }
  }));

const Shoppinglists = () => {

    const classes = useStyles()
    const dispatch = useDispatch()
    const history = useHistory()
    const { user } = useParams()
    const profile = useSelector( state => state.profileReducer)
    const shoppinglists = useSelector( state => state.shoppingListsReducer)
    const [message, setMessage] = useState("")
    const [newShoppingList, setNewShoppingList] = useState("")

    const handleInspect = ( href, name ) => async ( event ) => {
        event.preventDefault()
        
        try {
            const data = await services.getResource( href )
            
            if (!data['@error']) {
                dispatch( setShoppingList(data) )
                history.push(`/api/users/${user}/Shoppinglists/${name}`)
            }
 
    
        } catch (error) {
            window.alert(error)
            setMessage('')
        }
    }

    const handleDelete = ( href, method, name ) => async (event) => {
        event.preventDefault()

        try {
            await services.getResource( href, method )
            setMessage(name)
        } catch (error) {
            console.log(error)
        }

        
       
    }

    const addShoppingList = async (event) => {
        event.preventDefault()
        const conf = shoppinglists['@controls']['foodman:add-shoppinglist']
        const endpoint = conf.href
        const method = conf.method
        const newShoppingListObject = {
            name: newShoppingList
        }

        try {
            await services.sendData( endpoint, method, newShoppingListObject)
            setMessage(newShoppingList)
            setNewShoppingList('')
            setMessage('')

        } catch (error) {
            window.alert(error)
            setMessage('')
        }

    }

    useEffect( () => {
        if (profile['@controls'] !== undefined) {
            const endpoint = profile['@controls']['foodman:all-shoppinglists'].href
            const method = profile['@controls']['foodman:all-shoppinglists'].method
            
            services
            .getResource( endpoint, method )
            .then(response => {
                dispatch( setShoppingLists(response) )

                if (response.items.length === 0) {
                    history.push(`/api/users/${user}/Shoppinglists`)
        
                }
            })
        }
        
    }, [profile, message])

    const rows = () => {

        if (shoppinglists.items.length === 0) {
            return <Typography variant="h6">No shopping lists</Typography>
        }

        return shoppinglists.items.map((item) => {
            console.log(item)

            const labelId = `checkbox-list-label-${item.name}`
            const hrefSelf = item['@controls'].self.href
            const hrefDelete = item['@controls']['delete'].href
            const methodDelete = item['@controls']['delete'].method
            return (
                <ListItem key={item.name} role={undefined} dense button onClick={handleInspect( hrefSelf, item.name )}>
                    <ListItemIcon>
                        <IconButton edge="end" aria-label="comments" onClick={handleDelete(hrefDelete, methodDelete, item.name)}>
                            <DeleteIcon />
                        </IconButton>
                    </ListItemIcon>
                <ListItemText id={labelId} primary={item.name} />
                    <ListItemSecondaryAction>
                        <IconButton edge="end" aria-label="comments" onClick={handleInspect( hrefSelf, item.name )}>
                        <ArrowIcon />
                        </IconButton>
                    </ListItemSecondaryAction>
                </ListItem>
            )
        })
    }


    return (
        <div>
            <Paper className={classes.paper}>
                <List className={classes.root}>
                    {shoppinglists['@controls'] !== undefined ? rows() : <div></div>}
                </List>
            </Paper>
            <Paper>
                <div className={classes.add}>
                    <TextField
                        className={classes.textField}
                        margin="normal"
                        id="standard-basic" 
                        label="Add shopping list"
                        name="newShoppingList"
                        autoFocus
                        value={newShoppingList}
                        onChange={({ target }) => setNewShoppingList(target.value) }
                    />
                    <Button 
                        startIcon={<SaveIcon />}
                        onClick={addShoppingList} 
                        className={classes.button} 
                        type="submit"
                        
                    >
                        Save
                    </Button>
                </div>
            </Paper>
        </div>
    )
}

export default Shoppinglists
