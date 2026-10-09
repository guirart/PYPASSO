import * as Notifications from 'expo-notifications';
import { Platform } from 'react-native';
import { mensagem, useLembretes } from './lembretes-prefs';
import { useGame } from './store';

/**
 * Lembretes diários (só no celular). Em vez de um alarme repetido, agendamos os próximos 7 dias
 * no horário escolhido, pulando hoje se a pessoa já estudou. Reagendamos ao abrir o app, ao
 * terminar uma lição e ao mudar o horário; assim a mensagem cita a sequência atual.
 */
export const LEMBRETES_SUPORTADOS = true;
const CANAL = 'lembretes';

Notifications.setNotificationHandler({
  handleNotification: async () => ({ shouldShowBanner: true, shouldShowList: true, shouldPlaySound: false, shouldSetBadge: false }),
});

export async function pedirPermissao(): Promise<boolean> {
  if (Platform.OS === 'android') {
    await Notifications.setNotificationChannelAsync(CANAL, { name: 'Lembretes de estudo', importance: Notifications.AndroidImportance.DEFAULT });
  }
  const atual = await Notifications.getPermissionsAsync();
  if (atual.granted) return true;
  const r = await Notifications.requestPermissionsAsync({ ios: { allowAlert: true, allowSound: true, allowBadge: false } });
  return r.granted;
}

export async function agendarLembretes() {
  try {
    await Notifications.cancelAllScheduledNotificationsAsync();
    const { ativo, hora, minuto } = useLembretes.getState();
    if (!ativo) return;
    if (!(await Notifications.getPermissionsAsync()).granted) return;
    const g = useGame.getState();
    const hoje = new Date();
    const estudouHoje = g.lastDay === `${hoje.getFullYear()}-${hoje.getMonth() + 1}-${hoje.getDate()}`;
    for (let d = 0; d < 7; d++) {
      const quando = new Date(); quando.setDate(quando.getDate() + d); quando.setHours(hora, minuto, 0, 0);
      if (quando.getTime() <= Date.now() + 60_000) continue;
      if (d === 0 && estudouHoje) continue;
      // Sequência que estará valendo naquele dia se a pessoa estudar hoje/ontem.
      const seq = d === 0 || (d === 1 && estudouHoje) ? g.streak : 0;
      const m = mensagem(seq, d + hoje.getDate());
      await Notifications.scheduleNotificationAsync({
        content: { title: m.titulo, body: m.corpo },
        trigger: { type: Notifications.SchedulableTriggerInputTypes.DATE, date: quando, ...(Platform.OS === 'android' ? { channelId: CANAL } : {}) },
      });
    }
  } catch {
    // Sem permissão ou no Expo Go limitado: segue sem lembrete.
  }
}

/** Um lembrete de teste daqui a 5 segundos (botão no Perfil). */
export async function testarLembrete() {
  if (!(await pedirPermissao())) return false;
  const m = mensagem(useGame.getState().streak, Date.now());
  await Notifications.scheduleNotificationAsync({
    content: { title: m.titulo, body: m.corpo },
    trigger: { type: Notifications.SchedulableTriggerInputTypes.TIME_INTERVAL, seconds: 5, ...(Platform.OS === 'android' ? { channelId: CANAL } : {}) },
  });
  return true;
}
