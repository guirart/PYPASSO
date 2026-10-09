import { useEffect, useMemo, useRef } from 'react';
import { Animated, Easing, Platform } from 'react-native';
import { SvgXml } from 'react-native-svg';
import { trophySvg } from '@/lib/leagues';

/** Troféu de uma liga. `celebrate` faz ele entrar pulando e brilhando. */
export function Trophy({ tier, size = 64, locked, celebrate }: { tier: number; size?: number; locked?: boolean; celebrate?: boolean }) {
  const xml = useMemo(() => trophySvg(tier, { locked }), [tier, locked]);
  const pop = useRef(new Animated.Value(celebrate ? 0 : 1)).current;
  const wiggle = useRef(new Animated.Value(0)).current;
  useEffect(() => {
    if (!celebrate) return;
    const nd = Platform.OS !== 'web';
    Animated.sequence([
      Animated.spring(pop, { toValue: 1, friction: 4, tension: 110, useNativeDriver: nd }),
      Animated.loop(Animated.sequence([
        Animated.timing(wiggle, { toValue: 1, duration: 900, easing: Easing.inOut(Easing.quad), useNativeDriver: nd }),
        Animated.timing(wiggle, { toValue: 0, duration: 900, easing: Easing.inOut(Easing.quad), useNativeDriver: nd }),
      ])),
    ]).start();
  }, [celebrate, pop, wiggle]);
  const rotate = wiggle.interpolate({ inputRange: [0, 1], outputRange: ['-4deg', '4deg'] });
  return (
    <Animated.View style={{ width: size, height: size, transform: [{ scale: pop }, { rotate: celebrate ? rotate : '0deg' }] }}>
      <SvgXml xml={xml} width={size} height={size} />
    </Animated.View>
  );
}
