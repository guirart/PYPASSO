import { Fragment, type ReactNode } from 'react';
import { ScrollView, StyleSheet, Text, View } from 'react-native';
import { mono, useTheme, type Palette } from '@/lib/theme';

const KW = new Set('def return if elif else for while in not and or import from as lambda break continue pass True False None class'.split(' '));
const BI = new Set('print input len int str float range type max min sum list sorted'.split(' '));
const RE = /(#[^\n]*)|("(?:[^"\\\n]|\\.)*"?|'(?:[^'\\\n]|\\.)*'?)|(\b\d+(?:\.\d+)?\b)|([A-Za-z_À-ú][\wÀ-ú]*)/g;

export function highlight(src: string, t: Palette): ReactNode[] {
  const out: ReactNode[] = [];
  let last = 0; let m: RegExpExecArray | null; let k = 0;
  RE.lastIndex = 0;
  while ((m = RE.exec(src))) {
    if (m.index > last) out.push(src.slice(last, m.index));
    const color = m[1] ? t.cCom : m[2] ? t.cStr : m[3] ? t.cNum : KW.has(m[4]) ? t.cKw : BI.has(m[4]) ? t.cBi : undefined;
    out.push(color ? <Text key={k++} style={{ color, fontStyle: m[1] ? 'italic' : 'normal' }}>{m[0]}</Text> : m[0]);
    last = RE.lastIndex;
  }
  if (last < src.length) out.push(src.slice(last));
  return out;
}

/** Bloco de código. Lacunas "___" viram o que renderSlot devolver. */
export function CodeBlock({ code, renderSlot }: { code: string; renderSlot?: (i: number) => ReactNode }) {
  const t = useTheme();
  const parts = code.split('___');
  return (
    <View style={[styles.box, { backgroundColor: t.codeBg }]}>
      <ScrollView horizontal showsHorizontalScrollIndicator={false}>
        <Text style={[styles.code, { color: t.codeFg, fontFamily: mono }]}>
          {parts.map((p, i) => (
            <Fragment key={i}>
              {highlight(p, t)}
              {i < parts.length - 1 && renderSlot?.(i)}
            </Fragment>
          ))}
        </Text>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  box: { borderRadius: 14, paddingVertical: 14, paddingHorizontal: 16 },
  code: { fontSize: 15, lineHeight: 26 },
});
