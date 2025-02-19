import React, { useState } from "react";
import SearchBar from "./SearchBar";
import Results from ".components/Results";
import { fetchSearchResults } from "./services/api";


const App = () => {
    const [results, setResults] = useState([]);


    const handleSearch = async (query) => {
        try {
            const data = await fetchSearchResults(query);
            setResults(data.results); // Update results from the backend
        } catch (error) {
            console.error("Error fetching search results:", error);
        }
    };


    return (
        <div style={{ padding: "20px" }}>
            <h1>Unified Vintage Search</h1>
            <SearchBar onSearch={handleSearch} />
            <Results results={results} />
        </div>
    );
};


export default App;



