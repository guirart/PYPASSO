-- PyPasso — esquema do Supabase
-- Cole no SQL Editor do seu projeto Supabase e execute uma vez.

-- Perfis (um por usuário do Auth)
create table if not exists public.profiles (
  id uuid primary key references auth.users on delete cascade,
  display_name text check (char_length(display_name) <= 40),
  avatar_seed text,
  xp integer not null default 0,
  streak integer not null default 0,
  last_day text,
  league integer not null default 1,   -- 1 = Bronze, 2 = Prata, 3 = Ouro...
  created_at timestamptz not null default now()
);

-- Melhor resultado de cada lição
create table if not exists public.lesson_progress (
  user_id uuid not null references auth.users on delete cascade,
  lesson_id text not null,
  best_accuracy integer not null default 0,
  completed_at timestamptz not null default now(),
  primary key (user_id, lesson_id)
);

-- Cada ganho de XP vira um evento (base do ranking semanal)
create table if not exists public.xp_events (
  id bigint generated always as identity primary key,
  user_id uuid not null references auth.users on delete cascade,
  amount integer not null check (amount between 0 and 50),
  lesson_id text,
  created_at timestamptz not null default now()
);
create index if not exists xp_events_week_idx on public.xp_events (created_at, user_id);

-- Cria o perfil automaticamente quando alguém se cadastra
create or replace function public.handle_new_user()
returns trigger language plpgsql security definer set search_path = public as $$
begin
  insert into public.profiles (id) values (new.id) on conflict do nothing;
  return new;
end; $$;
drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created after insert on auth.users
  for each row execute function public.handle_new_user();

-- Segurança por linha: cada um só altera os próprios dados
alter table public.profiles enable row level security;
alter table public.lesson_progress enable row level security;
alter table public.xp_events enable row level security;

drop policy if exists "perfis visíveis para usuários logados" on public.profiles;
create policy "perfis visíveis para usuários logados" on public.profiles
  for select to authenticated using (true);
drop policy if exists "editar o próprio perfil" on public.profiles;
create policy "editar o próprio perfil" on public.profiles
  for update to authenticated using (auth.uid() = id) with check (auth.uid() = id);

drop policy if exists "ler o próprio progresso" on public.lesson_progress;
create policy "ler o próprio progresso" on public.lesson_progress
  for select to authenticated using (auth.uid() = user_id);
drop policy if exists "gravar o próprio progresso" on public.lesson_progress;
create policy "gravar o próprio progresso" on public.lesson_progress
  for insert to authenticated with check (auth.uid() = user_id);
drop policy if exists "atualizar o próprio progresso" on public.lesson_progress;
create policy "atualizar o próprio progresso" on public.lesson_progress
  for update to authenticated using (auth.uid() = user_id);

drop policy if exists "registrar o próprio xp" on public.xp_events;
create policy "registrar o próprio xp" on public.xp_events
  for insert to authenticated with check (auth.uid() = user_id);

-- Ranking da semana (segunda a domingo, horário de Brasília)
create or replace view public.weekly_leaderboard
with (security_invoker = false) as
select p.id as user_id, p.display_name, p.avatar_seed, p.league,
       coalesce(sum(e.amount), 0)::int as week_xp
from public.profiles p
left join public.xp_events e
  on e.user_id = p.id
 and e.created_at >= date_trunc('week', now() at time zone 'America/Sao_Paulo') at time zone 'America/Sao_Paulo'
group by p.id
having coalesce(sum(e.amount), 0) > 0 or p.id = auth.uid()
order by week_xp desc;

grant select on public.weekly_leaderboard to authenticated;

-- Denúncias de respostas da IA (exigência da Google Play para IA generativa)
create table if not exists public.ai_reports (
  id bigint generated always as identity primary key,
  user_id uuid references auth.users on delete cascade,
  motivo text not null check (char_length(motivo) <= 300),
  resposta jsonb not null,
  created_at timestamptz not null default now()
);
alter table public.ai_reports enable row level security;
drop policy if exists "registrar denúncia" on public.ai_reports;
create policy "registrar denúncia" on public.ai_reports
  for insert to authenticated with check (auth.uid() = user_id);

-- ============================================================ Ligas
-- 10 ligas: 1 Bronze (Noob) … 10 Diamante (Lenda Pythônica).
alter table public.profiles add column if not exists best_league integer not null default 1;

-- Resultado de cada semana (o app mostra a tela de "subiu/caiu" a partir daqui)
create table if not exists public.league_history (
  user_id uuid not null references auth.users on delete cascade,
  week_start date not null,
  from_league integer not null,
  to_league integer not null,
  rank integer not null,
  xp integer not null,
  visto boolean not null default false,
  primary key (user_id, week_start)
);
alter table public.league_history enable row level security;
drop policy if exists "ler o próprio histórico de liga" on public.league_history;
create policy "ler o próprio histórico de liga" on public.league_history
  for select to authenticated using (auth.uid() = user_id);
drop policy if exists "marcar resultado como visto" on public.league_history;
create policy "marcar resultado como visto" on public.league_history
  for update to authenticated using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- Fecha a semana anterior: em cada liga, os 5 primeiros sobem e os 3 últimos
-- (entre quem fez XP) descem. Quem não fez XP fica onde está.
create or replace function public.fechar_semana()
returns void language plpgsql security definer set search_path = public as $$
declare
  inicio timestamptz := (date_trunc('week', (now() at time zone 'America/Sao_Paulo') - interval '1 day')) at time zone 'America/Sao_Paulo';
begin
  if exists (select 1 from public.league_history where week_start = (inicio at time zone 'America/Sao_Paulo')::date) then
    return; -- semana já fechada
  end if;
  with xp as (
    select p.id, p.league, coalesce(sum(e.amount), 0)::int as w
    from public.profiles p
    left join public.xp_events e on e.user_id = p.id and e.created_at >= inicio and e.created_at < inicio + interval '7 days'
    group by p.id
  ), r as (
    select id, league, w,
           row_number() over (partition by league order by w desc) as rk,
           count(*) over (partition by league) as n
    from xp where w > 0
  ), novo as (
    select id, league as de, rk, w,
           least(10, greatest(1, league + case
             when rk <= 5 and league < 10 then 1
             when n > 8 and rk > n - 3 and league > 1 then -1
             else 0 end)) as para
    from r
  ), hist as (
    insert into public.league_history (user_id, week_start, from_league, to_league, rank, xp)
    select id, (inicio at time zone 'America/Sao_Paulo')::date, de, para, rk, w from novo
    returning user_id, to_league
  )
  update public.profiles p
     set league = h.to_league, best_league = greatest(p.best_league, h.to_league)
    from hist h where h.user_id = p.id;
end; $$;
revoke all on function public.fechar_semana() from public, anon, authenticated;

-- Agenda: toda segunda às 00:05 de Brasília (03:05 UTC).
-- Precisa da extensão pg_cron (Database → Extensions → pg_cron no painel do Supabase).
create extension if not exists pg_cron with schema extensions;
select cron.unschedule(jobid) from cron.job where jobname = 'pypasso-fechar-semana';
select cron.schedule('pypasso-fechar-semana', '5 3 * * 1', 'select public.fechar_semana()');

-- =====================================================================
-- Assinatura Plus (vidas ilimitadas)
-- Quem grava é só o servidor (webhooks do Stripe e do RevenueCat, com a chave de serviço).
-- O app lê a própria linha para saber se a conta é Plus.
-- =====================================================================
create table if not exists public.assinaturas (
  user_id uuid primary key references auth.users (id) on delete cascade,
  plano text not null default 'plus',
  origem text not null check (origem in ('stripe', 'play_store', 'app_store', 'outra')),
  status text not null check (status in ('nenhuma', 'teste', 'ativa', 'cancelada', 'atrasada', 'expirada')),
  ciclo text check (ciclo in ('mensal', 'anual')),
  expira_em timestamptz,
  teste_usado boolean not null default false,
  stripe_customer_id text unique,
  stripe_subscription_id text,
  atualizado_em timestamptz not null default now()
);
alter table public.assinaturas enable row level security;
drop policy if exists "ler a própria assinatura" on public.assinaturas;
create policy "ler a própria assinatura" on public.assinaturas
  for select using (auth.uid() = user_id);

-- Eventos de webhook já processados (evita processar duas vezes um reenvio).
create table if not exists public.webhook_eventos (
  id text primary key,
  origem text not null,
  recebido_em timestamptz not null default now()
);
alter table public.webhook_eventos enable row level security;

-- Plus vale enquanto não expirou (cancelada continua valendo até o fim do período pago).
create or replace function public.plus_ativo(uid uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (
    select 1 from public.assinaturas
    where user_id = uid
      and status in ('teste', 'ativa', 'cancelada', 'atrasada')
      and (expira_em is null or expira_em > now())
  );
$$;

-- ---------------------------------------------------------------------------
-- Teste com usuários (src/lib/teste.ts e TESTE-COM-USUARIOS.md)
-- Anônimo: só um código aleatório do aparelho. O app só insere; ninguém lê pelo app.
-- Leia no painel do Supabase (Table Editor / SQL) ou exporte em CSV.
create table if not exists public.teste_licoes (
  id bigint generated always as identity primary key,
  criado_em timestamptz not null default now(),
  aparelho text not null,
  licao text not null,
  segundos int not null default 0,
  erros jsonb not null default '{}'::jsonb, -- id do exercício -> nº de erros
  abandonou boolean not null default false
);
create table if not exists public.teste_relatos (
  id bigint generated always as identity primary key,
  criado_em timestamptz not null default now(),
  aparelho text not null,
  tipo text not null,
  texto text not null default '',
  exercicio text,
  licao text
);
alter table public.teste_licoes enable row level security;
alter table public.teste_relatos enable row level security;
drop policy if exists "app insere" on public.teste_licoes;
create policy "app insere" on public.teste_licoes for insert to anon, authenticated with check (char_length(aparelho) < 40);
drop policy if exists "app insere" on public.teste_relatos;
create policy "app insere" on public.teste_relatos for insert to anon, authenticated with check (char_length(texto) <= 1000);

-- Os exercícios em que mais se erra (rode no SQL Editor):
-- select e.key as exercicio, sum(e.value::int) as erros, count(*) as vezes
--   from public.teste_licoes, jsonb_each_text(erros) e group by 1 order by 2 desc limit 30;
