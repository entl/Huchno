import {View, Text, SafeAreaView} from "react-native";
import React, {useEffect, useState} from "react";
import {useLocalSearchParams} from "expo-router";

const Page = () => {
    const { chatid } = useLocalSearchParams()
    return (
        <SafeAreaView>
            <View>
                <Text>{chatid}</Text>
            </View>
        </SafeAreaView>
    );
}

export default Page;