import { Avatar as DBAvatar } from '@dicebear/core';
import { CRITTERS, avatarSvg, uniqueIds } from '@/lib/avatar';
import { useEffect, useMemo, useRef, useState } from 'react';
import { AccessibilityInfo, Animated, Easing, Platform, StyleSheet, Text, View } from 'react-native';
import { SvgXml } from 'react-native-svg';
import type { HostId } from '@/content/types';
import { useTheme } from '@/lib/theme';
import { PIPO, type PipoMood } from './pipo-art';
import { LOJA } from '@/lib/gamificacao';

const LOJA_MOLDURAS: Record<string, [string, string]> = Object.fromEntries(LOJA.filter((i) => i.cores).map((i) => [i.id, i.cores!]));

/**
 * Elenco e avatares: estilo "Critters" do DiceBear (domínio público, CC0 1.0).
 * O Pipo é a mascote original do PyPasso.
 */
const BASE = { animationVariant: 'none', borderRadius: 50, topProbability: 100, patternProbability: 100, cheeksProbability: 100 };

type CastMember = { name: string; look: Record<string, string>; face: [eyes: string, mouth: string] };
export const CAST: Record<Exclude<HostId, 'pipo'>, CastMember> = {
  ana: { name: 'Ana', face: ['bigPupils', 'smile'], look: { bodyVariant: 'round', topVariant: 'earsRound', patternVariant: 'belly', cheeksVariant: 'blush', bodyColor: '#fda4af', accentColor: '#fdba74', backgroundColor: '#be185d' } },
  caio: { name: 'Caio', face: ['round', 'grin'], look: { bodyVariant: 'block', topVariant: 'horns', patternVariant: 'dots', cheeksVariant: 'freckles', bodyColor: '#7dd3fc', accentColor: '#fcd34d', backgroundColor: '#1d4ed8' } },
  bia: { name: 'Bia', face: ['happy', 'tinySmile'], look: { bodyVariant: 'bell', topVariant: 'sprout', patternVariant: 'speckles', cheeksVariant: 'blushBig', bodyColor: '#bef264', accentColor: '#f0abfc', backgroundColor: '#047857' } },
  teo: { name: 'Téo', face: ['wide', 'tooth'], look: { bodyVariant: 'squat', topVariant: 'antennae', patternVariant: 'stripes', cheeksVariant: 'blush', bodyColor: '#c4b5fd', accentColor: '#5eead4', backgroundColor: '#6d28d9' } },
};
const MOOD_FACE: Record<Exclude<PipoMood, 'happy'>, [string, string]> = {
  cheer: ['happy', 'laugh'], sad: ['sleepy', 'sad'], think: ['sideeye', 'ooh'],
};

const render = (opts: Record<string, unknown>) => uniqueIds(new DBAvatar(CRITTERS, { ...BASE, ...opts }).toString());

/** Avatar de usuário: um Critter gerado a partir da semente. */
export function Avatar({ seed, size = 64 }: { seed: string; size?: number }) {
  const xml = useMemo(() => avatarSvg(seed), [seed]);
  return <SvgXml xml={xml} width={size} height={size} />;
}

/** Personagem do elenco, com expressão. */
export function CastFace({ id, size = 64, mood = 'happy' }: { id: Exclude<HostId, 'pipo'>; size?: number; mood?: PipoMood }) {
  const xml = useMemo(() => {
    const c = CAST[id];
    const [eyesVariant, mouthVariant] = mood === 'happy' ? c.face : MOOD_FACE[mood];
    return render({ seed: id, ...c.look, eyesVariant, mouthVariant });
  }, [id, mood]);
  return <SvgXml xml={xml} width={size} height={size} />;
}

/**
 * Pipo, a mascote. Pisca de tempos em tempos e "respira" (sobe e desce de leve).
 * mood: happy (padrão), cheer (comemorando), sad (triste), think (pensando).
 */
export function Mascot({ size = 64, mood = 'happy', animated = true }: { size?: number; mood?: PipoMood; animated?: boolean }) {
  const [blink, setBlink] = useState(false);
  const bob = useRef(new Animated.Value(0)).current;
  const pop = useRef(new Animated.Value(mood === 'cheer' ? 0.6 : 1)).current;

  useEffect(() => {
    if (!animated) return;
    let alive = true;
    let reduce = false;
    AccessibilityInfo.isReduceMotionEnabled().then((r) => { reduce = r; if (r) bob.stopAnimation(); }).catch(() => {});
    const loop = Animated.loop(Animated.sequence([
      Animated.timing(bob, { toValue: 1, duration: 1300, easing: Easing.inOut(Easing.quad), useNativeDriver: Platform.OS !== 'web' }),
      Animated.timing(bob, { toValue: 0, duration: 1300, easing: Easing.inOut(Easing.quad), useNativeDriver: Platform.OS !== 'web' }),
    ]));
    loop.start();
    if (mood === 'cheer') Animated.spring(pop, { toValue: 1, friction: 4, tension: 120, useNativeDriver: Platform.OS !== 'web' }).start();
    let t: ReturnType<typeof setTimeout>;
    const schedule = () => {
      t = setTimeout(() => {
        if (!alive) return;
        if (!reduce && (mood === 'happy' || mood === 'think')) { setBlink(true); setTimeout(() => alive && setBlink(false), 140); }
        schedule();
      }, 2200 + Math.random() * 3000);
    };
    schedule();
    return () => { alive = false; clearTimeout(t); loop.stop(); };
  }, [animated, mood, bob, pop]);

  const xml = blink && mood === 'happy' ? PIPO.blink : PIPO[mood];
  const translateY = bob.interpolate({ inputRange: [0, 1], outputRange: [0, -size * 0.035] });
  const scaleY = bob.interpolate({ inputRange: [0, 1], outputRange: [1, 1.015] });
  return (
    <Animated.View style={{ width: size, height: size, transform: animated ? [{ translateY }, { scaleY }, { scale: pop }] : [] }}>
      <SvgXml xml={xml} width={size} height={size} />
    </Animated.View>
  );
}

export function HostFace({ host, size = 72, mood }: { host: HostId; size?: number; mood?: PipoMood }) {
  if (host === 'pipo') return <Mascot size={size} mood={mood} />;
  return <CastFace id={host} size={size} mood={mood} />;
}

export const hostName = (h: HostId) => (h === 'pipo' ? 'Pipo' : CAST[h].name);

/** Personagem "falando" a pergunta num balão, como nas lições de idiomas. */
export function SpeakingHost({ host, text, mood }: { host: HostId; text: string; mood?: PipoMood }) {
  const t = useTheme();
  return (
    <View style={styles.row}>
      <HostFace host={host} size={76} mood={mood} />
      <View style={[styles.bubble, { borderColor: t.line, backgroundColor: t.surface }]}>
        <View style={[styles.tail, { borderRightColor: t.line }]} />
        <Text style={[styles.name, { color: t.brand }]}>{hostName(host)}</Text>
        <Text style={[styles.text, { color: t.ink }]}>{text}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: 'row', alignItems: 'flex-end', gap: 12 },
  bubble: { flex: 1, borderWidth: 2, borderRadius: 16, paddingVertical: 12, paddingHorizontal: 14 },
  tail: { position: 'absolute', left: -10, bottom: 14, width: 0, height: 0, borderTopWidth: 8, borderBottomWidth: 8, borderRightWidth: 10, borderTopColor: 'transparent', borderBottomColor: 'transparent' },
  name: { fontSize: 12, fontWeight: '800', letterSpacing: 0.8, textTransform: 'uppercase', marginBottom: 2 },
  text: { fontSize: 19, fontWeight: '700', lineHeight: 25 },
});

/** Avatar com a moldura comprada na Loja (anel colorido em volta). */
export function AvatarMoldura({ seed, size = 64, moldura }: { seed: string; size?: number; moldura?: string }) {
  const cores = moldura ? LOJA_MOLDURAS[moldura] : undefined;
  if (!cores) return <Avatar seed={seed} size={size} />;
  const anel = Math.max(4, Math.round(size * 0.07));
  return (
    <View style={{ width: size + anel * 4, height: size + anel * 4, borderRadius: 999, backgroundColor: cores[0], padding: anel, alignItems: 'center', justifyContent: 'center' }}>
      <View style={{ width: size + anel * 2, height: size + anel * 2, borderRadius: 999, backgroundColor: cores[1], padding: anel, alignItems: 'center', justifyContent: 'center' }}>
        <View style={{ width: size, height: size, borderRadius: 999, overflow: 'hidden' }}><Avatar seed={seed} size={size} /></View>
      </View>
    </View>
  );
}
