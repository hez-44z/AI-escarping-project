import axios from "axios";

const BASE_URL = "http://127.0.0.1:5000"; // Backend URL

export const fetchSearchResults = async (query) => {
    const response = await axios.get(`${BASE_URL}/search?q=${query}`);
    return response.data;
};
