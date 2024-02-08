import {Stack} from "expo-router";
import {MaterialIcons} from "@expo/vector-icons";


const ChatLayout = () => {
    return <ChatLayoutNav></ChatLayoutNav>
}

const ChatLayoutNav = () => {
    return (
        <Stack>
            <Stack.Screen name="index"
                         options={{
                                // hide title
                                headerTitle: 'My Chats',
                                headerRight: () => (
                                    <MaterialIcons name="add" size={24} color="black"/>
                                ),
                         }}
            />
            <Stack.Screen name="[chatid]"
                         options={{
                             title: "Chat"
                         }}
            />
        </Stack>
    )
}

export default ChatLayout;