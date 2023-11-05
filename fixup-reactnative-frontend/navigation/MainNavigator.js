import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Image } from 'react-native'
import dashboardIcon from '../assets/dashboard.png';
import historyIcon from '../assets/history.png';
import profileIcon from '../assets/profile.png';
import HomeScreen from '../screens/HomeScreen';
import WorkoutHistoryScreen from '../screens/WorkoutHistoryScreen';
import ProfileScreen from '../screens/ProfileScreen';

const Tab = createBottomTabNavigator();

const MainNavigator = () => {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({

        tabBarIcon: ({ focused }) => {
          let iconSource, iconSize, iconColor;

          if (route.name === 'Home') {
            iconSource = dashboardIcon;
            iconSize = { width: 20, height: 20 };
          } else if (route.name === 'WorkoutHistory') {
            iconSource = historyIcon;
            iconSize = { width: 24, height: 24 };
          } else if (route.name === 'Profile') {
            iconSource = profileIcon;
            iconSize = { width: 20, height: 20 };
          }

          iconColor = focused ? 'black' : 'gray';

          return (
            <Image source={iconSource} style={{ ...iconSize, tintColor: iconColor }} />
          );
        },
        tabBarLabelStyle: { display: 'none' },
        headerShown: false, 
      })}
    >
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="WorkoutHistory" component={WorkoutHistoryScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
};

export default MainNavigator;