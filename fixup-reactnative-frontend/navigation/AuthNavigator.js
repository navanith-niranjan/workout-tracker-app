import { createStackNavigator } from '@react-navigation/stack';
import LandingScreen from '../screens/LandingScreen';
import RegistrationScreen from '../screens/RegistrationScreen';
import OTPVerifyScreen from '../screens/OTPVerifyScreen';
import LoginScreen from '../screens/LoginScreen';
import ForgotPasswordScreen from '../screens/ForgotPasswordScreen';

const Stack = createStackNavigator();

const AuthNavigator = () => {
  return (
    <Stack.Navigator>
      <Stack.Screen name="Landing" component={LandingScreen} />
      <Stack.Screen name="SignUp" component={RegistrationScreen} />
      {/* <Stack.Screen name="OTPVerify" component={OTPVerifyScreen} /> */}
      <Stack.Screen name="SignIn" component={LoginScreen} />
      {/* <Stack.Screen name="ForgotPassword" component={ForgotPasswordScreen} /> */}
    </Stack.Navigator>
  );
};

export default AuthNavigator;