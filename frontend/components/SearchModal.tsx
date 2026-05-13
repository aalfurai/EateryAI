import { Modal, View, TextInput, TouchableOpacity, StyleSheet, } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

type Props = {
  visible: boolean;
  onClose: () => void;
  value: string;
  onChange: (text: string) => void;
  onSubmit: () => void;
};

export default function SearchModal({ visible, onClose, value, onChange, onSubmit }: Props) {
  const insets = useSafeAreaInsets();

  return (
    <Modal
      visible={visible}
      transparent
      animationType="fade"
    >
      <TouchableOpacity
        style={styles.overlay}
        activeOpacity={1}
        onPress={onClose}
      >
        {/* Prevent modal close when pressing inside */}
        <TouchableOpacity
          activeOpacity={1}
          style={[
            styles.modalContainer,
            { marginTop: insets.top + 12 },
          ]}
        >
          <View style={styles.modal}>
            <TextInput
              placeholder="Search..."
              placeholderTextColor="#777"
              value={value}
              onChangeText={onChange}
              style={styles.input}
              autoFocus
              returnKeyType="search"
              onSubmitEditing={onSubmit}
            />
          </View>
        </TouchableOpacity>
      </TouchableOpacity>
    </Modal>
  );
}

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: "rgba(0, 0, 0, 0.80)",
    alignItems: "center",
  },
  modalContainer: {
    width: "100%",
    alignItems: "center",
  },
  modal: {
    backgroundColor: "#111",
    borderColor: "#7C7C7C",
    borderWidth: 1,
    borderRadius: 30,
    justifyContent: "center",
    width: "92%",
    height: 50,
    paddingHorizontal: 16,
  },
  input: {
    color: "white",
    fontSize: 15,
  },
});