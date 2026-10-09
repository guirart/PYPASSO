import { useMemo, useRef, useState } from 'react';
import { Platform, Pressable, ScrollView, StyleSheet, Text, TextInput, View, type NativeSyntheticEvent, type TextInputKeyPressEventData } from 'react-native';
import { mono, type Palette } from '@/lib/theme';
import { highlight } from './CodeBlock';

/** Cores no estilo do tema escuro do VS Code. */
export const VS = {
  bg: '#1E1E1E', panel: '#252526', tab: '#2D2D2D', border: '#3C3C3C', text: '#D4D4D4', dim: '#858585',
  blue: '#3794FF', blueBar: '#007ACC', green: '#2EA043', red: '#F48771', info: '#9CDCFE', yellow: '#DCDCAA',
};
// Paleta de destaque de sintaxe (mesmas chaves usadas por highlight()).
const SYNTAX = { cKw: '#C586C0', cStr: '#CE9178', cNum: '#B5CEA8', cCom: '#6A9955', cBi: '#DCDCAA' } as Palette;

const FONT = 14;
const LINE = 21;
const CHAR = 8.6; // largura aproximada de um caractere monoespaçado em 14px
const PAD = 12;
const KEYS: { label: string; text: string; caret?: number }[] = [
  { label: '⇥', text: '    ' }, { label: ':', text: ':' }, { label: '( )', text: '()', caret: 1 }, { label: '[ ]', text: '[]', caret: 1 },
  { label: '" "', text: '""', caret: 1 }, { label: '=', text: ' = ' }, { label: '#', text: '# ' }, { label: '+', text: ' + ' },
  { label: '_', text: '_' }, { label: '{ }', text: '{}', caret: 1 }, { label: 'print', text: 'print()', caret: 6 },
];

type Sel = { start: number; end: number };

export type LineMarks = Record<number, 'error' | 'tip'>;

export function CodeEditorPane({ value, onChange, onRun, onCursor, marks }: {
  value: string;
  onChange: (v: string) => void;
  onRun?: () => void;
  onCursor?: (line: number, col: number) => void;
  /** Linhas destacadas pelo Pipo: erro (vermelho) ou dica (amarelo). */
  marks?: LineMarks;
}) {
  const sel = useRef<Sel>({ start: 0, end: 0 });
  const [forced, setForced] = useState<Sel | undefined>();
  const [viewW, setViewW] = useState(300);

  const lines = useMemo(() => value.split('\n'), [value]);
  const longest = useMemo(() => lines.reduce((m, l) => Math.max(m, l.length), 0), [lines]);
  const gutterW = Math.max(2, String(lines.length).length) * CHAR + 18 + (marks && Object.values(marks).includes('error') ? CHAR * 2 : 0);
  const width = Math.max(viewW - gutterW, (longest + 4) * CHAR + PAD * 2);
  const height = Math.max(lines.length + 3, 12) * LINE + PAD * 2;

  const place = (pos: number) => {
    sel.current = { start: pos, end: pos };
    setForced({ start: pos, end: pos });
  };

  const insert = (text: string, caret = text.length) => {
    const { start, end } = sel.current;
    onChange(value.slice(0, start) + text + value.slice(end));
    place(start + caret);
  };

  /** Ao apertar Enter, repete o recuo da linha anterior (+4 espaços depois de ":"). */
  const handleChange = (next: string) => {
    const prev = value;
    if (next.length === prev.length + 1) {
      let i = 0;
      while (i < prev.length && prev[i] === next[i]) i++;
      if (next[i] === '\n') {
        const lineStart = prev.lastIndexOf('\n', i - 1) + 1;
        const line = prev.slice(lineStart, i);
        let indent = (line.match(/^ */) ?? [''])[0];
        if (line.trimEnd().endsWith(':')) indent += '    ';
        if (indent) {
          onChange(next.slice(0, i + 1) + indent + next.slice(i + 1));
          place(i + 1 + indent.length);
          return;
        }
      }
    }
    onChange(next);
  };

  const onKey = (e: NativeSyntheticEvent<TextInputKeyPressEventData>) => {
    const ev = e as unknown as { nativeEvent: { key: string; ctrlKey?: boolean; metaKey?: boolean; shiftKey?: boolean }; preventDefault?: () => void };
    const { key, ctrlKey, metaKey } = ev.nativeEvent;
    if (key === 'Tab') { ev.preventDefault?.(); insert('    '); }
    else if (key === 'Enter' && (ctrlKey || metaKey)) { ev.preventDefault?.(); onRun?.(); }
  };

  const reportCursor = (pos: number) => {
    const before = value.slice(0, pos);
    const ln = before.split('\n').length;
    onCursor?.(ln, pos - before.lastIndexOf('\n'));
  };

  return (
    <View style={{ flex: 1, backgroundColor: VS.bg }}>
      <ScrollView style={{ flex: 1 }} keyboardShouldPersistTaps="handled" onLayout={(e) => setViewW(e.nativeEvent.layout.width)}>
        <View style={{ flexDirection: 'row' }}>
          <View style={[styles.gutter, { width: gutterW, height }]}>
            {lines.map((_, i) => (
              <Text key={i} style={[styles.ln, { fontFamily: mono }, marks?.[i + 1] === 'error' && { color: VS.red, fontWeight: '700' }, marks?.[i + 1] === 'tip' && { color: '#E2C08D' }]}>
                {marks?.[i + 1] === 'error' ? '● ' : ''}{i + 1}
              </Text>
            ))}
          </View>
          <ScrollView horizontal keyboardShouldPersistTaps="handled" showsHorizontalScrollIndicator>
            <View style={{ width, height }}>
              {/* Faixas das linhas marcadas pelo Pipo */}
              {marks && Object.entries(marks).map(([ln, kind]) => (
                <View key={ln} pointerEvents="none" style={{
                  position: 'absolute', left: 0, right: 0, height: LINE, top: PAD + (Number(ln) - 1) * LINE,
                  backgroundColor: kind === 'error' ? 'rgba(244,71,71,0.18)' : 'rgba(226,192,141,0.12)',
                  borderLeftWidth: 2, borderLeftColor: kind === 'error' ? VS.red : '#E2C08D',
                }} />
              ))}
              {/* Camada de destaque de sintaxe, por baixo do campo de texto */}
              <View pointerEvents="none" style={styles.layer}>
                <Text style={[styles.code, { fontFamily: mono, color: VS.text, width }]} selectable={false}>
                  {highlight(value + '\n', SYNTAX)}
                </Text>
              </View>
              <TextInput
                value={value}
                onChangeText={handleChange}
                onSelectionChange={(e) => { sel.current = e.nativeEvent.selection; reportCursor(e.nativeEvent.selection.start); if (forced) setForced(undefined); }}
                selection={forced}
                onKeyPress={onKey}
                multiline
                scrollEnabled={false}
                autoCapitalize="none"
                autoCorrect={false}
                autoComplete="off"
                spellCheck={false}
                textAlignVertical="top"
                selectionColor="rgba(55,148,255,0.45)"
                cursorColor={VS.text}
                underlineColorAndroid="transparent"
                accessibilityLabel="Editor de código"
                style={[styles.code, styles.input, { fontFamily: mono, width, height }, Platform.OS === 'web' && ({ outlineStyle: 'none', caretColor: VS.text } as object)]}
              />
            </View>
          </ScrollView>
        </View>
      </ScrollView>
      <ScrollView horizontal style={styles.keybar} contentContainerStyle={{ gap: 6, paddingHorizontal: 8 }} keyboardShouldPersistTaps="always" showsHorizontalScrollIndicator={false}>
        {KEYS.map((k) => (
          <Pressable key={k.label} onPress={() => insert(k.text, k.caret)} style={({ pressed }) => [styles.key, pressed && { backgroundColor: VS.border }]} accessibilityLabel={`Inserir ${k.label}`}>
            <Text style={{ color: VS.text, fontFamily: mono, fontSize: 14 }}>{k.label}</Text>
          </Pressable>
        ))}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  gutter: { paddingTop: PAD, paddingRight: 10, borderRightWidth: 1, borderRightColor: VS.border, backgroundColor: VS.bg },
  ln: { color: VS.dim, fontSize: FONT - 1, lineHeight: LINE, textAlign: 'right' },
  code: { fontSize: FONT, lineHeight: LINE, padding: PAD, paddingTop: PAD, margin: 0 },
  layer: { position: 'absolute', top: 0, left: 0 },
  input: { position: 'relative', zIndex: 1, color: 'transparent', backgroundColor: 'transparent', includeFontPadding: false, borderWidth: 0 },
  keybar: { flexGrow: 0, paddingVertical: 6, backgroundColor: VS.panel, borderTopWidth: 1, borderTopColor: VS.border },
  key: { borderWidth: 1, borderColor: VS.border, borderRadius: 6, paddingVertical: 6, paddingHorizontal: 12, backgroundColor: VS.tab },
});
