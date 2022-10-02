import React from 'react';
import { Button, Input } from '@mui/material';
import MyModal from './MyModal';
import axios from 'axios';
import { baseUrl } from '../urls';

export default function AddNewContact({ setMyContacts }) {
    const [data, setData] = React.useState({
        label: null,
        phone: null,
    })
    const handleAddNew = (e) => {
        e.preventDefault()
        axios.post(baseUrl + '/contacts/create/', data, {
            headers: {
                Authorization: "Bearer " + localStorage.getItem('access')
            }
        }).then(res => {
            setMyContacts(prev => [res.data.data, ...prev])
            alert("New contact added successfully.")
        }).catch(err => {
            console.log(err);
            alert(`Failed to add contact!${JSON.stringify(err?.response?.data)}`);
        })
    }
    return (
        <MyModal opener='Add New Contact' title='Create a new contact here'>
            <form onSubmit={handleAddNew} style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                <br />
                <Input onChange={e => setData({ ...data, label: e.target.value })} value={data.label} required placeholder="Contact Description" />
                <br />
                <Input onChange={e => setData({ ...data, phone: e.target.value })} value={data.phone} required placeholder="Phone Number" />
                <br />
                <br />
                <Button type='submit'>Submit</Button>
            </form>
        </MyModal>
    );
}
