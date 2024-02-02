import {Stack} from "expo-router";

const HomeLayout = () => {
    return <HomeLayoutNav></HomeLayoutNav>
}

const HomeLayoutNav = () => {
    return (
        <Stack>
            <Stack.Screen name="(home)/index"
                          options={{
                              title: "Home"
                          }}
            />
            <Stack.Screen name="chat/[chatid]"
                          options={{
                              title: "Chat"
                          }}
            />
        </Stack>
    )
}

export default HomeLayout;