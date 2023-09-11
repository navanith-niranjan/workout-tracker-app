import { createStackNavigator } from '@react-navigation/stack';
import LandingScreen from '../screens/LandingScreen';
import RegistrationScreen from '../screens/RegistrationScreen';
import OTPVerifyScreen from '../screens/OTPVerifyScreen';
import LoginScreen from '../screens/LoginScreen';
import ForgotPasswordScreen from '../screens/ForgotPasswordScreen';
import HomeScreen from '../screens/HomeScreen'

const Stack = createStackNavigator();

const AuthNavigator = () => {
  return (
    <Stack.Navigator>
      <Stack.Screen name="Landing" component={LandingScreen} options={{ headerShown: false }}/>
      <Stack.Screen name="SignUp" component={RegistrationScreen} options={{ headerShown: false }}/>
      <Stack.Screen name="OTPVerify" component={OTPVerifyScreen} options={{ headerShown: false }}/>
      <Stack.Screen name="SignIn" component={LoginScreen} options={{ headerShown: false }}/>
      <Stack.Screen name="ForgotPassword" component={ForgotPasswordScreen} options={{ headerShown: false }}/>
      <Stack.Screen name="Home" component={HomeScreen} />
    </Stack.Navigator>
  );
};

export default AuthNavigator;
