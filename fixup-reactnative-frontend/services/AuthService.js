import axios from 'axios'

class AuthService {
  constructor() {
    this.apiBaseUrl = 'http://127.0.0.1:8000';
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

      const response = await axios.post(`${this.apiBaseUrl}/api/auth/login/`, requestData); // Issue with this line

      const userData = response.data;

      return { success: true, data: userData };
    } 

    catch (error) {
      return { success: false, error: error.message };
    }

  }
}

export default new AuthService();