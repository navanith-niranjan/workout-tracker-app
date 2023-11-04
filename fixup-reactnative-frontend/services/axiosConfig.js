import axios from 'axios';
import tough from 'tough-cookie';

const cookieJar = new tough.CookieJar();

const axiosInstance = axios.create({
  baseURL: 'https://7b3a-162-212-233-34.ngrok-free.app', 
  withCredentials: true,
  jar: cookieJar, 
});

export default axiosInstance;