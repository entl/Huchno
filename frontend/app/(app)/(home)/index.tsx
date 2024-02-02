import {Text, Animated, StyleSheet, SafeAreaView} from "react-native";
import React, {useEffect, useState} from "react";
import axios from "axios";
import ScrollView = Animated.ScrollView;
import {Link} from "expo-router";
import {UserFromApi} from "@/app/_schemas";

import {useAuth} from "@/context/AuthContext";
import {API_HOST} from "@env";
import {getUsers} from "@/app/_queries";

const Index = () => {
    const [userData, setUserData] = useState<UserFromApi[]>([]);
    const {access_token, onLogout} = useAuth();

    useEffect(() => {
        const fetchData = async () => {
            try {
                let users = await getUsers(access_token);
                setUserData(users);
            } catch (error) {
                console.error('Error fetching user data:', error);
            }
        };
        fetchData();
    }, []);

    return (
        <SafeAreaView style={{flex: 1}}>
            <ScrollView style={styles.container}>
                {userData.map((user) => (
                    <Link style={styles.group}
                          href={{
                              pathname: "/(app)/chat/[chatid]",
                              params: {chatid: user.id},
                          }}>
                        <Text>{user.username}</Text>
                    </Link>
                ))}
            </ScrollView>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#F8F5EA',
        padding: 10,
    },
    group: {
        flexDirection: 'row',
        gap: 10,
        alignItems: 'center',
        backgroundColor: "#fff",
        padding: 10,
        borderRadius: 10,
        marginBottom: 10,
        shadowColor: '#000',
        shadowOffset: {width: 0, height: 1},
        shadowOpacity: 0.22,
        shadowRadius: 2.22,
    }
});

export default Index;