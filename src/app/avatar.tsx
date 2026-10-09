import { router } from 'expo-router';
import { useEffect, useMemo, useRef, useState } from 'react';
import { Animated, Platform, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { SvgXml } from 'react-native-svg';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Button3D } from '@/components/Button3D';
import { COLORS, PARTS, encodeLook, lockTier, lookSvg, partLabel, randomLook, resolveLook, type Look, type PartKey } from '@/lib/avatar';
import { leagueOf } from '@/lib/leagues';
import { useGame } from '@/lib/store';
import { saveProfileRemote } from '@/lib/sync';
import { useTheme } from '@/lib/theme';
import { Icone } from '@/components/Icone';

type Tab = PartKey | 'cores';
const TABS: { id: Tab; label: string }[] = [
  ...PARTS.map((p) => ({ id: p.key as Tab, label: p.label })),
  { id: 'cores', label: 'Cores' },
];

/** Editor de avatar: monta o Critter por partes e cores. */
export default function AvatarEditor() {
  const t = useTheme();
  const insets = useSafeAreaInsets();
  const { avatarSeed, league, bestLeague, setProfile } = useGame();
  const unlocked = Math.max(league, bestLeague);
  const [look, setLook] = useState<Look>(() => resolveLook(avatarSeed));
  const [tab, setTab] = useState<Tab>('body');
  const [hint, setHint] = useState<string | null>(null);
  const bump = useRef(new Animated.Value(1)).current;
  const original = useMemo(() => JSON.stringify(resolveLook(avatarSeed)), [avatarSeed]);
  const changed = JSON.stringify(look) !== original;

  const preview = useMemo(() => lookSvg(look), [look]);
  useEffect(() => {
    bump.setValue(0.9);
    Animated.spring(bump, { toValue: 1, friction: 4, tension: 160, useNativeDriver: Platform.OS !== 'web' }).start();
  }, [preview, bump]);

  const set = (patch: Partial<Look>) => { setLook((l) => ({ ...l, ...patch })); setHint(null); };
  const save = () => {
    setProfile({ avatarSeed: encodeLook(look) });
    saveProfileRemote().catch(() => {});
    router.back();
  };

  return (
    <View style={{ flex: 1, backgroundColor: t.bg }}>
      <View style={[styles.top, { paddingTop: insets.top + 8, borderBottomColor: t.line }]}>
        <Pressable onPress={() => router.back()} hitSlop={10} accessibilityLabel="Fechar sem salvar">
          <Text style={{ color: t.muted, fontSize: 22, fontWeight: '800' }}>✕</Text>
        </Pressable>
        <Text style={[styles.title, { color: t.ink }]}>Seu avatar</Text>
        <View style={{ width: 22 }} />
      </View>

      <View style={styles.previewRow}>
        <Animated.View style={{ transform: [{ scale: bump }] }}>
          <SvgXml xml={preview} width={150} height={150} />
        </Animated.View>
        <View style={{ gap: 10, flex: 1 }}>
          <Button3D label="Sortear" variant="ghost" onPress={() => set(randomLook(unlocked))} />
          <Button3D label={changed ? 'Salvar' : 'Pronto'} onPress={changed ? save : () => router.back()} />
        </View>
      </View>

      <ScrollView horizontal showsHorizontalScrollIndicator={false} style={{ flexGrow: 0 }} contentContainerStyle={styles.tabs}>
        {TABS.map((tb) => {
          const on = tb.id === tab;
          return (
            <Pressable key={tb.id} onPress={() => setTab(tb.id)} accessibilityRole="tab" accessibilityState={{ selected: on }}
              style={[styles.tab, { backgroundColor: on ? t.brand : t.surface, borderColor: on ? t.brand : t.line }]}>
              <Text style={{ color: on ? '#fff' : t.ink, fontWeight: '800' }}>{tb.label}</Text>
            </Pressable>
          );
        })}
      </ScrollView>
      {hint ? <Text style={[styles.hint, { color: t.sunDeep }]}>{hint}</Text> : null}

      <ScrollView contentContainerStyle={styles.gridWrap}>
        {tab === 'cores' ? (
          <View style={{ gap: 18 }}>
            {([['bg', 'Fundo'], ['bodyColor', 'Corpo'], ['accentColor', 'Detalhes']] as const).map(([key, label]) => (
              <View key={key} style={{ gap: 8 }}>
                <Text style={[styles.label, { color: t.muted }]}>{label.toUpperCase()}</Text>
                <View style={styles.swatches}>
                  {COLORS[key].map((c) => {
                    const on = look[key] === c;
                    return (
                      <Pressable key={c} onPress={() => set({ [key]: c } as Partial<Look>)} accessibilityLabel={`${label}: ${c}`}
                        style={[styles.swatch, { backgroundColor: c, borderColor: on ? t.ink : 'transparent' }]}>
                        {on ? <Text style={{ color: '#fff', fontWeight: '900', textShadowColor: '#000', textShadowRadius: 3 }}>✓</Text> : null}
                      </Pressable>
                    );
                  })}
                </View>
              </View>
            ))}
          </View>
        ) : (
          <View style={styles.grid}>
            {PARTS.find((p) => p.key === tab)!.options.map((v) => {
              const part = tab as PartKey;
              const need = lockTier(part, v);
              const locked = need > unlocked;
              const on = look[part] === v;
              return (
                <Option key={v} look={{ ...look, [part]: v }} label={partLabel(v, part)} selected={on} locked={locked}
                  onPress={() => (locked ? setHint(`${partLabel(v, part)} libera quando você chegar na Liga ${leagueOf(need).gem} (${leagueOf(need).title}).`) : set({ [part]: v } as Partial<Look>))} />
              );
            })}
          </View>
        )}
      </ScrollView>
    </View>
  );
}

function Option({ look, label, selected, locked, onPress }: { look: Look; label: string; selected: boolean; locked: boolean; onPress: () => void }) {
  const t = useTheme();
  const xml = useMemo(() => lookSvg(look), [look]);
  return (
    <Pressable onPress={onPress} accessibilityLabel={`${label}${locked ? ', bloqueado' : selected ? ', escolhido' : ''}`}
      style={[styles.opt, { backgroundColor: t.surface, borderColor: selected ? t.brand : t.line }, selected && { borderWidth: 3 }]}>
      <View style={{ opacity: locked ? 0.35 : 1 }}>
        <SvgXml xml={xml} width={64} height={64} />
      </View>
      {locked ? <View style={styles.lock}><Icone nome="cadeado" size={14} color="#fff" /></View> : null}
      <Text style={{ color: selected ? t.brand : t.ink, fontSize: 11, fontWeight: '800', textAlign: 'center' }} numberOfLines={2}>{label}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  top: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: 16, paddingBottom: 10, borderBottomWidth: 2 },
  title: { fontSize: 18, fontWeight: '900' },
  previewRow: { flexDirection: 'row', alignItems: 'center', gap: 16, padding: 16, maxWidth: 560, width: '100%', alignSelf: 'center' },
  tabs: { gap: 8, paddingHorizontal: 16, paddingBottom: 10 },
  tab: { borderWidth: 2, borderRadius: 99, paddingHorizontal: 14, paddingVertical: 7 },
  hint: { paddingHorizontal: 16, fontWeight: '800', fontSize: 13 },
  gridWrap: { padding: 16, paddingBottom: 48, maxWidth: 560, width: '100%', alignSelf: 'center' },
  grid: { flexDirection: 'row', flexWrap: 'wrap', gap: 10, justifyContent: 'flex-start' },
  opt: { width: 88, alignItems: 'center', gap: 4, borderWidth: 2, borderRadius: 14, paddingVertical: 8, paddingHorizontal: 4 },
  lock: { position: 'absolute', top: 30, fontSize: 20 },
  label: { fontSize: 12, fontWeight: '900', letterSpacing: 1 },
  swatches: { flexDirection: 'row', flexWrap: 'wrap', gap: 10 },
  swatch: { width: 40, height: 40, borderRadius: 20, borderWidth: 3, alignItems: 'center', justifyContent: 'center' },
});
