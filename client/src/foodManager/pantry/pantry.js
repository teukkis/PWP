import React, { useState, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'

import services from '../../services'
import { setPantry } from './pantryRedux'

import { makeStyles } from '@material-ui/core/styles'
import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import IconButton from '@material-ui/core/IconButton';
import DeleteIcon from '@material-ui/icons/Delete';


const useStyles = makeStyles({
    root: {
      width: '100%',
    },
    container: {
      maxHeight: 440,
    },
  });

const Pantry = () => {

    const classes = useStyles()
    const dispatch = useDispatch()
    const [message, setMessage] = useState("")
    const pantry = useSelector( state => state.pantryReducer)
    const profile = useSelector( state => state.profileReducer)

    const handleDelete = ( item ) => async ( event ) => {
        event.preventDefault()
        const endpoint = item.href
        await services.getResource( endpoint, "DELETE" ) //delete control should be in the response
        setMessage(item.name)
        setMessage('')
    }

    useEffect( () => {
        if (profile['@controls'] !== undefined) {
            const endpoint = profile['@controls']['foodman:get-pantry'].href
            const method = profile['@controls']['foodman:get-pantry'].method
            
            services
            .getResource( endpoint, method )
            .then(response => {
                dispatch( setPantry(response) )
            })
        }
        
    }, [profile, message])

    const columns = [
        { id: 'name', label: 'Name', minWidth: 150 },
        { id: 'add_date', label: 'Add_date', maxWidth: 40 },
        { id: 'id', label: 'gone', maxWidth: 40 },
      ];

    const renderRows = () => {
        if ( pantry.items.length === 0 ) {
            return (
                <TableRow >
                    <TableCell>
                        Your pantry is empty
                    </TableCell>
                    <TableCell>
                        Your pantry is empty
                    </TableCell>
                    <TableCell>
                        Your pantry is empty
                    </TableCell>
                </TableRow>
            )
        }

        return pantry.items.map((row) => {
            return (
                <TableRow hover role="checkbox" tabIndex={-1} key={row.name}>
                    <TableCell>
                        {row.name}
                    </TableCell>
                    <TableCell>
                        {row.add_date}
                    </TableCell>
                    <TableCell>
                        <IconButton edge="end" onClick={handleDelete(row)}>
                            <DeleteIcon />
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
                    {pantry['@controls'] !== undefined ? renderHeaders() : <TableRow/>}         
                </TableHead>
                <TableBody>
                    {pantry['@controls'] !== undefined ? renderRows() : <TableRow/>}
                </TableBody>
                </Table>
            </TableContainer>
            </Paper>

        </div>
    )
}

export default Pantry
