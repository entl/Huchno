import {string} from "prop-types";
import axios, {AxiosResponse} from "axios";
import {UUID} from "node:crypto";
import {API_HOST} from "@env";

const api: string = "http://localhost:8000/";

// get all users using axios
export const getUsers = async (access_token: string) => {
    try {
        const response = await axios({
            method: "GET",
            url: `${API_HOST}/users/`,
            headers: {
                "Content-type": "multipart/form-data",
                "Authorization": `Bearer ${access_token}`
            }});
        return response.data;
    } catch (error) {
        console.error('Error fetching user data:', error);
    }
};

// get user by id using axios
export const getUserById = async (id: UUID, access_token: string) => {
    try {
        const response: AxiosResponse = await axios.get(api + `users/${id}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching user data:', error);
    }
}

