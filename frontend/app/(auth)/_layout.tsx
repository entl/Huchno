import {Slot, Stack} from "expo-router";
import {SafeAreaProvider} from "react-native-safe-area-context";
import {DarkTheme, DefaultTheme, ThemeProvider} from "@react-navigation/native";
import {useColorScheme} from "react-native";

const AuthLayout = () => {
    return <AuthLayoutNav></AuthLayoutNav>
}

const AuthLayoutNav = () => {
    const colorScheme = useColorScheme();
    return (
        <Stack screenOptions={{
            headerShown: true,
        }}>
            <Stack.Screen name="login" options={{
                title: "Sign In"
            }}></Stack.Screen>
            <Stack.Screen name="register" options={{
                headerTitle: "Register"
            }}></Stack.Screen>
        </Stack>
    )
}

export default AuthLayout;