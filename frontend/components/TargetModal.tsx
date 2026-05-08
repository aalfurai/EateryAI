import { Modal, View, Text, TouchableOpacity, StyleSheet, Animated, Pressable, } from "react-native";
import { useEffect, useRef } from "react";
import { LinearGradient } from "expo-linear-gradient";

type Props = {
  visible: boolean;
  onClose: () => void;
};

export default function TargetModal({ visible, onClose, }: Props) {
  const slideAnim = useRef(new Animated.Value(400)).current;
  const fadeAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    slideAnim.setValue(400);
    fadeAnim.setValue(0);

    if (visible) {
      // sliding up
      Animated.parallel([
        Animated.timing(slideAnim, {
          toValue: 0,
          duration: 400,
          useNativeDriver: true,
        }),
        Animated.timing(fadeAnim, {
          toValue: 1,
          duration: 250,
          useNativeDriver: true,
        }),
      ]).start();

    } else {
      // sliding down
      Animated.parallel([
        Animated.timing(slideAnim, {
          toValue: 400,
          duration: 350,
          useNativeDriver: true,
        }),
        Animated.timing(fadeAnim, {
          toValue: 0,
          duration: 200,
          useNativeDriver: true,
        }),
      ]).start();
    }
  }, [visible]);

  return (
    <Modal
      visible={visible}
      transparent
      animationType="none"
    >
      {/* Overlay */}
      <Animated.View
        style={[
          styles.overlay,
          {
            opacity: fadeAnim,
          },
        ]}
      >
        {/* Click outside to close */}
        <Pressable
          style={StyleSheet.absoluteFill}
          onPress={onClose}
        />

        {/* Animated sheet */}
        <Animated.View
          style={[
            styles.modal,
            {
              transform: [
                { translateY: slideAnim },
              ],
            },
          ]}
        >
          <Text style={styles.title}>Meal Targets</Text>

          {/* Filter sections */}
          <View style={styles.priceContainer} />
          <View style={styles.calorieContainer} />
          <View style={styles.proteinContainer} />

          {/* Buttons */}
          <View style={styles.buttonsContainer}>

            <TouchableOpacity onPress={onClose}>
              <LinearGradient
                colors={["#4F4F4F", "#303030"]}
                style={styles.cancelButton}
              >
                <Text style={styles.closeText}>Cancel</Text>
              </LinearGradient>
            </TouchableOpacity>

            <TouchableOpacity>
              <LinearGradient
                colors={["#4F4F4F", "#303030"]}
                style={styles.applyButton}
              >
                <Text style={styles.closeText}>Apply Filters</Text>
              </LinearGradient>
            </TouchableOpacity>
          </View>
        </Animated.View>
      </Animated.View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: "rgba(0, 0, 0, 0.67)",
    justifyContent: "flex-end",
  },
  modal: {
    backgroundColor: "#111",
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
    padding: 24,
    minHeight: "80%",
    alignItems: "center",
  },
  title: {
    color: "white",
    fontSize: 22,
    fontWeight: "700",
    marginBottom: 24,
  },
  label: {
    color: "white",
    fontSize: 16,
    marginBottom: 12,
  },
  buttonsContainer: {
    flexDirection: "row",
    marginTop: 100,
  },
  cancelButton: {
    backgroundColor: "#4F4F4F",
    paddingVertical: 14,
    borderRadius: 14,
    borderColor: "#7C7C7C",
    borderWidth: 1,
    alignItems: "center",
    justifyContent: "center",
    width: 175,
    height: 64,
    marginRight: 10,
  },
  applyButton: {
    backgroundColor: "#4F4F4F",
    paddingVertical: 14,
    borderRadius: 14,
    borderColor: "#7C7C7C",
    borderWidth: 1,
    alignItems: "center",
    justifyContent: "center",
    width: 175,
    height: 64,
  },
  closeText: {
    color: "white",
    fontWeight: "600",
    fontSize: 14,
  },
  priceContainer: {
    backgroundColor: "#588CB7",
    paddingVertical: 14,
    borderRadius: 14,
    borderColor: "#A1B8C9",
    borderWidth: 1,
    alignItems: "center",
    justifyContent: "center",
    width: 360,
    height: 120,
    marginBottom: 16,
  },
  calorieContainer: {
    backgroundColor: "#3A9574",
    paddingVertical: 14,
    borderRadius: 14,
    borderColor: "#87B6AD",
    borderWidth: 1,
    alignItems: "center",
    justifyContent: "center",
    width: 360,
    height: 120,
    marginBottom: 16,
  },
  proteinContainer: {
    backgroundColor: "#6CA351",
    paddingVertical: 14,
    borderRadius: 14,
    borderColor: "#A1C9A1",
    borderWidth: 1,
    alignItems: "center",
    justifyContent: "center",
    width: 360,
    height: 120,
    marginBottom: 16,
  },
});