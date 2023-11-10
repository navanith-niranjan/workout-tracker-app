import axios from 'axios'
import AsyncStorage from '@react-native-async-storage/async-storage';
import { axiosInstance, clearCookies } from './axiosConfig';
import store from '../redux/store';
import { clearAuthState } from '../redux/authReducer';

class AuthService {
  constructor() {
    this.apiBaseUrl = 'https://5d84-162-212-233-34.ngrok-free.app';
  }
  
  async saveToken(token) {
    try {
      await AsyncStorage.setItem('authToken', token);
    } catch (error) {
      console.error('Error saving token:', error);
    }
  }

  async verifyToken(token) {
    try {
      const response = await axiosInstance.post(`${this.apiBaseUrl}/api/auth/token/verify/`, { token: token });

      if (response.status === 200) {
        return true; 
      } else {
        return false; 
      }

    } catch (error) {
      console.error('Token verification error:', error);
      return false; 
    }
  }

  async get_email(Username) {
    try {
      const response = await axios.post(`${this.apiBaseUrl}/api/get-email/`, {username: Username});

      return response.data.email;
    } catch (error) {
      console.error('Error:', error);
    }
  }

  async login(emailOrUsername, password) {
    try {
      let identifierField;
  
      if (emailOrUsername.includes('@')) {
        identifierField = 'email';
      } else {
        identifierField = 'username';
      }
  
      const requestData = {
        [identifierField]: emailOrUsername,
        password: password,
      };
  
      const response = await axios.post(`${this.apiBaseUrl}/api/auth/login/`, requestData);
      const userData = response.data;

      if (userData.access) {
        await this.saveToken(userData.access);
      }

      await AsyncStorage.setItem('user_pk', userData.user.pk.toString());

      return { success: true, data: userData, token: userData.access };
    } catch (error) {
      if (error.response && error.response.data && error.response.data.non_field_errors) {
        const errorMessages = error.response.data.non_field_errors;

        if (errorMessages.includes('E-mail is not verified.')) {
          return { success: false, error: 'Account is not verified' };
        }
    }
      return { success: false, error: error.message };
    }
  }

  async logout() {
    try {
      await AsyncStorage.clear();
      store.dispatch(clearAuthState());

      await axios.post(`${this.apiBaseUrl}/api/auth/logout/`);

      return { success: true };
    } catch (error) {
        console.error('Logout error:', error);
        return { success: false, error: error.message };
    }
  }

  async signup(username, email, password1, password2, firstName, lastName) {
    try {
      const requestData = {
        username: username,
        email: email,
        password1: password1,
        password2: password2,
        first_name: firstName,
        last_name: lastName,
      };

      const response = await axios.post(`${this.apiBaseUrl}/api/auth/registration/`, requestData);
      const responseData = response.data;
      
      return { success: true, data: responseData };
    } catch (error) {
      if (error.response && error.response.data) {
        const responseErrors = error.response.data;
  
        if (responseErrors.username) {
          return { success: false, error: responseErrors.username[0] };
        } else if (responseErrors.email) {
          return { success: false, error: responseErrors.email[0] };
        }
      }
      return { success: false, error: error.message };
    }
  }

  async verifyOTP(otpCode, email) {
    try {
      const requestData = {
        otp_code: otpCode,
        email: email, 
      };

      const response = await axios.post(`${this.apiBaseUrl}/api/auth/registration/verify-email-otp/`, requestData);

      if (response.status === 200) {
        return { success: true };
      } else {
        return { success: false, error: 'OTP verification failed' };
      }
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  async resendEmail(email) {
    try {
      const requestData = {
        email: email,
      };

      const response = await axios.post(`${this.apiBaseUrl}/api/auth/registration/resend-email-otp/`, requestData);

      const responseData = response.data;

      return { success: true, data: responseData };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  async handleSendEmailForPasswordReset(email) {
    try {
      const requestData = {
        email: email,
      };

      const response = await axios.post(
        `${this.apiBaseUrl}/api/auth/password/reset-otp/`,
        requestData
      );

      if (response.status === 200) {
        return { success: true };
      } else {
        return { success: false, error: 'Failed to send email' };
      }
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  async handleVerifyOTP(email, otpCode) {
    try {
      const requestData = {
        email: email,
        otp_code: otpCode,
      };
  
      const response = await axios.post(
        `${this.apiBaseUrl}/api/auth/password/reset-otp/confirm/`,
        requestData
      );
  
      if (response.status === 206) {
        return { success: true };
      }
    } catch (error) {
      return { success: false, error: 'OTP verification failed' };
    }
  }

  async handleResetPassword(email, otpCode, password1, password2) {
    try {
      const requestData = {
        email: email,
        otp_code: otpCode,
        password1: password1,
        password2: password2,
      };
  
      const response = await axios.post(
        `${this.apiBaseUrl}/api/auth/password/reset-otp/confirm/`,
        requestData
      );
  
      if (response.status === 200) {
        return { success: true };
      }
    } catch (error) {
      return { success: false, error: 'Passwords do not match' };
    }
  }

  // async deleteAccount() {
  //   try {
  //     const pk = await AsyncStorage.getItem('user_pk');
      
  //     if (pk) {
  //       const response = await axiosInstance.delete(`${this.apiBaseUrl}/api/users/${pk}/`);
        
  //       if (response.status === 204) {
  //         await AsyncStorage.clear();
  //         store.dispatch(clearAuthState());
  //         clearCookies();
  //         console.log("IT WORKED IT DELETED")
  //       }

  //       return {success: true}
  //     } else {
  //       throw new Error('User pk not found in AsyncStorage')
  //     }
  //   } catch (error) {
  //     return {success: false, error: 'Failed to delete account'}
  //   }
  // }
  
}

export default new AuthService();