import { Button } from '@mui/material';
import axios from 'axios';
import React from 'react';
import './App.css';
import AddNewContact from './components/AddNewContact';
import ContactsList from './components/ContactsList';
import Login from './components/Login';
import SearchContact from './components/SearchContact';
import SignUp from './components/SignUp';
import SpamCheck from './components/SpamCheck';
import { baseUrl } from './urls';
import phoneIcon from './assets/images/phone-icon.png'

function App() {
  const [isAuthenticated, setIsAuthenticated] = React.useState(false)
  const [accessToken, setAccessToken] = React.useState(null)
  const [myProfile, setMyProfile] = React.useState(null)
  const [myContacts, setMyContacts] = React.useState([])

  const resetAll = () => {
    setAccessToken(null)
    setIsAuthenticated(false)
    localStorage.removeItem('access')
    localStorage.removeItem('refresh')
    setMyProfile(null)
    setMyContacts([])
  }
  React.useEffect(() => {
    const token = localStorage.getItem('access')
    if (token) {
      setIsAuthenticated(true)
      setAccessToken(token)
    }
    else setIsAuthenticated(false)
  }, [])

  React.useEffect(() => {
    if (isAuthenticated && accessToken) {
      axios.get(baseUrl + '/auth/myprofile/', {
        headers: {
          Authorization: "Bearer " + accessToken
        }
      }).then(res => {
        setMyProfile(res.data.data)
      }).catch(err => alert("Token seems to be expired! Click refresh token and try again."))

      axios.get(baseUrl + '/contacts/mycontacts/?limit=20', {
        headers: {
          Authorization: "Bearer " + accessToken
        }
      }).then(res => {
        setMyContacts(res.data.results)
      }).catch(err => alert("Token seems to be expired! Click refresh token and try again."))
    }
  }, [isAuthenticated, accessToken])

  const refreshToken = () => {
    axios.post(baseUrl + '/auth/token/refresh/', {
      'refresh': localStorage.getItem('refresh')
    }).then(res => {
      const { refresh, access } = res.data
      setAccessToken(access)
      localStorage.setItem('access', access)
      localStorage.setItem('refresh', refresh)
      alert("Token refreshed! Now try doing your stuffs.")
    }).catch(err => console.log("Err:", err))
  }

  const handleLogout = () => {
    axios.post(baseUrl, '/auth/logout/', { refresh_token: localStorage.getItem('refresh') }).then(res => {
      resetAll()
    }).catch(err => {
      resetAll()
    })
  }

  return (
    <div className="App">
      {isAuthenticated && myProfile ? <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ float: 'right', display: 'flex', alignItems: 'center' }}>
          <a style={{ textDecoration: 'none', paddingRight: '10px', fontSize: '20px' }} href='/docs/'>API Docs</a>
          <a style={{ textDecoration: 'none', fontSize: '20px' }} href='/admin/'>Admin Dashboard</a>
        </div>
        <div>Loginned as <strong>{myProfile?.name}({myProfile?.phone})</strong></div>
        <div style={{ float: 'right', display: 'flex', alignItems: 'center' }}>
          <SpamCheck />
          <Button onClick={refreshToken}>Refresh Token</Button>
          <Button onClick={handleLogout}>Logout</Button>
        </div>
      </div> :
        <div style={{ display: 'flex', alignItems: 'center', marginLeft: 'auto' }}>
          <Login setIsAuthenticated={setIsAuthenticated} setAccessToken={setAccessToken} />
          <SignUp setIsAuthenticated={setIsAuthenticated} setAccessToken={setAccessToken} />
        </div>}

      {isAuthenticated ?
        <div>
          <div >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <h1>My contacts</h1>
              <div style={{ marginLeft: '5rem' }}> <AddNewContact setMyContacts={setMyContacts} /></div>
            </div>
            {myContacts.length > 0 ? <ContactsList contacts={myContacts} /> : <p>No contacts found</p>}
          </div>
          <br />
          <br />
          <SearchContact isAuthenticated={isAuthenticated} />
        </div> : <div style={{ width: '100vw', height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column' }}>
          <img src={phoneIcon} alt='logo' />
          <h1 style={{ fontSize: '4rem', textShadow: '1px 12px 10px yello;' }}>Welcome to My Contacts Directory</h1></div>}
    </div>
  );
}

export default App;
