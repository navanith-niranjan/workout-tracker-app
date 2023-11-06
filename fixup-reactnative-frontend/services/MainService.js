import axios from 'axios'
import AsyncStorage from '@react-native-async-storage/async-storage';

class MainService {
  constructor() {
    this.apiBaseUrl = 'https://7b3a-162-212-233-34.ngrok-free.app';
  }
  
  async getUserInfo() {
    try {
        const pk = await AsyncStorage.getItem('user_pk');

        if (pk) {
            const response = await axios.get(`${this.apiBaseUrl}/api/users/${pk}/`);
            return response.data;
        } else {
            throw new Error('User pk not found in AsyncStorage')
        }
        
    } catch (error) {
      console.error('Error getting user info:', error);
    }
  }

}

export default new MainService();