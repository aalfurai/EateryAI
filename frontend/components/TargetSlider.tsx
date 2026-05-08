import { View, Text, StyleSheet } from "react-native";
import Slider from "@react-native-community/slider";

type Props = {
  label: string;
  value: number;
  onChange: (v: number) => void;
  min?: number;
  max?: number;
  step?: number;
  format?: (v: number) => string;
};

export default function TargetSlider({
  label,
  value,
  onChange,
  min = 0,
  max = 100,
  step = 1,
  format,
}: Props) {
  return (
    <View style={styles.container}>
      {/* top row */}
      <View style={styles.topRow}>
        <Text style={styles.label}>{label}</Text>
        <Text style={styles.value}>
          {format ? format(value) : value}
        </Text>
      </View>

      <Slider
        style={{ width: "100%", height: 40 }}
        minimumValue={min}
        maximumValue={max}
        step={step}
        value={value}
        onValueChange={onChange}
        minimumTrackTintColor="#ffffff"
        maximumTrackTintColor="#ffffff73"
        thumbTintColor="#fff"
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginVertical: 12,
    width: "80%",
  },
  topRow: {
    flexDirection: "row",
    marginBottom: 6,
    justifyContent: "space-between",
  },
  label: {
    left: 0,
    color: "white",
    fontSize: 18,
    fontWeight: "700",
  },
  value: {
    right: 0,
    color: "white",
    fontSize: 16,
  },
});