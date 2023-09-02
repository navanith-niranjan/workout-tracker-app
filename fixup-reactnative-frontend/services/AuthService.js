import axios from 'axios'

class AuthService {
  constructor() {
    this.apiBaseUrl = 'https://16f9-2605-b100-11b-40-e887-35f0-b64e-e04e.ngrok-free.app';
  }

  async login(emailOrUsername, password) {
    try {
      let identifierField;
      
      if (emailOrUsername.includes('@')) {
        identifierField = 'email';
      } 
      else {
        identifierField = 'username';
      }
      
      const requestData = {
        [identifierField]: emailOrUsername,
        password: password,
      };

      const response = await axios.post(`${this.apiBaseUrl}/api/auth/login/`, requestData); 

      const userData = response.data;

      return { success: true, data: userData };
    } 

    catch (error) {
      return { success: false, error: error.message };
    }

  }
}

export default new AuthService();