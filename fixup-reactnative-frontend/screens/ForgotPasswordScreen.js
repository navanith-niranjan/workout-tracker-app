import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Animated, Easing, KeyboardAvoidingView, ScrollView } from 'react-native';
import AuthService from '../services/AuthService';
import { useNavigation } from '@react-navigation/native';
import CustomButton from '../components/CustomButtonForLandingPage';
import { StatusBar } from 'expo-status-bar';
import CustomBackButton from '../components/CustomBackButton';

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

  const handleSendEmailForPasswordReset = async () => {
    if (!email) {
      console.log('Please fill in your email');
      return;
    }

    const sendEmailResult = await AuthService.handleSendEmailForPasswordReset(email);

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
      style={{ flex: 1 }}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      enabled
    >
      <ScrollView
      contentContainerStyle={styles.container}
      keyboardDismissMode="on-drag"
      >
      <CustomBackButton iconStyle={{position: 'absolute', right: 140, bottom: 220}}/>
        <StatusBar barStyle="dark-content" />
        {stage === 'email' && (
          <>
            <Text style={styles.title}>Forgot Password</Text>
            <View style={styles.inputContent}>
              <TextInput
                style={styles.input}
                keyboardType='email-address'
                placeholder="Enter your email"
                onChangeText={(text) => setEmail(text)}
                value={email}
                autoCapitalize="none"
              />
            </View>
            <CustomButton title="Send Email" onPress={handleSendEmailForPasswordReset} />
          </>
        )}

        {stage === 'otp' && (
          <>
            <Text style={styles.title}>Enter the code sent to your email</Text>
            <View style={styles.inputContent}>
              <TextInput
                style={styles.input} 
                keyboardType='numeric'
                onChangeText={(text) => setOTP(text)}
                value={otp}
                autoCapitalize="none"
              />
            </View>
          <CustomButton title="Verify OTP" onPress={handleVerifyOTP} />
          <TouchableOpacity onPress={handleSendEmailForPasswordReset}>
            <Text style={styles.resendOTP}>Resend one-time password?</Text>
          </TouchableOpacity>
          </>
        )}

        {stage === 'resetPassword' && (
          <>
            <Text style={styles.title}>Reset Password</Text>
            <View style={styles.inputContent}>
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
            </View>
            <CustomButton title="Reset Password" onPress={handleResetPassword} />
          </>
        )}
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
    fontSize: 19,
    marginBottom: 40,
    fontFamily: 'Montserrat',
    textAlign: 'center',
  },
  inputContent: {
    width: '80%',
    marginBottom: 40,
  },
  input: {
    height: 50,
    backgroundColor: 'white',
    borderColor: 'white',
    borderBottomColor: 'gray',
    borderWidth: 1,
    marginBottom: 10,
    paddingLeft: 10,
  },
  resendOTP: {
    color: 'blue', 
    textDecorationLine: 'underline', 
    marginTop: 10, 
    fontFamily: 'Montserrat',
  },
});

export default ForgotPasswordScreen;
