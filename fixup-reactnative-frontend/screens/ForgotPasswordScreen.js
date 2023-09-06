import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Animated, Easing } from 'react-native';
import AuthService from '../services/AuthService';

const ForgotPasswordScreen = () => {
  const [email, setEmail] = useState('');
  const [otp, setOTP] = useState('');
  const [password1, setPassword1] = useState('');
  const [password2, setPassword2] = useState('');
  const [stage, setStage] = useState('email'); // Initial stage is 'email'
  const [fadeAnimOTP] = useState(new Animated.Value(0)); // Initialize opacity value

  useEffect(() => {
    // Trigger the fade-in effect when the stage changes to 'otp'
    if (stage === 'otp') {
      Animated.timing(fadeAnimOTP, {
        toValue: 1,
        duration: 500, // Adjust the duration as needed
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
    // Implement your logic to reset the password using password1 and password2
    // Once the password is reset, you can navigate the user to the login screen or another appropriate screen
  };

  return (
    <View style={styles.container}>
      {stage === 'email' && (
        <>
          <Text style={styles.title}>Forgot Password</Text>
          <TextInput
            style={styles.input}
            placeholder="Enter your email"
            onChangeText={(text) => setEmail(text)}
            value={email}
          />
          <Button title="Send Email" onPress={handleSendEmail} />
        </>
      )}

      {stage === 'otp' && (
        <Animated.View style={{ opacity: fadeAnimOTP }}>
          <View style={styles.otpContainer}>
            <Text style={styles.title}>Enter OTP</Text>
            <TextInput
              style={[styles.input, styles.otpInput]} // Adjust the width to make it twice as long
              placeholder="Enter OTP"
              onChangeText={(text) => setOTP(text)}
              value={otp}
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
          />
          <TextInput
            style={styles.input}
            placeholder="Confirm New Password"
            secureTextEntry
            onChangeText={(text) => setPassword2(text)}
            value={password2}
          />
          <Button title="Reset Password" onPress={handleResetPassword} />
        </>
      )}
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
  otpContainer: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  otpInput: {
    width: '160%', // Make it twice as long as before
  },
});

export default ForgotPasswordScreen;
