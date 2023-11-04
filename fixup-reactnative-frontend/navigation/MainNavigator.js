import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import HomeScreen from '../screens/HomeScreen';
import WorkoutHistoryScreen from '../screens/WorkoutHistoryScreen';
import CreateWorkoutScreen from '../screens/CreateWorkoutScreen';
import ProfileScreen from '../screens/ProfileScreen';

const Tab = createBottomTabNavigator();

const MainNavigator = () => {
  return (
    <Tab.Navigator screenOptions={{ headerShown: false }} options={{ gestureEnabled: false }}>
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="WorkoutHistory" component={WorkoutHistoryScreen} />
      <Tab.Screen name="CreateWorkout" component={CreateWorkoutScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
};

export default MainNavigator;