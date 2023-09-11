import React from 'react';
import { View, TouchableOpacity, Text, StyleSheet } from 'react-native';

const NavigationBar = ({ activeTab, onTabPress }) => {
  return (
    <View style={styles.container}>
      <TouchableOpacity
        style={[
          styles.tab,
          activeTab === 'Home' ? styles.activeTab : null,
        ]}
        onPress={() => onTabPress('Home')}
      >
        <Text
          style={[
            styles.tabText,
            activeTab === 'Home' ? styles.activeTabText : null,
          ]}
        >
          Home
        </Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={[
          styles.tab,
          activeTab === 'Workouts' ? styles.activeTab : null,
        ]}
        onPress={() => onTabPress('Workouts')}
      >
        <Text
          style={[
            styles.tabText,
            activeTab === 'Workouts' ? styles.activeTabText : null,
          ]}
        >
          Workouts
        </Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={[
          styles.tab,
          activeTab === 'Profile' ? styles.activeTab : null,
        ]}
        onPress={() => onTabPress('Profile')}
      >
        <Text
          style={[
            styles.tabText,
            activeTab === 'Profile' ? styles.activeTabText : null,
          ]}
        >
          Profile
        </Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    backgroundColor: 'white', 
    borderTopWidth: 1,
    borderTopColor: 'lightgray', 
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    height: 80, 
  },
  tab: {
    flex: 1,
    alignItems: 'center',
    paddingVertical: 10,
  },
  tabText: {
    color: 'gray', 
    fontSize: 14,
    paddingBottom: 20,
  },
  activeTab: {
    backgroundColor: 'white', 
  },
  activeTabText: {
    color: 'black', 
    fontWeight: 'bold', 
  },
});

export default NavigationBar;
