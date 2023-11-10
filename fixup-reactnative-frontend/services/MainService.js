import axios from 'axios'
import AsyncStorage from '@react-native-async-storage/async-storage';
import { setUser } from '../redux/userReducer';
import store from '../redux/store';

class MainService {
  constructor() {
    this.apiBaseUrl = 'https://5d84-162-212-233-34.ngrok-free.app';
  }
  
  async getUserInfo() {
    try {
        const pk = await AsyncStorage.getItem('user_pk');

        if (pk) {
            const response = await axios.get(`${this.apiBaseUrl}/api/users/${pk}/`);
            const userInfo = response.data;

            store.dispatch(setUser(userInfo));

            return userInfo;
        } else {
            throw new Error('User pk not found in AsyncStorage')
        }
        
    } catch (error) {
      console.error('Error getting user info:', error);
    }
  }

}

export default new MainService();