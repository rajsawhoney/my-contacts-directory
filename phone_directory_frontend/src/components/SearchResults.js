import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { Button } from '@mui/material';
import axios from 'axios';
import { baseUrl } from '../urls';

export default function SearchResults({ results, setResults }) {

    const markAsSpam = (id) => {
        if (window.confirm('Are you sure, you want to mark it as spam?'))
            axios.put(baseUrl + '/contacts/mark_as_spam/' + id, null, {
                headers: {
                    Authorization: "Bearer " + localStorage.getItem('access')
                }
            }).then(res => {
                if (res.data.is_spam) {
                    const new_results = results.map(item => {
                        if (item.id === id) return { ...item, is_spam: true }
                        return item
                    })
                    setResults(new_results)
                    alert("Mark as Spam Success!")
                }
            }).catch(err => alert("Token seems to be expired! Click refresh token and try again."))
    }
    return (
        <TableContainer component={Paper}>
            <Table sx={{ minWidth: 350 }} aria-label="simple table">
                <TableHead>
                    <TableRow>
                        <TableCell>ID</TableCell>
                        <TableCell align="left">Contact Owner</TableCell>
                        <TableCell align="left">Phone Number</TableCell>
                        <TableCell align="left">Email</TableCell>
                        <TableCell align="left">Is Spam?</TableCell>
                        <TableCell align="left">Action</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {results.map((row) => (
                        <TableRow
                            key={row.id}
                        >
                            <TableCell>
                                {row.id}
                            </TableCell>
                            <TableCell align="left">{row.owner.name}</TableCell>
                            <TableCell align="left">{row.phone}</TableCell>
                            <TableCell align="left">{row.owner.email ?? 'null'}</TableCell>
                            <TableCell align="left">{row.is_spam ? <img style={{ width: '50px' }} src="https://upload.wikimedia.org/wikipedia/commons/b/bb/No-spam.png" alt='spam-icon' /> : "Not Spam"}</TableCell>
                            <TableCell align="left"><Button disabled={row.is_spam} onClick={() => markAsSpam(row.id)}>Mark as Spam</Button></TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
}
