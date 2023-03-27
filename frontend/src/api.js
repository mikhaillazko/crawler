import axios from "axios";

const baseURL = 'http://127.0.0.1:8000/api/crawler/'
axios.defaults.baseURL = baseURL;

export const addTask = async (siteUrl) => {
    return axios.post(`tasks/`, {site_url: siteUrl});
}

export const getTask = async (task_id) => {
    return axios.get(`tasks/${task_id}`);
}

export const getTaskResults = async (task_id, offset) => {
    return axios.get(`links/?task_id=${task_id}&offset=${offset}`);
}
