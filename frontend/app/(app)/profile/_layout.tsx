import {Stack} from "expo-router";
import {MaterialIcons} from "@expo/vector-icons";


const ChatLayout = () => {
    return <ChatLayoutNav></ChatLayoutNav>
}

const ChatLayoutNav = () => {
    return (
        <Stack>
            <Stack.Screen name="chat/index"
                          options={{
                              title: "Home"
                          }}
            />
        </Stack>
    )
}

export default ChatLayout;