import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet } from 'react-native';
import AuthService from '../services/AuthService';
import { useNavigation, useRoute } from '@react-navigation/native';

const OTPVerifyScreen = () => {
  const navigation = useNavigation();
  const route = useRoute();
  const { email } = route.params; // Get the email from the route parameters
  const [otp, setOTP] = useState('');
  const [error, setError] = useState('');
  const [isEmailSent, setIsEmailSent] = useState(true); // Change to false initially

  const handleVerify = async () => {
    if (!otp) {
      setError('Please enter the OTP code');
      return;
    }

    try {
      const verifyResult = await AuthService.verifyOTP(otp, email); // Include the email in the verification request

      if (verifyResult.success) {
        // OTP verification was successful, navigate to the login screen
        navigation.navigate('SignIn'); // Update the screen name to 'SignIn' or your login screen's name
      } else {
        // Handle OTP verification failure, display an error message
        setError(verifyResult.error || 'Invalid OTP. Please try again.');
      }
    } catch (error) {
      // Handle any unexpected errors that may occur during OTP verification
      setError('An error occurred during OTP verification. Please try again later.');
      console.error(error); // Log the error for debugging purposes
    }
  };

  const handleResendEmail = async () => {
    try {
      // Assuming you have access to the user's email address from the registration screen
      // Replace 'userEmail' with the actual user's email
      const resendResult = await AuthService.resendEmail(email); // Include the email in the resend request

      if (resendResult.success) {
        // Email resend was successful, update the state to indicate the email has been resent
        setIsEmailSent(true);
      } else {
        // Handle email resend failure, display an error message
        setError(resendResult.error || 'Failed to resend OTP email. Please try again.');
      }
    } catch (error) {
      // Handle any unexpected errors that may occur during email resend
      setError('An error occurred during email resend. Please try again later.');
      console.error(error); // Log the error for debugging purposes
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>OTP Verification</Text>
      {isEmailSent ? (
        <Text>Check your email for the OTP code.</Text>
      ) : (
        <Text>OTP email has been resent.</Text>
      )}
      <TextInput
        style={styles.input}
        placeholder="Enter OTP"
        onChangeText={(text) => setOTP(text)}
        value={otp}
      />
      <Button title="Verify" onPress={handleVerify} />
      <Button title="Resend Email" onPress={handleResendEmail} />
      {error ? <Text style={styles.error}>{error}</Text> : null}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    marginBottom: 20,
  },
  input: {
    width: '80%',
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 10,
    paddingLeft: 10,
  },
  error: {
    color: 'red',
    fontSize: 14,
    marginTop: 10,
  },
});

export default OTPVerifyScreen;
