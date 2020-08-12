import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux'

import services from '../../../services'
import { setShoppingList, checkShoppingList } from '../shoppingListRedux'

import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import IconButton from '@material-ui/core/IconButton';
import DeleteIcon from '@material-ui/icons/DeleteForever';
import AddIcon from '@material-ui/icons/Add';
import EditIcon from '@material-ui/icons/Edit'
import SaveIcon from '@material-ui/icons/Save';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';

const useStyles = makeStyles((theme) => ({
    root: {
        width: '100%',
    },
    container: {
        height: "60vh",
        marginBottom: theme.spacing(1)
    },
    textField: {
        '& > *': {
        margin: theme.spacing(1),
        width: 120,
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
}))



const ShoppingList = () => {
    const classes = useStyles();
    const dispatch = useDispatch()
    const shoppinglist = useSelector( state => state.shoppingListReducer)
    const [quantity, setQuantity] = useState(0)
    const [unit, setUnit] = useState('')
    const [editable, setEditable] = useState(false)
    const [itemToEdit, setItemToEdit] = useState({name: ''})
    const [currentItem, setCurrentItem] = useState({})

    useEffect( () => {
        dispatch( checkShoppingList() )
        
    }, [dispatch])


    const columns = [
        { id: 'name', label: 'Name', minWidth: 100 },
        { id: 'quantity', label: 'Quantity', maxWidth: 40 },
        { id: 'unit', label: 'Unit', maxWidth: 40},
        { id: 'delete', label: 'Delete', maxWidth: 20},
        { id: 'edit', label: 'Edit', maxWidth: 20},
        { id: 'add', label: 'Add to pantry', maxWidth: 50}
      ]

    const handleEdit = async (event) => {
        event.preventDefault()
        

        try {
            const endpoint = currentItem['@controls']['foodman:edit-shoppinglistitems'].href
            const shoppingListEndpoint = shoppinglist['@controls'].self.href
            const method = currentItem['@controls']['foodman:edit-shoppinglistitems'].method
            const newItem = {
                shopping_list_id: currentItem.shopping_list_id,
                fooditem_id: currentItem.fooditem_id,
                quantity: Number(quantity),
                unit: unit
            }

            await services.sendData( endpoint, method, newItem)
            const data = await services.getResource( shoppingListEndpoint )
            dispatch( setShoppingList(data) )
            setEditable(false)
            
        } catch (error) {

        }
    }
    
    const handleDelete = ( item ) => async ( event ) => {
        event.preventDefault()
        const endpoint = item['@controls']['foodman:delete'].href
        const method = item['@controls']['foodman:delete'].method
        const listEndpoint = shoppinglist['@controls'].self.href

        await services.getResource( endpoint, method )
        const data = await services.getResource( listEndpoint, "GET" )
        dispatch( setShoppingList(data) )
    }

    const displayEdit = ( item ) => ( event ) => {
        setEditable(true)
        setItemToEdit({name: item.name, quantity: item.quantity, unit: item.unit})
        setCurrentItem(item)
    }

    const addToPantry = ( item ) => async ( event ) => {
        event.preventDefault()
        const addEndpoint = item['@controls']['foodman:add-pantry-fooditem'].href
        const addMethod = item['@controls']['foodman:add-pantry-fooditem'].method
        const delEndpoint = item['@controls']['foodman:delete'].href
        const delMethod = item['@controls']['foodman:delete'].method
        const listEndpoint = shoppinglist['@controls'].self.href

        const newItem = {
            fooditem_id: item.fooditem_id,
        }
        console.log(addEndpoint)
        console.log(addMethod)
        console.log(newItem)

        try {
            await services.sendData( addEndpoint, addMethod, newItem )
            await services.getResource( delEndpoint, delMethod )
            const data = await services.getResource( listEndpoint, "GET" )
            dispatch( setShoppingList(data) ) 
        } catch (error) {
            console.log(error)
        }
               
    }

    const renderRows = () => {
        
        return shoppinglist.items.map((row) => {
            
            return (
                <TableRow hover tabIndex={-1} key={`${row.name}${Math.floor(Math.random() * Math.floor(1000))}`}>
                    <TableCell>
                        {row.name}
                    </TableCell>
                    <TableCell>
                        {row.quantity}
                    </TableCell>
                    <TableCell>
                        {row.unit}
                    </TableCell>
                    <TableCell>
                        <IconButton edge="end" onClick={handleDelete( row )}>
                            <DeleteIcon />
                        </IconButton>
                    </TableCell>
                    <TableCell>
                        <IconButton edge="end" onClick={displayEdit( row )}>
                            <EditIcon />
                        </IconButton>
                    </TableCell>
                    <TableCell>
                        <IconButton edge="end" onClick={addToPantry( row )}>
                            <AddIcon />
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
        <div>
            <Paper className={classes.root}>
                <TableContainer className={classes.container}>
                    <Table stickyHeader aria-label="sticky table">
                    <TableHead>
                        {shoppinglist['items'] !== undefined ? renderHeaders() : <TableRow/>}         
                    </TableHead>
                    <TableBody>
                        {shoppinglist['items'] !== undefined ? renderRows() : <TableRow/>}
                    </TableBody>
                    </Table>
                </TableContainer>
            </Paper>
            <Paper>
                {editable ? 
                    <div className={classes.add}>
                        <TextField
                            className={classes.textField}
                            margin="normal"
                            id="foodItemName" 
                            label="food item"
                            name="name"
                            autoFocus
                            value={itemToEdit.name}
                            InputProps={{
                                readOnly: true,
                            }}
                        />
                        <TextField
                            className={classes.textField}
                            margin="normal"
                            id="unit" 
                            label="unit"
                            name="unit"
                            autoFocus
                            value={unit}
                            onChange={({ target }) => setUnit(target.value) }
                        />
                        <TextField
                            className={classes.textField}
                            margin="normal"
                            id="quantity" 
                            label="quantity"
                            name="quantity"
                            type="number"
                            value={quantity}
                            onChange={({ target }) => setQuantity(target.value) }
                        />
                        <Button 
                            startIcon={<SaveIcon />}
                            onClick={handleEdit} 
                            className={classes.button} 
                            type="submit"
                        >
                            Save
                        </Button>
                    </div>
                        : <div></div>
                }
            </Paper>
        </div>
    );
}

export default ShoppingList