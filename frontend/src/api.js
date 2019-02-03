import axios from 'axios'

const api = axios.create({
  baseURL: 'http://0.0.0.0:8888/api/',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json'
  }
})

export default api
