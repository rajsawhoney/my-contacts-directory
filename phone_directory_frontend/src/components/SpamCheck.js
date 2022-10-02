import React from 'react';
import { Button, Input } from '@mui/material';
import MyModal from './MyModal';
import axios from 'axios';
import { baseUrl } from '../urls'

export default function SpamCheck() {
    const [number, setNumber] = React.useState('')
    const handleSpamCheck = (e) => {
        e.preventDefault()
        if (!number) return alert("Phone number is required!")
        axios.get(baseUrl + '/contacts/check_spam_number/' + number, {
            headers: {
                Authorization: "Bearer " + localStorage.getItem('access')
            }
        }).then(res => {
            console.log("res", res.data);
            alert(`${number} is ${res.data.is_spam ? '' : 'not'} marked as a spam number.`)
        }).catch(err => {
            alert(`Failed to check!${JSON.stringify(err?.response?.data)}`);
        })
    }
    return (
        <MyModal opener='Check Spam Number' title='Check Spam Phone Number'>
            <form onSubmit={handleSpamCheck} style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                <br />
                <Input onChange={e => setNumber(e.target.value)} value={number} required placeholder="Phone Number" />
                <br />
                <br />
                <Button type='submit'>Check</Button>
            </form>
        </MyModal>
    );
}
