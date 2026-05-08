import { Modal, View, Text, TouchableOpacity, StyleSheet, } from "react-native";
import { LinearGradient } from "expo-linear-gradient";

type Props = {
  visible: boolean;
  onClose: () => void;
};

export default function FilterModal({
  visible,
  onClose,
}: Props) {
  return (
    <Modal
      visible={visible}
      transparent
      animationType="fade"
    >
      {/* Dark overlay */}
      <TouchableOpacity
        style={styles.overlay}
        activeOpacity={1}
        onPress={onClose}
      >
        {/* Prevent closing when pressing panel */}
        <TouchableOpacity activeOpacity={1}>
          <View style={styles.modal}>
            <Text style={styles.title}>Filters</Text>

            {/* TODO: Add sliders/toggles later */}
            <View style={styles.priceContainer}/>
            <View style={styles.calorieContainer}/>
            <View style={styles.proteinContainer}/>

            {/* Selection buttons */}
            <View style={styles.buttonsContainer}>
              <TouchableOpacity
                onPress={onClose}
              >
                <LinearGradient
                  colors={["#4F4F4F", "#303030"]}
                  style={styles.cancelButton}
                >
                  <Text style={styles.closeText}>Cancel</Text>
                </LinearGradient>
              </TouchableOpacity>

              <TouchableOpacity
                // TODO: apply filters
              >
                <LinearGradient
                  colors={["#4F4F4F", "#303030"]}
                  style={styles.applyButton}
                >
                  <Text style={styles.closeText}>Apply Filters</Text>
                </LinearGradient>
              </TouchableOpacity>
            </View>
          </View>
        </TouchableOpacity>
      </TouchableOpacity>
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
    minHeight: 670,
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
    marginTop: 80,
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