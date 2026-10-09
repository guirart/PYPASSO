import { useState } from 'react';
import { Modal, Pressable, StyleSheet, Text, TextInput, View } from 'react-native';
import { Button3D } from './Button3D';
import { Icone } from './Icone';
import { TIPOS_RELATO, useTeste, type TipoRelato } from '@/lib/teste';
import { useTheme } from '@/lib/theme';

/** "Travei aqui": a pessoa conta o que aconteceu neste exercício. */
export function RelatoModal({ visivel, fechar, exId, licao }: { visivel: boolean; fechar: () => void; exId?: string; licao?: string }) {
  const t = useTheme();
  const relatar = useTeste((s) => s.relatar);
  const [tipo, setTipo] = useState<TipoRelato | null>(null);
  const [texto, setTexto] = useState('');
  const [enviado, setEnviado] = useState(false);
  const sair = () => { setTipo(null); setTexto(''); setEnviado(false); fechar(); };
  return (
    <Modal visible={visivel} transparent animationType="fade" onRequestClose={sair}>
      <Pressable style={styles.fundo} onPress={sair} accessibilityLabel="Fechar">
        <Pressable style={[styles.card, { backgroundColor: t.bg, borderColor: t.line }]} onPress={() => {}}>
          {enviado ? (
            <>
              <View style={{ alignItems: 'center' }}><Icone nome="coracao" size={48} color={t.brand} /></View>
              <Text style={[styles.h, { color: t.ink, textAlign: 'center' }]}>Valeu! O Pipo anotou.</Text>
              <Text style={{ color: t.muted, fontWeight: '600', textAlign: 'center' }}>Esses relatos mostram o que precisa melhorar no PyPasso.</Text>
              <Button3D label="Voltar ao exercício" onPress={sair} />
            </>
          ) : (
            <>
              <View style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}><Icone nome="bandeira" size={24} color={t.bad} /><Text style={[styles.h, { color: t.ink }]}>Travei aqui</Text></View>
              <Text style={{ color: t.muted, fontWeight: '600' }}>O que aconteceu? Isso não gasta vidas.</Text>
              {TIPOS_RELATO.map((op) => (
                <Pressable key={op.id} onPress={() => setTipo(op.id)} accessibilityRole="radio" accessibilityState={{ checked: tipo === op.id }}
                  style={[styles.op, { borderColor: tipo === op.id ? t.brand : t.line, backgroundColor: tipo === op.id ? t.surface : t.bg }]}>
                  <Icone nome={op.icone} size={20} color={tipo === op.id ? t.brand : t.muted} />
                  <Text style={{ color: t.ink, fontWeight: '800', flex: 1 }}>{op.texto}</Text>
                </Pressable>
              ))}
              <TextInput value={texto} onChangeText={setTexto} placeholder="Conte com suas palavras (opcional)" placeholderTextColor={t.muted} multiline maxLength={1000}
                style={[styles.input, { color: t.ink, borderColor: t.line, backgroundColor: t.surface }]} />
              <Button3D label="Enviar" disabled={!tipo} onPress={() => { if (!tipo) return; relatar({ tipo, texto: texto.trim(), exId, licao }); setEnviado(true); }} />
              <Button3D label="Cancelar" variant="ghost" onPress={sair} />
            </>
          )}
        </Pressable>
      </Pressable>
    </Modal>
  );
}

const styles = StyleSheet.create({
  fundo: { flex: 1, backgroundColor: 'rgba(0,0,0,0.45)', alignItems: 'center', justifyContent: 'center', padding: 16 },
  card: { width: '100%', maxWidth: 420, borderRadius: 20, borderWidth: 2, padding: 18, gap: 10 },
  h: { fontSize: 22, fontWeight: '900' },
  op: { flexDirection: 'row', alignItems: 'center', gap: 10, borderWidth: 2, borderRadius: 14, padding: 10 },
  input: { borderWidth: 2, borderRadius: 14, padding: 10, minHeight: 64, fontWeight: '600', textAlignVertical: 'top' },
});
