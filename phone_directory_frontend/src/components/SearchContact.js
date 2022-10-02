import { Button } from '@mui/material';
import axios from 'axios';
import React from 'react';
import { baseUrl } from '../urls';
import SearchResults from './SearchResults';

export default function SearchContact({ isAuthenticated }) {
    const [searchTerm, setSearchTerm] = React.useState('')
    const [prevUrl, setPrevUrl] = React.useState(null)
    const [nextUrl, setNextUrl] = React.useState(null)
    const [searchResults, setSearchResults] = React.useState([])
    const handleSearch = (searchUrl) => {
        if (!searchTerm) return
        axios.get(searchUrl, {
            headers: {
                Authorization: "Bearer " + localStorage.getItem('access')
            }
        }).then(res => {
            const { previous, next, results } = res.data
            setPrevUrl(previous)
            setNextUrl(next)
            setSearchResults(results)
        }).catch(err => alert("Token seems to be expired! Click refresh token and try again."))
    }

    if (!isAuthenticated) return null
    return (
        <div style={{ width: '100%' }}>
            <div style={{ width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <input style={{
                    padding: '1.5rem 3rem', flex: '.99',
                    borderRadius: '8px',
                    border: '0.5px solid black',
                    fontSize: '1.4rem'
                }} placeholder='Search contacts by phone or person name' onChange={e => setSearchTerm(e.target.value)} onKeyUp={e => e.key === "Enter" && handleSearch(baseUrl + `/contacts/search?search=${searchTerm}`)} value={searchTerm} />
                <Button style={{ padding: '1.5rem 2rem', backgroundColor: 'lightgray', fontWeight: 'bold' }} onClick={() => handleSearch(baseUrl + `/contacts/search?search=${searchTerm}`)}>Submit</Button>
            </div>
            {/* {searchResults.length > 0 ? <div> */}
            <h1>Search Results</h1>
            <SearchResults setResults={setSearchResults} results={searchResults} />
            <br />
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-around' }}>
                <Button onClick={() => handleSearch(prevUrl)} disabled={!prevUrl}>Previous Page</Button>
                <Button onClick={() => handleSearch(nextUrl)} disabled={!nextUrl}>Next Page</Button>
            </div>
            {/* </div> : <h1>{searchTerm ? 'Search Results' : null}</h1>} */}
        </div>
    );
}
