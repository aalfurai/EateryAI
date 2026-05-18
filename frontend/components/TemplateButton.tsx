import { TouchableOpacity, Text, StyleSheet, View } from "react-native";
import { Ionicons } from "@expo/vector-icons";

export type Template = {
  id: string;
  label: string;
  sub: string;
  icon: keyof typeof Ionicons.glyphMap;
  categories: string[];
};

type Props = {
  template: Template;
  selected: boolean;
  onPress: () => void;
};

export default function TemplateButton({ template, selected, onPress }: Props) {
  return (
    <TouchableOpacity
      style={[styles.button, selected && styles.selected]}
      onPress={onPress}
      activeOpacity={0.7}
    >
      <Ionicons
        name={template.icon}
        size={24}
        color={selected ? "white" : "#555"}
        style={styles.icon}
      />
      <Text style={[styles.label, selected && styles.labelSelected]}>{template.label}</Text>
      <Text style={styles.sub}>{template.sub}</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  button: {
    flex: 1,
    backgroundColor: "#0d1117",
    borderRadius: 14,
    borderWidth: 1,
    borderColor: "#1e2530",
    padding: 16,
    minHeight: 110,
    justifyContent: "flex-end",
  },
  selected: {
    borderColor: "white",
    backgroundColor: "rgba(255,255,255,0.06)",
  },
  icon: {
    marginBottom: 10,
  },
  label: {
    color: "#555",
    fontSize: 15,
    fontWeight: "700",
    marginBottom: 4,
  },
  labelSelected: {
    color: "white",
  },
  sub: {
    color: "#3a3a3a",
    fontSize: 12,
  },
});
