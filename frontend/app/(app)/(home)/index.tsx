import {Text, StyleSheet, SafeAreaView, View} from "react-native";
import React from "react";

const HomeIndex = () => {
    return (
        <SafeAreaView style={{flex: 1}}>
           <View><Text>INDEX HOME</Text></View>
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

export default HomeIndex;