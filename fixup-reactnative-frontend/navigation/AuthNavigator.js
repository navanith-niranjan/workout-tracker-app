import { createStackNavigator } from '@react-navigation/stack';
import LoginScreen from '../screens/LoginScreen';

const Stack = createStackNavigator();

const AuthNavigator = () => {
  return (
    <Stack.Navigator>
      <Stack.Screen name="Login" component={LoginScreen} />
      {/* Add more screens for registration, forgot password, OTP verification, etc. */}
    </Stack.Navigator>
  );
};

export default AuthNavigator;