import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Animated, Easing, KeyboardAvoidingView } from 'react-native';
import AuthService from '../services/AuthService';
import { useNavigation } from '@react-navigation/native';
import { StatusBar } from 'expo-status-bar';

const ForgotPasswordScreen = () => {
  const navigation = useNavigation();

  const [email, setEmail] = useState('');
  const [otp, setOTP] = useState('');
  const [password1, setPassword1] = useState('');
  const [password2, setPassword2] = useState('');
  const [stage, setStage] = useState('email'); 
  const [fadeAnimOTP] = useState(new Animated.Value(0));

  useEffect(() => {
    if (stage === 'otp' || stage === 'resetPassword') {
      Animated.timing(fadeAnimOTP, {
        toValue: 1,
        duration: 500, 
        easing: Easing.linear,
        useNativeDriver: true,
      }).start();
    }
  }, [stage]);

  const handleSendEmail = async () => {
    if (!email) {
      console.log('Please fill in your email');
      return;
    }

    const sendEmailResult = await AuthService.handleSendEmail(email);

    if (sendEmailResult.success) {
      setStage('otp');
    } else {
      console.log('Failed to send email:', sendEmailResult.error);
    }
  };

  const handleVerifyOTP = async () => {
    if (!otp) {
      console.log('Please fill in your otp code');
      return;
    }

    const otpResult = await AuthService.handleVerifyOTP(email, otp);

    if (otpResult.success) {
      setStage('resetPassword');
    } else {
      console.log('Error:', handleVerifyOTP.error);
    }
  };

  const handleResetPassword = async () => {
    if (!password1 || !password2) {
      console.log('Please fill both password fields')
      return;
    }

    const changePasswordResult = await AuthService.handleResetPassword(email, otp, password1, password2)

    if (changePasswordResult.success) {
      navigation.navigate('SignIn'); 
    } else {
      console.log('Error:', handleResetPassword.error)
    }

  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      enabled
    >
      <StatusBar barStyle="dark-content" />
      {stage === 'email' && (
        <>
          <Text style={styles.title}>Forgot Password</Text>
          <TextInput
            style={styles.input}
            placeholder="Enter your email"
            onChangeText={(text) => setEmail(text)}
            value={email}
            autoCapitalize="none"
          />
          <Button title="Send Email" onPress={handleSendEmail} />
        </>
      )}

      {stage === 'otp' && (
        <Animated.View style={{ opacity: fadeAnimOTP }}>
          <View style={styles.otpContainer}>
            <Text style={styles.title}>Enter OTP</Text>
            <TextInput
              style={[styles.input, styles.otpInput]} 
              placeholder="Enter OTP"
              onChangeText={(text) => setOTP(text)}
              value={otp}
              autoCapitalize="none"
            />
            <Button title="Verify OTP" onPress={handleVerifyOTP} />
          </View>
        </Animated.View>
      )}

      {stage === 'resetPassword' && (
        <>
          <Text style={styles.title}>Reset Password</Text>
          <TextInput
            style={styles.input}
            placeholder="New Password"
            secureTextEntry
            onChangeText={(text) => setPassword1(text)}
            value={password1}
            autoCapitalize="none"
          />
          <TextInput
            style={styles.input}
            placeholder="Confirm New Password"
            secureTextEntry
            onChangeText={(text) => setPassword2(text)}
            value={password2}
            autoCapitalize="none"
          />
          <Button title="Reset Password" onPress={handleResetPassword} />
        </>
      )}
    </KeyboardAvoidingView>
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
  otpContainer: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  otpInput: {
    width: '160%', 
  },
});

export default ForgotPasswordScreen;
