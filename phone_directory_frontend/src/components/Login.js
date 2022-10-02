import React from 'react';
import { Button, Input } from '@mui/material';
import MyModal from './MyModal';
import axios from 'axios';
import { baseUrl } from '../urls'

export default function Login({ setAccessToken, setIsAuthenticated }) {
    const [data, setData] = React.useState({
        phone: null,
        password: null
    })
    const handleLogin = (e) => {
        e.preventDefault()
        axios.post(baseUrl + '/auth/login/', data).then(res => {
            const { refresh, access } = res.data
            localStorage.setItem('access', access)
            localStorage.setItem('refresh', refresh)
            setIsAuthenticated(true)
            setAccessToken(access)
        }).catch(err => {
            alert(`Failed to login!${JSON.stringify(err?.response?.data)}`);
        })
    }
    return (
        <MyModal opener='Login' title='Login Here'>
            <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                <br />
                <Input onChange={e => setData({ ...data, phone: e.target.value })} value={data.phone} required placeholder="Username" />
                <br />
                <Input onChange={e => setData({ ...data, password: e.target.value })} value={data.password} required placeholder="Password" />
                <br />
                <Button type='submit'>Submit</Button>
            </form>
        </MyModal>
    );
}
