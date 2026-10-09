import { Pressable, StyleSheet, Text, View, type StyleProp, type ViewStyle } from 'react-native';
import { useTheme } from '@/lib/theme';

type Variant = 'brand' | 'good' | 'bad' | 'ghost' | 'white' | 'sun';

/** Botão com "degrau" embaixo que afunda ao tocar, no estilo dos apps de idiomas. */
export function Button3D({ label, onPress, variant = 'brand', disabled, style }: {
  label: string; onPress?: () => void; variant?: Variant; disabled?: boolean; style?: StyleProp<ViewStyle>;
}) {
  const t = useTheme();
  const map: Record<Variant, [string, string, string]> = {
    brand: [t.brand, t.brandDeep, '#fff'],
    good: [t.good, t.goodDeep, '#fff'],
    bad: [t.bad, t.badDeep, '#fff'],
    ghost: [t.surface, t.line, t.muted],
    white: ['#fff', 'rgba(0,0,0,0.18)', t.brand],
    sun: ['#fff', 'rgba(0,0,0,0.15)', t.sunDeep],
  };
  const [bg, deep, fg] = disabled ? [t.line, t.lineDeep, t.muted] : map[variant];
  return (
    <Pressable onPress={onPress} disabled={disabled} accessibilityRole="button" style={style}>
      {({ pressed }) => (
        <View style={[styles.base, {
          backgroundColor: bg,
          borderBottomColor: deep,
          borderBottomWidth: pressed && !disabled ? 0 : 4,
          marginTop: pressed && !disabled ? 4 : 0,
          borderWidth: variant === 'ghost' ? 2 : 0,
          borderColor: t.line,
        }]}>
          <Text style={[styles.label, { color: fg }]}>{label.toUpperCase()}</Text>
        </View>
      )}
    </Pressable>
  );
}

const styles = StyleSheet.create({
  base: { borderRadius: 14, paddingVertical: 13, paddingHorizontal: 18, alignItems: 'center' },
  label: { fontWeight: '800', fontSize: 15, letterSpacing: 0.8 },
});
