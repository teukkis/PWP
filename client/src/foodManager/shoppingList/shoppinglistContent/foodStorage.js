import React, { useState, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'

import services from '../../../services'
import { setShoppingList } from '../shoppingListRedux'
import { sendfoodStorage } from '../foodStorageRedux'

import { makeStyles } from '@material-ui/core/styles'
import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import IconButton from '@material-ui/core/IconButton';
import ShoppingCartIcon from '@material-ui/icons/ShoppingCart';


const useStyles = makeStyles({
    root: {
      width: '100%',
    },
    container: {
      maxHeight: 440,
    },
  });

const FoodStorage = () => {

    const classes = useStyles()
    const dispatch = useDispatch()
    const shoppinglist = useSelector( state => state.shoppingListReducer)
    const foodStorage = useSelector( state => state.foodStorageReducer)
    const [message, setMessage] = useState("")


    const handleAdd = ( name, fooditemId ) => async (event) => {
        event.preventDefault()
        const conf = shoppinglist['@controls']['foodman:add-fooditem']
        const endpoint = conf.href
        const method = conf.method
        const itemToAdd = {
            name: name,
            shopping_list_id: shoppinglist.id,
            fooditem_id: fooditemId,
            
        }
        
        try {
            await services.sendData( endpoint, method, itemToAdd)
            const data = await services.getResource( endpoint )
            dispatch( setShoppingList(data) )
            

        } catch (error) {
            window.alert(error)
            setMessage('')
        }
    }

    useEffect( () => {
        
        if (shoppinglist['@controls'] !== undefined) {
            const endpoint = shoppinglist['@controls']['foodman:all-fooditems'].href
            const method = shoppinglist['@controls']['foodman:all-fooditems'].method
            
            services
            .getResource( endpoint, method )
            .then(response => {
                dispatch( sendfoodStorage(response) )
            })
        }
        
    }, [shoppinglist, message, dispatch])


    const columns = [
        { id: 'name', label: 'Name', minWidth: 150 },
        { id: 'type', label: 'Type', maxWidth: 40 },
        { id: 'id', label: 'Add', maxWidth: 40 },
      ];

    const renderRows = () => {
        
        return foodStorage.items.map((row) => {
            return (
                <TableRow key={row.id} hover role="checkbox" tabIndex={-1}>
                    <TableCell>
                        {row.name}
                    </TableCell>
                    <TableCell>
                        {row.type}
                    </TableCell>
                    <TableCell>
                        <IconButton edge="end" onClick={handleAdd(row.name, row.id)}>
                            <ShoppingCartIcon />
                        </IconButton>
                    </TableCell>
                </TableRow>
            );
        })
    }

    const renderHeaders = () => {
        return (
        <TableRow>
            {columns.map((column) => (
                <TableCell
                key={column.id}
                align={column.align}
                style={{ minWidth: column.minWidth }}
                >
            {column.label}
            </TableCell>
        ))}
        </TableRow>
        )
    }


    return (
        <Paper className={classes.root}>
        <TableContainer className={classes.container}>
            <Table stickyHeader aria-label="sticky table">
            <TableHead>
                {foodStorage['@controls'] !== undefined ? renderHeaders() : <TableRow/>}         
            </TableHead>
            <TableBody>
                {foodStorage['@controls'] !== undefined ? renderRows() : <TableRow/>}
            </TableBody>
            </Table>
        </TableContainer>
        </Paper>
    )
}

export default FoodStorage
