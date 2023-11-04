import React, { useState } from 'react';
import { Text, TextInput, TouchableOpacity, StyleSheet, KeyboardAvoidingView, ScrollView } from 'react-native';
import AuthService from '../services/AuthService';
import { useNavigation, useRoute } from '@react-navigation/native';
import CustomButton from '../components/CustomButtonForLandingPage';
import { StatusBar } from 'expo-status-bar';
import CustomBackButton from '../components/CustomBackButton';

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
          navigation.navigate('Main');
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
        setIsEmailSent(false);
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
    <KeyboardAvoidingView
      style={{ flex: 1 }}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      enabled
    >
      <ScrollView
      contentContainerStyle={styles.container}
      keyboardDismissMode="on-drag"
      >
      <CustomBackButton iconStyle={{position: 'absolute', right: 140, bottom: 190}}/>
        <StatusBar barStyle="dark-content" />
        <Text style={styles.title}>OTP Verification</Text>
        {isEmailSent ? (
          <Text style={styles.subtitle}>Check your email for the OTP code.</Text>
        ) : (
          <Text style={styles.subtitle}>OTP email has been resent.</Text>
        )}
        <TextInput
          style={styles.input}
          keyboardType='numeric'
          onChangeText={(text) => setOTP(text)}
          value={otp}
          autoCapitalize="none"
        />
        <CustomButton title="Verify" onPress={handleVerify} />
        <TouchableOpacity onPress={handleResendEmail}>
            <Text style={styles.resendEmail}>Resend email?</Text>
        </TouchableOpacity>
        {error ? <Text style={styles.error}>{error}</Text> : null}
      </ScrollView>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    width: '100%',
    marginTop: 70,
  },
  title: {
    fontSize: 24,
    marginBottom: 10,
    fontFamily: 'Montserrat',
  },
  subtitle: {
    fontSize: 14,
    marginBottom: 40,
    fontFamily: 'Montserrat',
  },
  input: {
    width: '80%',
    marginBottom: 40,
    height: 50,
    backgroundColor: 'white',
    borderColor: 'white',
    borderBottomColor: 'gray',
    borderWidth: 1,
    paddingLeft: 10,
  },
  resendEmail: {
    color: 'blue', 
    textDecorationLine: 'underline', 
    marginTop: 10, 
    fontFamily: 'Montserrat',
  },
  error: {
    color: 'red',
    fontSize: 14,
    marginTop: 10,
  },
});

export default OTPVerifyScreen;
