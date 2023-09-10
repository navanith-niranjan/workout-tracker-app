import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet } from 'react-native';
import AuthService from '../services/AuthService';
import { useNavigation, useRoute } from '@react-navigation/native';
import { StatusBar } from 'expo-status-bar';

const OTPVerifyScreen = () => {
  const navigation = useNavigation();
  const route = useRoute();
  const { email, password } = route.params;
  const [otp, setOTP] = useState('');
  const [error, setError] = useState('');
  const [isEmailSent, setIsEmailSent] = useState(true); 

  const handleVerify = async () => {
    if (!otp) {
      setError('Please enter the OTP code');
      return;
    }

    try {
      const verifyResult = await AuthService.verifyOTP(otp, email); 

      if (verifyResult.success) {
        const loginResult = await AuthService.login(email, password); 

        if (loginResult.success) {
          navigation.navigate('Home');
        }
        else {
          setError('Login failed')
        }
      } 
      else {
        setError(verifyResult.error || 'Invalid OTP. Please try again.');
      }
    } 
    catch (error) {
        setError('An error occurred during OTP verification. Please try again later.');
        console.error(error); 
    }
  };

  const handleResendEmail = async () => {
    try {
      const resendResult = await AuthService.resendEmail(email); 

      if (resendResult.success) {
        setIsEmailSent(true);
      } 
      else {
          setError(resendResult.error || 'Failed to resend OTP email. Please try again.');
      }
    } 
    catch (error) {
        setError('An error occurred during email resend. Please try again later.');
        console.error(error);
    }
  };

  return (
    <View style={styles.container}>
      <StatusBar barStyle="dark-content" />
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
        autoCapitalize="none"
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
