import { router } from 'expo-router';
import { useEffect, useState } from 'react';
import { Linking, Pressable, ScrollView, Share, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Button3D } from '@/components/Button3D';
import { Cross } from '@/components/Icons';
import { Icone } from '@/components/Icone';
import { deleteAccount } from '@/lib/account';
import { useLembretes } from '@/lib/lembretes-prefs';
import { apagarDadosDoAparelho, CONTATO_EMAIL, exportarDados, mudarConsentimento, PRIVACY_URL, ultimoRegistro, usePrivacidade, type Consentimento } from '@/lib/privacidade';
import { supabase } from '@/lib/supabase';
import { useTeste } from '@/lib/teste';
import { mono, useTheme } from '@/lib/theme';

const data = (ts: number) => new Date(ts).toLocaleDateString('pt-BR');

/** O que o app trata, para quê e com qual base legal. É o resumo da Política de Privacidade (store/politica-de-privacidade.html). */
const TRATAMENTOS: { dado: string; para: string; base: string }[] = [
  { dado: 'E-mail (só se criar conta)', para: 'Criar e entrar na conta', base: 'Execução de contrato' },
  { dado: 'Nome de exibição e avatar', para: 'Mostrar seu perfil e sua posição na liga a outros usuários', base: 'Execução de contrato' },
  { dado: 'Progresso, XP, sequência (só com conta)', para: 'Sincronizar entre aparelhos e calcular a liga semanal', base: 'Execução de contrato' },
  { dado: 'Código enviado ao Pipo com IA (só quando você toca em "Explicar com IA")', para: 'Gerar a explicação e a sugestão de correção', base: 'Execução de contrato' },
  { dado: 'Registros do teste: erros, tempos, lições deixadas no meio e relatos, ligados a um código aleatório do aparelho (só se você participar)', para: 'Melhorar os exercícios e o aplicativo', base: 'Consentimento' },
  { dado: 'Denúncias de respostas da IA', para: 'Melhorar a segurança e a qualidade das respostas', base: 'Legítimo interesse' },
];

/** Central de privacidade: onde estão os dados, as escolhas da pessoa, os direitos da LGPD (art. 18) e como apagar. */
export default function PrivacidadeScreen() {
  const t = useTheme();
  const insets = useSafeAreaInsets();
  const enviarTeste = useTeste((s) => s.enviar);
  const codigoTeste = useTeste((s) => s.codigo);
  const nRegistrosTeste = useTeste((s) => Object.keys(s.ex).length + Object.keys(s.licoes).length + s.relatos.length);
  const ia = usePrivacidade((s) => s.ia);
  const registros = usePrivacidade((s) => s.registros);
  const lembretes = useLembretes((s) => s.ativo);
  const [email, setEmail] = useState<string | null>(null);
  const [msg, setMsg] = useState('');
  const [ocupado, setOcupado] = useState(false);
  const [confirmar, setConfirmar] = useState<'aparelho' | 'conta' | null>(null);

  useEffect(() => {
    supabase?.auth.getUser().then(({ data: d }) => setEmail(d.user?.email ?? null)).catch(() => {});
  }, []);

  const copiar = async (texto: string, ok: string) => {
    try {
      if (typeof navigator !== 'undefined' && navigator.clipboard && typeof window !== 'undefined') await navigator.clipboard.writeText(texto);
      else await Share.share({ message: texto });
      setMsg(ok);
    } catch {
      setMsg('Não consegui copiar aqui. Tente de novo ou use outro aparelho.');
    }
  };

  const copiarDados = async () => {
    setOcupado(true); setMsg('');
    try {
      const r = await exportarDados();
      await copiar(r.texto, `Copiei seus dados (${r.campos} grupos deste aparelho${r.nuvem ? ' e o que está na sua conta' : ''}). Cole num arquivo para guardar.`);
    } catch {
      setMsg('Não foi possível reunir seus dados agora. Tente de novo.');
    }
    setOcupado(false);
  };

  const Escolha = ({ item, titulo, texto, ligado }: { item: Consentimento; titulo: string; texto: string; ligado: boolean }) => {
    const r = ultimoRegistro(registros, item);
    const semServidor = !supabase; // sem servidor ligado, não há nada a enviar: a opção só informa
    return (
      <Pressable onPress={() => mudarConsentimento(item, !ligado)} disabled={semServidor} accessibilityRole="switch" accessibilityState={{ checked: ligado, disabled: semServidor }} accessibilityLabel={titulo}
        style={[styles.linha, { borderColor: ligado && !semServidor ? t.good : t.line, backgroundColor: t.surface, opacity: semServidor ? 0.7 : 1 }]}>
        <View style={{ flex: 1, gap: 3 }}>
          <Text style={{ color: t.ink, fontWeight: '900' }}>{titulo}</Text>
          <Text style={{ color: t.muted, fontWeight: '600', fontSize: 13, lineHeight: 18 }}>{texto}</Text>
          {semServidor && <Text style={{ color: t.sunDeep, fontSize: 12, fontWeight: '800' }}>Indisponível: este app está sem servidor ligado, então nada é enviado.</Text>}
          {r && <Text style={{ color: t.muted, fontSize: 12 }}>Você {r.valor ? 'ativou' : 'desativou'} em {data(r.em)}.</Text>}
        </View>
        <View style={[styles.switch, { backgroundColor: ligado ? t.good : t.line }]}><View style={[styles.knob, { alignSelf: ligado ? 'flex-end' : 'flex-start' }]} /></View>
      </Pressable>
    );
  };

  return (
    <View style={{ flex: 1, backgroundColor: t.bg }}>
      <View style={[styles.head, { paddingTop: insets.top + 10, borderBottomColor: t.line }]}>
        <Pressable onPress={() => router.back()} accessibilityLabel="Fechar" hitSlop={10}><Cross color={t.muted} size={26} /></Pressable>
        <Text style={[styles.h1, { color: t.ink }]}>Privacidade e dados</Text>
      </View>
      <ScrollView contentContainerStyle={[styles.scroll, { paddingBottom: insets.bottom + 28 }]}>
        <Text style={{ color: t.muted, fontWeight: '700', fontSize: 15, lineHeight: 22 }}>
          Aqui você vê o que o PyPasso guarda, escolhe o que compartilha e pode copiar ou apagar seus dados quando quiser.
        </Text>

        <Text style={[styles.sec, { color: t.ink }]}>Onde estão seus dados</Text>
        <View style={[styles.card, { backgroundColor: t.surface, borderColor: t.line }]}>
          <Text style={{ color: t.ink, fontWeight: '900' }}>Neste aparelho</Text>
          <Text style={{ color: t.muted, fontWeight: '600', lineHeight: 20 }}>
            Seu progresso, XP e moedas, o nome e o avatar que você escolheu, os arquivos da aba Código e as preferências. Sem conta, nada disso sai daqui.
          </Text>
        </View>
        <View style={[styles.card, { backgroundColor: t.surface, borderColor: email ? t.brand : t.line }]}>
          <Text style={{ color: t.ink, fontWeight: '900' }}>Na nuvem</Text>
          <Text style={{ color: t.muted, fontWeight: '600', lineHeight: 20 }}>
            {!supabase ? 'Este app está sem servidor ligado: nada é enviado para a nuvem.'
              : email ? `Conta ${email}: guardamos seu e-mail, nome, avatar, XP, sequência, progresso das lições e posição na liga. Seu nome e avatar aparecem para outros jogadores na liga.`
              : 'Você não entrou em nenhuma conta, então nada do seu progresso está na nuvem.'}
          </Text>
        </View>

        <Text style={[styles.sec, { color: t.ink }]}>Suas escolhas</Text>
        <Escolha item="teste" ligado={enviarTeste} titulo="Participar do teste do app"
          texto="Envia, sem nome nem e-mail, onde você erra, quanto tempo leva, onde desiste e o que relata no botão “Travei aqui”. Desligado, esses registros ficam só neste aparelho." />
        <Escolha item="ia" ligado={ia} titulo="Explicações com IA no Pipo"
          texto="Quando você toca em “Explicar com IA”, o código, as entradas, a saída e o erro vão para o nosso servidor e para o provedor de IA. Desligado, o botão some e nada disso é enviado. A análise local do Pipo continua funcionando." />
        <View style={[styles.linha, { borderColor: t.line, backgroundColor: t.surface }]}>
          <View style={{ flex: 1, gap: 3 }}>
            <Text style={{ color: t.ink, fontWeight: '900' }}>Lembretes diários: {lembretes ? 'ligados' : 'desligados'}</Text>
            <Text style={{ color: t.muted, fontWeight: '600', fontSize: 13, lineHeight: 18 }}>São agendados no próprio aparelho e não enviam dados a ninguém. Mude em Perfil → Lembretes.</Text>
          </View>
        </View>

        <Text style={[styles.sec, { color: t.ink }]}>Seus direitos</Text>
        <View style={[styles.card, { backgroundColor: t.surface, borderColor: t.line }]}>
          <Text style={{ color: t.ink, fontWeight: '900' }}>Acesso e portabilidade</Text>
          <Text style={{ color: t.muted, fontWeight: '600', lineHeight: 20 }}>Copie tudo o que o app tem sobre você, num texto em formato JSON, que você pode guardar ou levar para outro serviço.</Text>
          <Button3D label={ocupado ? 'Reunindo seus dados…' : 'Copiar meus dados'} disabled={ocupado} onPress={copiarDados} />
        </View>
        <View style={[styles.card, { backgroundColor: t.surface, borderColor: t.line }]}>
          <Text style={{ color: t.ink, fontWeight: '900' }}>Correção</Text>
          <Text style={{ color: t.muted, fontWeight: '600', lineHeight: 20 }}>Seu nome fica em Perfil → Seu nome. O avatar, em Editar avatar.</Text>
          <Button3D label="Editar avatar" variant="ghost" onPress={() => router.replace('/avatar')} />
        </View>
        <View style={[styles.card, { backgroundColor: t.surface, borderColor: t.line }]}>
          <Text style={{ color: t.ink, fontWeight: '900' }}>Eliminação</Text>
          <Text style={{ color: t.muted, fontWeight: '600', lineHeight: 20 }}>
            Apagar os dados deste aparelho remove progresso, nome, avatar, moedas, arquivos da aba Código e os registros do teste que estão aqui. Não apaga a conta nem o que já foi enviado para a nuvem.
          </Text>
          {confirmar === 'aparelho' ? (
            <View style={[styles.aviso, { borderColor: t.bad }]}>
              <Text style={{ color: t.ink, fontWeight: '700' }}>Isso não pode ser desfeito. Apagar os dados deste aparelho?</Text>
              <Button3D label="Sim, apagar" variant="bad" onPress={() => { apagarDadosDoAparelho(); setConfirmar(null); setMsg('Os dados deste aparelho foram apagados.'); }} />
              <Button3D label="Cancelar" variant="ghost" onPress={() => setConfirmar(null)} />
            </View>
          ) : <Button3D label="Apagar os dados deste aparelho" variant="ghost" onPress={() => setConfirmar('aparelho')} />}

          {email && (confirmar === 'conta' ? (
            <View style={[styles.aviso, { borderColor: t.bad }]}>
              <Text style={{ color: t.ink, fontWeight: '700' }}>Excluir a conta apaga para sempre seu perfil, progresso, XP, posição na liga e denúncias. Isso não pode ser desfeito.</Text>
              <Button3D label={ocupado ? 'Excluindo…' : 'Sim, excluir minha conta'} variant="bad" disabled={ocupado}
                onPress={async () => { setOcupado(true); const r = await deleteAccount(); setOcupado(false); setConfirmar(null); if (r.ok) { setEmail(null); setMsg('Sua conta e seus dados na nuvem foram excluídos.'); } else setMsg(r.message ?? 'Não foi possível excluir agora.'); }} />
              <Button3D label="Cancelar" variant="ghost" disabled={ocupado} onPress={() => setConfirmar(null)} />
            </View>
          ) : <Button3D label="Excluir minha conta" variant="bad" onPress={() => setConfirmar('conta')} />)}
        </View>
        {!!msg && <Text style={{ color: t.good, fontWeight: '800', lineHeight: 20 }} accessibilityLiveRegion="polite">{msg}</Text>}

        {(
          <View style={[styles.card, { backgroundColor: t.surface, borderColor: t.line }]}>
            <Text style={{ color: t.ink, fontWeight: '900' }}>Registros do teste</Text>
            <Text style={{ color: t.muted, fontWeight: '600', lineHeight: 20 }}>
              Há {nRegistrosTeste} registros do teste neste aparelho (onde você erra, tempos e relatos), sem nome nem e-mail. {supabase ? `Desligar a participação interrompe o envio, mas o que já foi enviado fica no servidor, ligado só a este código. Para pedir a eliminação, informe o código${CONTATO_EMAIL ? ` em ${CONTATO_EMAIL}` : ' ao responsável pelo app'}:` : 'Sem servidor ligado, eles ficam só aqui. Seu código de aparelho:'}
            </Text>
            <Pressable onPress={() => copiar(codigoTeste, 'Código copiado.')} accessibilityRole="button" accessibilityLabel={`Copiar o código do aparelho ${codigoTeste}`} style={[styles.codigo, { borderColor: t.line, backgroundColor: t.bg }]}>
              <Text style={{ color: t.ink, fontFamily: mono, fontWeight: '800' }}>{codigoTeste}</Text>
              <Icone nome="copiar" size={18} color={t.brand} />
            </Pressable>
          </View>
        )}

        <Text style={[styles.sec, { color: t.ink }]}>Como tratamos seus dados</Text>
        <View style={[styles.card, { backgroundColor: t.surface, borderColor: t.line, gap: 10 }]}>
          {TRATAMENTOS.map((x) => (
            <View key={x.dado} style={{ gap: 2 }}>
              <Text style={{ color: t.ink, fontWeight: '800', lineHeight: 19 }}>{x.dado}</Text>
              <Text style={{ color: t.muted, fontSize: 13, lineHeight: 18 }}>{x.para} · Base legal: {x.base}</Text>
            </View>
          ))}
          <Text style={{ color: t.muted, fontSize: 12, lineHeight: 17 }}>
            Não coletamos localização, contatos, fotos nem identificadores de publicidade, e o app não tem anúncios. O PyPasso é para maiores de 13 anos; menores de 18 devem usá-lo com o conhecimento dos responsáveis. Este é um resumo: vale a Política de Privacidade completa.
          </Text>
          {PRIVACY_URL ? (
            <Pressable onPress={() => Linking.openURL(PRIVACY_URL)} accessibilityRole="link"><Text style={{ color: t.brand, fontWeight: '800' }}>Ler a Política de Privacidade completa</Text></Pressable>
          ) : null}
          {CONTATO_EMAIL ? <Text style={{ color: t.muted, fontSize: 13 }}>Dúvidas ou pedidos sobre seus dados: {CONTATO_EMAIL}</Text> : null}
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  head: { flexDirection: 'row', alignItems: 'center', gap: 14, paddingHorizontal: 16, paddingBottom: 12, borderBottomWidth: 1 },
  h1: { flex: 1, fontSize: 22, fontWeight: '900' },
  scroll: { padding: 16, gap: 12, maxWidth: 640, width: '100%', alignSelf: 'center' },
  sec: { fontSize: 18, fontWeight: '900', marginTop: 8 },
  card: { borderWidth: 2, borderRadius: 16, padding: 14, gap: 8 },
  linha: { flexDirection: 'row', alignItems: 'center', gap: 12, borderWidth: 2, borderRadius: 16, padding: 14 },
  switch: { width: 46, height: 28, borderRadius: 99, padding: 3, justifyContent: 'center' },
  knob: { width: 22, height: 22, borderRadius: 11, backgroundColor: '#fff' },
  aviso: { gap: 10, borderWidth: 2, borderRadius: 14, padding: 12 },
  codigo: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', borderWidth: 2, borderRadius: 12, paddingVertical: 10, paddingHorizontal: 14 },
});
