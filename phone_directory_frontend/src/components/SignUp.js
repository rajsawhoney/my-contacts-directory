import React from 'react';
import { Button, Input } from '@mui/material';
import MyModal from './MyModal';
import axios from 'axios';
import { baseUrl } from '../urls';

export default function SignUp({ setIsAuthenticated, setAccessToken }) {
    const [data, setData] = React.useState({
        name: null,
        phone: null,
        email: null,
        password: null
    })
    const handleSignUp = (e) => {
        e.preventDefault()
        axios.post(baseUrl + '/auth/register/', data).then(res => {
            const { refresh, access } = res.data.data
            localStorage.setItem('access', access)
            localStorage.setItem('refresh', refresh)
            setIsAuthenticated(true)
            setAccessToken(access)
            alert("User Registeration Success!")
        }).catch(err => {
            console.log(err);
            alert(`Failed to register!${JSON.stringify(err?.response?.data)}`);
        })
    }
    return (
        <MyModal opener='SignUp' title='SignUp Here'>
            <form onSubmit={handleSignUp} style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                <br />
                <Input onChange={e => setData({ ...data, name: e.target.value })} value={data.name} required placeholder="Your Full Name" />
                <br />
                <Input onChange={e => setData({ ...data, phone: e.target.value })} value={data.phone} required placeholder="Phone Number" />
                <br />
                <Input onChange={e => setData({ ...data, email: e.target.value })} value={data.email} placeholder="Email Number" />
                <br />
                <Input onChange={e => setData({ ...data, password: e.target.value })} value={data.password} placeholder="Password" />
                <br />
                <Button type='submit'>Submit</Button>
            </form>
        </MyModal>
    );
}
