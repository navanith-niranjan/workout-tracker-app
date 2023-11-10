import axios from 'axios';
import tough from 'tough-cookie';

const cookieJar = new tough.CookieJar();

const axiosInstance = axios.create({
  baseURL: 'https://5d84-162-212-233-34.ngrok-free.app', 
  withCredentials: true,
  jar: cookieJar, 
});

const clearCookies = () => {
  cookieJar.removeAllSync();
}

export { axiosInstance, clearCookies };