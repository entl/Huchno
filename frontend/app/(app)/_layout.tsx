import {Tabs} from "expo-router";
import {MaterialIcons} from "@expo/vector-icons";
import {ACCENT_YELLOW_COLOR, SECONDARY_COLOR} from "@env"


const HomeLayout = () => {
    return <HomeLayoutNav></HomeLayoutNav>
}

const HomeLayoutNav = () => {
    // add separator to tabs
    return (

        <Tabs screenOptions={{
            headerShown: false,
            tabBarStyle: {
                height: 60,
                paddingTop: 10,
                paddingBottom: 10,
                borderTopWidth: 1,
                borderTopColor: "#f0f0f0",
                backgroundColor: '#fff',
                elevation: 10,
                shadowColor: '#000',
                shadowOpacity: 0.05,
                shadowRadius: 10,
                shadowOffset: {
                    height: 1,
                    width: 0,
                },
            },
            tabBarItemStyle: {
                borderRightWidth:3,
                height:20,
                borderRightColor:`${SECONDARY_COLOR}`,
                alignItems: 'center',
                justifyContent: 'center',
                shadowColor: '#000',
                shadowOpacity: 0.05,
                shadowRadius: 10,
                shadowOffset: {
                    height: 1,
                    width: 0,
                },
            },
            tabBarActiveTintColor: ACCENT_YELLOW_COLOR,
            // tabBarInactiveTintColor: inactiveColor,
        }}
        >
            <Tabs.Screen name="(home)/index"
                          options={{
                              headerShown: false,
                              tabBarLabelStyle: {display: 'none'},
                              tabBarIcon: ({color, size}) => (
                                  <MaterialIcons name="home" color={color} size={size}/>
                              ),
                          }}
            />
            <Tabs.Screen name="chat"
                         options={{
                             headerShown: false,
                             tabBarLabelStyle: {display: 'none'},
                             tabBarIcon: ({color, size}) => (
                                 <MaterialIcons name="chat" color={color} size={size}/>
                             ),
                         }}
            />
            <Tabs.Screen name="profile"
                         options={{
                             headerShown: false,
                             tabBarLabelStyle: {display: 'none'},
                             tabBarIcon: ({color, size}) => (
                                 <MaterialIcons name="person" color={color} size={size}/>
                             ),
                         }}
            />
        </Tabs>
    )
}

export default HomeLayout;