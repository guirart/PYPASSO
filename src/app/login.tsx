import { router } from 'expo-router';
import { useState } from 'react';
import { Pressable, StyleSheet, Text, TextInput, View } from 'react-native';
import { Button3D } from '@/components/Button3D';
import { Mascot } from '@/components/Characters';
import { supabase } from '@/lib/supabase';
import { useTheme } from '@/lib/theme';

/** Login sem senha: o Supabase envia um código de 6 dígitos por e-mail. */
export default function LoginScreen() {
  const t = useTheme();
  const [email, setEmail] = useState('');
  const [code, setCode] = useState('');
  const [sent, setSent] = useState(false);
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);
  const [withPassword, setWithPassword] = useState(false);
  const [password, setPassword] = useState('');

  if (!supabase) {
    return (
      <View style={[styles.wrap, { backgroundColor: t.bg }]}>
        <Text style={[styles.h1, { color: t.ink }]}>Login indisponível</Text>
        <Text style={{ color: t.muted }}>Configure EXPO_PUBLIC_SUPABASE_URL e EXPO_PUBLIC_SUPABASE_ANON_KEY no arquivo .env.</Text>
        <Button3D label="Voltar" onPress={() => router.back()} />
      </View>
    );
  }

  const send = async () => {
    setBusy(true); setMsg(null);
    const { error } = await supabase!.auth.signInWithOtp({ email: email.trim(), options: { shouldCreateUser: true } });
    setBusy(false);
    if (error) setMsg('Não deu para enviar o código. Confira o e-mail e tente de novo.');
    else setSent(true);
  };
  const signInPassword = async () => {
    setBusy(true); setMsg(null);
    const { error } = await supabase!.auth.signInWithPassword({ email: email.trim(), password });
    setBusy(false);
    if (error) setMsg('E-mail ou senha incorretos.');
    else router.back();
  };
  const verify = async () => {
    setBusy(true); setMsg(null);
    const { error } = await supabase!.auth.verifyOtp({ email: email.trim(), token: code.trim(), type: 'email' });
    setBusy(false);
    if (error) setMsg('Código inválido ou expirado. Peça um novo.');
    else router.back();
  };

  const input = [styles.input, { borderColor: t.line, backgroundColor: t.surface, color: t.ink }];
  return (
    <View style={[styles.wrap, { backgroundColor: t.bg }]}>
      <Mascot size={110} mood={sent ? 'think' : 'happy'} />
      <Text style={[styles.h1, { color: t.ink }]}>{sent ? 'Digite o código' : 'Entrar no PyPasso'}</Text>
      <Text style={{ color: t.muted, fontWeight: '600', textAlign: 'center' }}>
        {withPassword ? 'Entre com seu e-mail e senha.' : sent ? `Enviamos um código de 6 dígitos para ${email}.` : 'Sem senha: você recebe um código por e-mail.'}
      </Text>
      {withPassword ? (
        <>
          <TextInput value={email} onChangeText={setEmail} placeholder="seu@email.com" placeholderTextColor={t.muted}
            keyboardType="email-address" autoCapitalize="none" autoComplete="email" style={input} accessibilityLabel="E-mail" />
          <TextInput value={password} onChangeText={setPassword} placeholder="Senha" placeholderTextColor={t.muted}
            secureTextEntry autoCapitalize="none" autoComplete="password" style={input} accessibilityLabel="Senha" />
        </>
      ) : !sent ? (
        <TextInput value={email} onChangeText={setEmail} placeholder="seu@email.com" placeholderTextColor={t.muted}
          keyboardType="email-address" autoCapitalize="none" autoComplete="email" style={input} />
      ) : (
        <TextInput value={code} onChangeText={setCode} placeholder="123456" placeholderTextColor={t.muted}
          keyboardType="number-pad" maxLength={6} autoComplete="one-time-code" style={[input, { letterSpacing: 6, textAlign: 'center' }]} />
      )}
      {msg && <Text style={{ color: t.bad, fontWeight: '700' }}>{msg}</Text>}
      {withPassword ? (
        <Button3D style={{ alignSelf: 'stretch' }} label={busy ? 'Aguarde…' : 'Entrar'}
          disabled={busy || !email.includes('@') || !password} onPress={signInPassword} />
      ) : (
        <Button3D style={{ alignSelf: 'stretch' }} label={busy ? 'Aguarde…' : sent ? 'Entrar' : 'Enviar código'}
          disabled={busy || (sent ? code.length < 6 : !email.includes('@'))} onPress={sent ? verify : send} />
      )}
      {!sent && (
        <Pressable onPress={() => { setWithPassword(!withPassword); setMsg(null); }}>
          <Text style={{ color: t.brand, fontWeight: '700' }}>{withPassword ? 'Entrar com código no e-mail' : 'Já tenho senha'}</Text>
        </Pressable>
      )}
      <Button3D style={{ alignSelf: 'stretch' }} variant="ghost" label="Cancelar" onPress={() => router.back()} />
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { flex: 1, padding: 24, gap: 16, alignItems: 'center', justifyContent: 'center', maxWidth: 440, width: '100%', alignSelf: 'center' },
  h1: { fontSize: 26, fontWeight: '900', textAlign: 'center' },
  input: { alignSelf: 'stretch', borderWidth: 2, borderRadius: 14, paddingVertical: 14, paddingHorizontal: 16, fontSize: 18 },
});
