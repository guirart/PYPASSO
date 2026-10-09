import { useState } from 'react';
import { Modal, Pressable, StyleSheet, Text, View } from 'react-native';
import type { ModeloBau } from '@/lib/baus';
import type { ItemInst } from '@/lib/itens';
import { useTheme } from '@/lib/theme';
import { BauAnimado } from './BauAnimado';
import { ImagemBau } from './baus-sprites';
import { DetalheItem } from './CartaoItem';

/**
 * Baú que caiu de uma luta: aparece fechado, a pessoa toca para abrir (a animação roda numa janela por cima de tudo) e,
 * depois de pegar, a peça fica à mostra. `quem` é o texto de quem deixou o baú ("O CHEFE", "A ELITE").
 */
export function BauDeDrop({ drop, quem, rotulo }: { drop: { item: ItemInst; bau: ModeloBau }; quem: string; rotulo: string }) {
  const t = useTheme();
  const [estado, setEstado] = useState<'fechado' | 'abrindo' | 'aberto'>('fechado');
  return (
    <>
      {estado !== 'aberto' ? (
        <Pressable onPress={() => setEstado('abrindo')} accessibilityRole="button" accessibilityLabel={rotulo} style={[styles.cartao, { backgroundColor: t.surface, borderColor: t.sun }]}>
          <ImagemBau modelo={drop.bau} esc={3} />
          <View style={{ flex: 1 }}>
            <Text style={{ color: t.sunDeep, fontWeight: '900', letterSpacing: 0.8 }}>{quem} DEIXOU CAIR UM BAÚ</Text>
            <Text style={{ color: t.ink, fontWeight: '800', fontSize: 14 }}>{drop.bau.nome}</Text>
            <Text style={{ color: t.muted, fontWeight: '700', fontSize: 13 }}>Toque para abrir e ver qual peça saiu.</Text>
          </View>
        </Pressable>
      ) : (
        <View style={{ width: '100%', alignItems: 'center', gap: 6 }}>
          <Text style={{ color: t.sunDeep, fontWeight: '900', letterSpacing: 0.8 }}>{quem} DEIXOU CAIR UMA PEÇA</Text>
          <DetalheItem item={drop.item} />
        </View>
      )}
      <Modal visible={estado === 'abrindo'} transparent animationType="fade" onRequestClose={() => setEstado('aberto')}>
        <BauAnimado item={drop.item} bau={drop.bau} onFim={() => setEstado('aberto')} />
      </Modal>
    </>
  );
}

const styles = StyleSheet.create({
  cartao: { flexDirection: 'row', alignItems: 'center', gap: 12, borderWidth: 3, borderRadius: 18, padding: 12, width: '100%', maxWidth: 440 },
});
