import axios from 'axios'

class AuthService {
  constructor() {
    this.apiBaseUrl = 
    //'https://1c05-142-181-46-57.ngrok-free.app';
    //'https://16f9-2605-b100-11b-40-e887-35f0-b64e-e04e.ngrok-free.app';
    //'https://1890-142-189-85-134.ngrok-free.app/';
    //'https://5307-142-189-85-134.ngrok-free.app';
    'https://7b48-142-189-85-134.ngrok-free.app';
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

  async signup(username, email, password1, password2, firstName = '', lastName = '') {
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
      return { success: false, error: error.message };
    }
  }

  async verifyOTP(otpCode, email) {
    try {
      const requestData = {
        otp_code: otpCode,
        email: email, // Include the email in the request
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

  async handleSendEmail(email) {
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
  
}

export default new AuthService();